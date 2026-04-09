"""
Lab: Cargar/limpiar CSV en Pandas → entrenar un clasificador → guardar con joblib → inferencia.

Dataset: flores.csv (variante simplificada del clásico Iris).
Modelo:  DecisionTreeClassifier (sklearn) — simple, interpretable, sin hiperparámetros complejos.
"""

from __future__ import annotations

from pathlib import Path

import joblib  # type: ignore
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Columnas de características que usa el modelo
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
TARGET = "species"


# ---------------------------------------------------------------------------
# 1. Cargar y limpiar
# ---------------------------------------------------------------------------


def load_and_clean(csv_path: str | Path) -> pd.DataFrame:
    """Carga el CSV y elimina las filas con valores nulos.

    Pasos de limpieza:
    - Leer con pd.read_csv
    - Eliminar filas con cualquier NaN (dropna)
    - Reiniciar el índice
    """
    df = pd.read_csv(csv_path)

    filas_antes = len(df)
    df = df.dropna()
    filas_despues = len(df)

    print(
        f"[limpieza] filas cargadas: {filas_antes} | eliminadas: {filas_antes - filas_despues} | limpias: {filas_despues}"
    )

    df = df.reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# 2. Entrenar clasificador
# ---------------------------------------------------------------------------


def train_classifier(df: pd.DataFrame) -> DecisionTreeClassifier:
    """Entrena un DecisionTreeClassifier con las columnas de FEATURES → TARGET."""
    X = df[FEATURES]
    y = df[TARGET]

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    print(f"[entrenamiento] clases aprendidas: {list(model.classes_)}")
    return model


# ---------------------------------------------------------------------------
# 3. Guardar modelo con joblib
# ---------------------------------------------------------------------------


def save_model(model: DecisionTreeClassifier, model_path: str | Path) -> None:
    """Serializa el modelo entrenado en disco usando joblib."""
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"[guardado] modelo guardado en: {model_path}")


# ---------------------------------------------------------------------------
# 4. Inferencia
# ---------------------------------------------------------------------------


def predict(model_path: str | Path, features: list[float]) -> str:
    """Carga el modelo desde disco y predice la especie para un nuevo ejemplo.

    Args:
        model_path: ruta al archivo .joblib del modelo guardado.
        features:   lista con los valores [sepal_length, sepal_width, petal_length, petal_width].

    Returns:
        Nombre de la especie predicha como string.
    """
    model: DecisionTreeClassifier = joblib.load(model_path)
    prediction = model.predict([features])
    return str(prediction[0])


# ---------------------------------------------------------------------------
# Script de demostración (ejecutar directamente con: python -m ciencia_datos.clasificador)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    BASE = Path(__file__).parent.parent.parent  # raíz del proyecto

    # 1. Cargar y limpiar
    df = load_and_clean(BASE / "data" / "flores.csv")
    print(df.head())

    # 2. Entrenar
    model = train_classifier(df)

    # 3. Guardar
    model_path = BASE / "models" / "flores_model.joblib"
    save_model(model, model_path)

    # 4. Inferencia con un ejemplo nuevo
    ejemplo = [5.1, 3.5, 1.4, 0.2]  # típico de setosa
    especie = predict(model_path, ejemplo)
    print(f"[inferencia] features={ejemplo} → predicción: {especie}")
