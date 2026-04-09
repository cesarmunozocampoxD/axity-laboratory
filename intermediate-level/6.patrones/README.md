# Patrones de Diseño – Lab

Laboratorio práctico de patrones de diseño en Python


## Requisitos

- Python ≥ 3.12
- [Poetry](https://python-poetry.org/)

## Instalación

```bash
poetry install
```

## Ejecutar las pruebas

```bash
poetry run pytest tests/ -v
```

## Estructura del proyecto

```
src/
  patrones/
    __init__.py
    pricing.py      # Strategy – precios
    cache.py        # Decorator – caché
    provider.py     # Adapter – proveedor externo
tests/
  __init__.py
  test_patterns.py  # 21 pruebas con pytest
pyproject.toml
WIKI.md             # Guía teórica de patrones creacionales y estructurales
```

## Descripción de los módulos

### `pricing.py` – Strategy

`PriceCalculator` delega el cálculo al objeto estrategia que recibe.
Las estrategias disponibles son:

- `RegularPricing` – precio base sin descuento
- `MemberPricing` – 10 % de descuento para miembros
- `SalePricing` – 30 % de descuento en temporada de rebajas

La estrategia se puede cambiar en tiempo de ejecución con `set_strategy()`.

```python
from patrones.pricing import PriceCalculator, SalePricing

calc = PriceCalculator(SalePricing())
print(calc.get_price(100.0))  # 70.0
```

### `cache.py` – Decorator

`CachedPriceCalculator` envuelve cualquier objeto que tenga `get_price()` y almacena los resultados para evitar cálculos repetidos.

```python
from patrones.pricing import PriceCalculator, MemberPricing
from patrones.cache import CachedPriceCalculator

calc = PriceCalculator(MemberPricing())
cached = CachedPriceCalculator(calc)

cached.get_price(100.0)  # calcula y guarda
cached.get_price(100.0)  # devuelve desde caché
print(cached.cache_size)  # 1
```

### `provider.py` – Adapter

`ExternalPricingService` simula un servicio de terceros con una interfaz diferente (`fetch_price`).
`ExternalPricingAdapter` expone `get_price()` para que el resto de la aplicación no dependa del contrato externo.

```python
from patrones.provider import ExternalPricingService, ExternalPricingAdapter

service = ExternalPricingService()
adapter = ExternalPricingAdapter(service, "PROD-1")

print(adapter.get_price(100.0))  # 85.0
```

### Composición de los tres patrones

Los tres comparten la misma interfaz `get_price()`, por lo que se pueden encadenar:

```python
from patrones.provider import ExternalPricingService, ExternalPricingAdapter
from patrones.cache import CachedPriceCalculator

service = ExternalPricingService()
adapter = ExternalPricingAdapter(service, "PROD-1")
cached  = CachedPriceCalculator(adapter)

print(cached.get_price(200.0))  # 170.0 – calculado una vez, cacheado
print(cached.get_price(200.0))  # 170.0 – desde caché
```
