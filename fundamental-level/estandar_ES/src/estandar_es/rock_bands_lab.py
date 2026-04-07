"""
Lab: Ingesta de CSV, métricas y exportación a JSON; logging con distintos niveles.

Flujo:
1. Configura logging con niveles DEBUG, INFO, WARNING y ERROR.
2. Lee rock_bands.csv con pathlib + csv.DictReader.
3. Valida cada fila y registra advertencias si hay campos vacíos.
4. Calcula métricas: total de bandas, por país, por género y por década.
5. Exporta los resultados a JSON con sangría legible.
"""

import csv
import json
import logging
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuración de logging
# ---------------------------------------------------------------------------


def setup_logging(level: int = logging.DEBUG) -> logging.Logger:
    """Configura y devuelve el logger del módulo con un handler de consola."""
    logger = logging.getLogger("rock_bands_lab")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# ---------------------------------------------------------------------------
# Ingesta de CSV
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {"Band", "Country/Region", "City", "Formed", "Primary Genre"}


def load_bands(csv_path: Path, logger: logging.Logger) -> list[dict]:
    """Lee el CSV y devuelve una lista de diccionarios.

    Registra un WARNING por cada fila con campos vacíos o año inválido,
    y un ERROR si el archivo no existe o faltan columnas obligatorias.
    """
    logger.info("Cargando archivo: %s", csv_path)

    if not csv_path.exists():
        logger.error("El archivo no existe: %s", csv_path)
        raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")

    bands: list[dict] = []

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        missing = REQUIRED_FIELDS - set(reader.fieldnames or [])
        if missing:
            logger.error("Columnas obligatorias faltantes en el CSV: %s", missing)
            raise ValueError(f"Columnas faltantes: {missing}")

        for line_num, row in enumerate(reader, start=2):
            logger.debug("Procesando fila %d: %s", line_num, row.get("Band"))

            empty_fields = [k for k, v in row.items() if not v or not v.strip()]
            if empty_fields:
                logger.warning(
                    "Fila %d ('%s'): campos vacíos → %s",
                    line_num,
                    row.get("Band"),
                    empty_fields,
                )

            formed_raw = row.get("Formed", "").strip()
            try:
                row["Formed"] = int(formed_raw)
            except ValueError:
                logger.warning(
                    "Fila %d ('%s'): 'Formed' no es un año válido → '%s'",
                    line_num,
                    row.get("Band"),
                    formed_raw,
                )
                row["Formed"] = None

            bands.append(row)

    logger.info("Total de bandas cargadas: %d", len(bands))
    return bands


# ---------------------------------------------------------------------------
# Cálculo de métricas
# ---------------------------------------------------------------------------


def compute_metrics(bands: list[dict], logger: logging.Logger) -> dict:
    """Calcula métricas agregadas a partir de la lista de bandas."""
    logger.info("Calculando métricas para %d bandas…", len(bands))

    by_country: dict[str, int] = defaultdict(int)
    by_genre: dict[str, int] = defaultdict(int)
    by_decade: dict[str, int] = defaultdict(int)
    valid_years: list[int] = []

    for band in bands:
        country = band.get("Country/Region", "").strip() or "Desconocido"
        genre = band.get("Primary Genre", "").strip() or "Desconocido"
        formed = band.get("Formed")

        by_country[country] += 1
        by_genre[genre] += 1

        if isinstance(formed, int):
            decade = f"{(formed // 10) * 10}s"
            by_decade[decade] += 1
            valid_years.append(formed)
        else:
            logger.debug(
                "Banda '%s' excluida del cálculo de decadas (año None).",
                band.get("Band"),
            )

    average_year = (
        round(sum(valid_years) / len(valid_years), 1) if valid_years else None
    )

    metrics = {
        "total_bands": len(bands),
        "average_formation_year": average_year,
        "bands_by_country": dict(
            sorted(by_country.items(), key=lambda x: x[1], reverse=True)
        ),
        "bands_by_genre": dict(
            sorted(by_genre.items(), key=lambda x: x[1], reverse=True)
        ),
        "bands_by_decade": dict(sorted(by_decade.items())),
    }

    logger.debug("Métrica 'bands_by_country': %s", metrics["bands_by_country"])
    logger.debug("Métrica 'bands_by_genre': %s", metrics["bands_by_genre"])
    logger.debug("Métrica 'bands_by_decade': %s", metrics["bands_by_decade"])
    logger.info("Métricas calculadas correctamente.")

    return metrics


# ---------------------------------------------------------------------------
# Exportación a JSON
# ---------------------------------------------------------------------------


def export_to_json(data: dict, output_path: Path, logger: logging.Logger) -> None:
    """Serializa `data` como JSON con sangría de 2 espacios en `output_path`."""
    logger.info("Exportando resultados a: %s", output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    logger.info(
        "Exportación completada. Tamaño del archivo: %d bytes",
        output_path.stat().st_size,
    )


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def run(
    csv_path: Path, output_path: Path, logger: logging.Logger | None = None
) -> dict:
    """Ejecuta el pipeline completo: ingesta → métricas → exportación.

    Parameters
    ----------
    csv_path:    ruta al archivo CSV de entrada.
    output_path: ruta donde se guardará el JSON de salida.
    logger:      logger opcional; si no se provee, se crea uno interno.

    Returns
    -------
    Diccionario con las métricas calculadas.
    """
    if logger is None:
        logger = setup_logging()

    bands = load_bands(csv_path, logger)
    metrics = compute_metrics(bands, logger)
    export_to_json(metrics, output_path, logger)

    return metrics


if __name__ == "__main__":
    _logger = setup_logging(logging.DEBUG)

    _base = Path(__file__).resolve().parents[2]
    _csv = _base / "rock_bands.csv"
    _out = _base / "output" / "rock_bands_metrics.json"

    run(_csv, _out, _logger)
