import pytest

from explorer_app.logic.etl_utils import ETLUtils


def load_json(filename):
    import json
    with open(filename) as f:
        return json.load(f)


@pytest.fixture()
def people(request):
    request.cls.people = (load_json(filename='explorer_app/tests/logic/people.json'),)


@pytest.fixture()
def people_table(request, people):
    request.cls.people_table = ETLUtils.combine(gen=request.cls.people)


@pytest.fixture()
def planets(request):
    request.cls.planets = (load_json(filename='explorer_app/tests/logic/planets.json'),)
