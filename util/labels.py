from enum import StrEnum

import allure
import pytest


class CustomLabels(StrEnum):
    LAYER = "layer"
    COMPONENT = "component"


class TestLayers(StrEnum):
    API = "api"
    UI = "ui"


def api(fn):
    fn = pytest.mark.api(fn)
    fn = allure.label(CustomLabels.LAYER, TestLayers.API)(fn)
    return fn


def ui(fn):
    fn = pytest.mark.ui(fn)
    fn = allure.label(CustomLabels.LAYER, TestLayers.UI)(fn)
    return fn
