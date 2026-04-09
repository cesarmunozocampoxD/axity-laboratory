"""
Tests del laboratorio de ciencia de datos:
  - carga y limpieza de CSV
  - entrenamiento del clasificador
  - guardado con joblib e inferencia
"""

from pathlib import Path

import pandas as pd
import pytest  # type: ignore
from ciencia_datos.clasificador import (
    FEATURES,
    TARGET,
    load_and_clean,
    predict,
    save_model,
    train_classifier,
)

DATA_PATH = Path(__file__).parent.parent / "data" / "flores.csv"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def df_limpio() -> pd.DataFrame:
    return load_and_clean(DATA_PATH)


@pytest.fixture(scope="module")
def modelo_entrenado(df_limpio):
    return train_classifier(df_limpio)


# ---------------------------------------------------------------------------
# 1. Tests de carga y limpieza
# ---------------------------------------------------------------------------


class TestLoadAndClean:
    def test_retorna_dataframe(self, df_limpio):
        assert isinstance(df_limpio, pd.DataFrame)

    def test_sin_nulos(self, df_limpio):
        assert df_limpio.isnull().sum().sum() == 0

    def test_columnas_presentes(self, df_limpio):
        for col in FEATURES + [TARGET]:
            assert col in df_limpio.columns

    def test_filas_limpias(self, df_limpio):
        # El CSV tiene 33 filas totales; 3 contienen NaN → quedan 30
        assert len(df_limpio) == 30

    def test_indice_reiniciado(self, df_limpio):
        assert df_limpio.index.tolist() == list(range(len(df_limpio)))


# ---------------------------------------------------------------------------
# 2. Tests del entrenamiento
# ---------------------------------------------------------------------------


class TestTrainClassifier:
    def test_tiene_metodo_predict(self, modelo_entrenado):
        assert hasattr(modelo_entrenado, "predict")

    def test_clases_esperadas(self, modelo_entrenado):
        assert set(modelo_entrenado.classes_) == {"setosa", "versicolor", "virginica"}

    def test_predice_setosa(self, modelo_entrenado):
        # Valores típicos de setosa
        pred = modelo_entrenado.predict([[5.1, 3.5, 1.4, 0.2]])
        assert pred[0] == "setosa"

    def test_predice_versicolor(self, modelo_entrenado):
        pred = modelo_entrenado.predict([[6.4, 3.2, 4.5, 1.5]])
        assert pred[0] == "versicolor"

    def test_predice_virginica(self, modelo_entrenado):
        pred = modelo_entrenado.predict([[7.1, 3.0, 5.9, 2.1]])
        assert pred[0] == "virginica"


# ---------------------------------------------------------------------------
# 3. Tests de guardado con joblib e inferencia
# ---------------------------------------------------------------------------


class TestSaveAndPredict:
    def test_archivo_creado(self, modelo_entrenado, tmp_path):
        model_file = tmp_path / "model.joblib"
        save_model(modelo_entrenado, model_file)
        assert model_file.exists()

    def test_inferencia_setosa(self, modelo_entrenado, tmp_path):
        model_file = tmp_path / "model.joblib"
        save_model(modelo_entrenado, model_file)
        resultado = predict(model_file, [5.1, 3.5, 1.4, 0.2])
        assert resultado == "setosa"

    def test_inferencia_versicolor(self, modelo_entrenado, tmp_path):
        model_file = tmp_path / "model.joblib"
        save_model(modelo_entrenado, model_file)
        resultado = predict(model_file, [6.4, 3.2, 4.5, 1.5])
        assert resultado == "versicolor"

    def test_inferencia_virginica(self, modelo_entrenado, tmp_path):
        model_file = tmp_path / "model.joblib"
        save_model(modelo_entrenado, model_file)
        resultado = predict(model_file, [7.1, 3.0, 5.9, 2.1])
        assert resultado == "virginica"

    def test_retorna_string(self, modelo_entrenado, tmp_path):
        model_file = tmp_path / "model.joblib"
        save_model(modelo_entrenado, model_file)
        resultado = predict(model_file, [5.1, 3.5, 1.4, 0.2])
        assert isinstance(resultado, str)
