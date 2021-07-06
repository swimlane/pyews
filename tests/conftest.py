import os
import pytest

@pytest.fixture
def pyews_fixture():
    import pyews
    yield pyews

@pytest.fixture
def pyews_ews_interface():
    from pyews import EWS
    yield EWS
