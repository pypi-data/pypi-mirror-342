import pytest
import io
from richtqdm import RichTqdm, in_notebook, UnitsColumn
from rich.text import Text


# Dummy task object for UnitsColumn tests
class DummyTask:
    def __init__(self, completed, total):
        self.completed = completed
        self.total = total


def test_units_column_default():
    col = UnitsColumn()
    task = DummyTask(3, 10)
    text = col.render(task)
    assert isinstance(text, Text)
    assert text.plain == "3/10 it"


def test_units_column_custom_unit():
    col = UnitsColumn(unit="files")
    task = DummyTask(5, 20)
    text = col.render(task)
    assert text.plain == "5/20 files"


def test_in_notebook_returns_bool():
    result = in_notebook()
    assert isinstance(result, bool)


def test_len_and_iterate_disable():
    data = [1, 2, 3]
    p = RichTqdm(data, disable=True)
    assert len(p) == len(data)
    assert list(p) == data


def test_len_no_total_raises():
    gen = (i for i in range(2))
    p = RichTqdm(gen, disable=True)
    with pytest.raises(TypeError):
        _ = len(p)


def test_context_manager_and_update_sets_task_and_clears():
    data = [0, 1, 2]
    p = RichTqdm(data, disable=False)
    with p as bar:
        # task_id should be set inside context
        assert bar.task_id is not None
        # advance progress
        bar.update(advance=2)
        # change description
        bar.set_description("testing")
        # writing should not raise
        bar.write("hello world")
    # after exit, task_id should be cleared
    assert p.task_id is None


def test_close_stops_progress():
    p = RichTqdm([1], disable=False)
    # manually enter progress context
    p.__enter__()
    assert p.progress is not None
    p.close()
    assert p.progress is None
    assert p.task_id is None
