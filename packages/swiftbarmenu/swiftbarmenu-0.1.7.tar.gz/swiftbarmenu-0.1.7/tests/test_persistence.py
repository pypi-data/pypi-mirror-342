import pickle

from src.swiftbarmenu import Persistence


def test_persistence_str():
    p = Persistence()

    assert p.__str__() == "Persistence(file_name='data', path='data.pkl')"


def test_persistence_repr():
    p = Persistence()

    assert p.__repr__() == "Persistence(file_name='data', path='data.pkl')"


def test_persistence_save(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    sample_data = {
        "name": "test",
        "data": {
            "data1": "test",
            "data2": "test"
        }
    }

    # Act
    p = Persistence()
    p.save(sample_data)

    # Assert
    with (plugin_data_p / "data.pkl").open('rb') as file:
        stored_data = pickle.load(file)

        assert stored_data == sample_data


def test_persistence_load(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    sample_data = {
        "name": "test 2",
        "data": "test",
    }

    with (plugin_data_p / "data.pkl").open('wb') as file:
        stored_data = pickle.dump(sample_data, file)

    # Act
    p = Persistence()
    stored_data = p.load()

    # Assert
    assert stored_data == sample_data


def test_persistence_load_nofile(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    # Act
    p = Persistence()
    stored_data = p.load()

    # Assert
    assert stored_data == {}


def test_persistence_clear(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    sample_data = {
        "data": "test",
    }

    p = Persistence()
    p.save(sample_data)

    assert (plugin_data_p / "data.pkl").exists()

    # Act
    p.clear()

    # Assert
    assert not (plugin_data_p / "data.pkl").exists()


def test_persistence_save_custom_name(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    sample_data = {
        "name": "test",
        "data": {
            "data1": "test",
            "data2": "test"
        }
    }

    # Act
    p = Persistence("test")
    p.save(sample_data)

    # Assert
    with (plugin_data_p / "test.pkl").open('rb') as file:
        stored_data = pickle.load(file)

        assert stored_data == sample_data


def test_persistence_load_custom_name(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    sample_data = {
        "name": "test 2",
        "data": "test",
    }

    with (plugin_data_p / "test.pkl").open('wb') as file:
        stored_data = pickle.dump(sample_data, file)

    # Act
    p = Persistence("test")
    stored_data = p.load()

    # Assert
    assert stored_data == sample_data


def test_persistence_load_custom_name_nofile(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    # Act
    p = Persistence("test")
    stored_data = p.load()

    # Assert
    assert stored_data == {}


def test_persistence_clear_custom_name(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    sample_data = {
        "data": "test",
    }

    p = Persistence("test")
    p.save(sample_data)

    assert (plugin_data_p / "test.pkl").exists()

    # Act
    p.clear()

    # Assert
    assert not (plugin_data_p / "test.pkl").exists()
