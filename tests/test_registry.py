import pandas as pd

from registry import TransformerRegistry


def test_registry_initialization():
    registry = TransformerRegistry()
    assert registry._registry == {}


def test_register_transformer():
    registry = TransformerRegistry()

    @registry.register("test_transform")
    def test_transform(df: pd.DataFrame) -> pd.DataFrame:
        return df

    assert "test_transform" in registry._registry
    assert registry.get("test_transform") == test_transform


def test_get_nonexistent_transformer():
    registry = TransformerRegistry()
    assert registry.get("nonexistent") is None


def test_register_multiple_transformers():
    registry = TransformerRegistry()

    @registry.register("transform1")
    def transform1(df: pd.DataFrame) -> pd.DataFrame:
        return df

    @registry.register("transform2")
    def transform2(df: pd.DataFrame) -> pd.DataFrame:
        return df

    assert len(registry._registry) == 2
    assert "transform1" in registry._registry
    assert "transform2" in registry._registry
