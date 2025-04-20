from collections.abc import Sequence
from pathlib import Path

import pandas as pd
import pystac
import pytest

from stac_generator.core.base.utils import read_source_config
from stac_generator.core.vector.generator import VectorGenerator
from stac_generator.exceptions import StacConfigException

CONFIG_PATH = Path("tests/files/unit_tests/vectors/configs")


def load_items(file: str) -> Sequence[pystac.Item]:
    config_path = CONFIG_PATH / file
    config = read_source_config(str(config_path))
    generator = VectorGenerator(config)
    return generator.create_items()


def load_item(file: str) -> pystac.Item:
    return load_items(file)[0]


def test_given_invalid_wrong_layer_expects_raises() -> None:
    with pytest.raises(Exception):
        load_items("invalid_wrong_layer.json")


def test_given_invalid_column_info_expects_raises() -> None:
    with pytest.raises(StacConfigException):
        load_items("invalid_column_info.json")


def test_given_no_column_info_expects_no_value_in_property() -> None:
    item = load_item("no_column_info.json")
    assert "column_info" not in item.properties["stac_generator"]


def test_given_column_info_expects_column_info_in_property() -> None:
    item = load_item("with_column_info.json")
    assert "column_info" in item.properties["stac_generator"]
    assert item.properties["stac_generator"]["column_info"] != []


def test_given_with_epsg_expects_epsg_in_property() -> None:
    item = load_item("with_epsg.json")
    assert "proj:code" in item.properties
    assert item.properties["proj:code"] == "EPSG:1168"


def test_given_layers_info_expects_multiple_layers() -> None:
    items = load_items("with_layer.json")
    assert len(items) == 2
    assert items[0].id == "Sunbury"
    assert items[1].id == "Werribee"


def test_given_join_file_invalid_config_left_on_undescribed_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_left_on_undescribed.json")


def test_given_join_file_invalid_no_join_column_info_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_no_join_column_info.json")


def test_given_join_file_invalid_config_no_left_on_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_no_left_on.json")


def test_given_join_file_invalid_config_no_right_on_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_no_right_on.json")


def test_given_join_file_invalid_config_right_on_undescribed_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_right_on_undescribed.json")


def test_given_join_file_invalid_wrong_join_column_info_expects_throw() -> None:
    with pytest.raises(StacConfigException):
        load_item("join_invalid_config_wrong_join_column_info.json")


def test_given_join_file_invalid_wrong_join_date_column_expects_throw() -> None:
    with pytest.raises(StacConfigException):
        load_item("join_invalid_config_wrong_join_date_column.json")


def test_given_join_file_invalid_wrong_left_on_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_wrong_left_on.json")


def test_given_join_file_invalid_wrong_right_on_expects_throw() -> None:
    with pytest.raises(ValueError):
        load_item("join_invalid_config_wrong_right_on.json")


def test_given_join_with_date_expects_correct_start_end_datetime() -> None:
    item = load_item("join_with_date.json")
    assert "column_info" in item.properties["stac_generator"]
    assert item.properties["stac_generator"]["column_info"] == [
        {"name": "Suburb_Name", "description": "Suburb_Name"}
    ]
    assert "join_config" in item.properties["stac_generator"]
    assert item.properties["stac_generator"]["join_config"]["column_info"] == [
        {"name": "Area", "description": "Area Name"},
        {"name": "Sell_Price", "description": "Median Sales Price in 2025"},
        {"name": "Rent_Price", "description": "Median Rental Price in 2025"},
        {
            "name": "Sell/Rent",
            "description": "Ratio of Sales Price (in $1000) over Rental Price (in $)",
        },
    ]
    assert (
        item.properties["stac_generator"]["join_config"]["file"]
        == "tests/files/unit_tests/vectors/price.csv"
    )
    assert item.properties["stac_generator"]["join_config"]["right_on"] == "Area"
    assert item.properties["stac_generator"]["join_config"]["left_on"] == "Suburb_Name"
    assert item.properties["stac_generator"]["join_config"]["date_column"] == "Date"
    assert item.properties["start_datetime"] == "2020-01-01T00:00:00Z"
    assert item.properties["end_datetime"] == "2025-01-01T00:00:00Z"


def test_given_join_with_date_no_tzexpects_correct_start_end_datetime() -> None:
    item = load_item("join_with_date_no_tz.json")
    assert "column_info" in item.properties["stac_generator"]
    assert item.properties["stac_generator"]["column_info"] == [
        {"name": "Suburb_Name", "description": "Suburb_Name"}
    ]
    assert "join_config" in item.properties["stac_generator"]
    assert item.properties["stac_generator"]["join_config"]["column_info"] == [
        {"name": "Area", "description": "Area Name"},
        {"name": "Sell_Price", "description": "Median Sales Price in 2025"},
        {"name": "Rent_Price", "description": "Median Rental Price in 2025"},
        {
            "name": "Sell/Rent",
            "description": "Ratio of Sales Price (in $1000) over Rental Price (in $)",
        },
    ]
    assert (
        item.properties["stac_generator"]["join_config"]["file"]
        == "tests/files/unit_tests/vectors/price_no_tz.csv"
    )
    assert item.properties["stac_generator"]["join_config"]["right_on"] == "Area"
    assert item.properties["stac_generator"]["join_config"]["left_on"] == "Suburb_Name"
    assert item.properties["stac_generator"]["join_config"]["date_column"] == "Date"
    assert item.properties["start_datetime"] == "2020-01-01T00:00:00Z"
    assert item.properties["end_datetime"] == "2025-01-01T00:00:00Z"


def test_given_join_with_no_date_expects_same_start_end_datetime() -> None:
    item = load_item("join_no_date.json")
    assert item.properties["stac_generator"]["column_info"] == [
        {"name": "Suburb_Name", "description": "Suburb_Name"}
    ]
    assert item.properties["stac_generator"]["join_config"]["column_info"] == [
        {"name": "Area", "description": "Area name"},
        {"name": "Distance", "description": "Driving Distance to CBD in km"},
        {
            "name": "Public_Transport",
            "description": "Time taken to reach CBD by public transport in minutes",
        },
        {"name": "Drive", "description": "Time taken to reach CBD by driving in minutes"},
        {"name": "Growth", "description": "Average 5 year growth in percentage in 2025"},
        {"name": "Yield", "description": "Average rental yield in 2025"},
    ]
    assert (
        item.properties["stac_generator"]["join_config"]["file"]
        == "tests/files/unit_tests/vectors/distance.csv"
    )
    assert item.properties["stac_generator"]["join_config"]["right_on"] == "Area"
    assert item.properties["stac_generator"]["join_config"]["left_on"] == "Suburb_Name"
    assert item.properties["start_datetime"] == item.properties["end_datetime"]
    assert item.datetime == pd.Timestamp(item.properties["start_datetime"])
