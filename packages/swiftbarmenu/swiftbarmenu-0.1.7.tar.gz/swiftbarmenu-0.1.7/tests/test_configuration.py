import os

from src.swiftbarmenu import Configuration


def test_configuration_str():
    p = Configuration()

    assert p.__str__() == "Configuration(path='config.ini')"


def test_configuration_repr():
    p = Configuration()

    assert p.__repr__() == "Configuration(path='config.ini')"


def test_configuration_persist_empty(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    # Act
    c = Configuration()
    c.persist()

    # Assert
    assert (plugin_data_p / 'config.ini').exists()


def test_configuration_set_str():
    # Act
    c = Configuration()
    c.set("test", "test")

    # Assert
    assert c.get("test") == "test"


def test_configuration_set_int():
    # Act
    c = Configuration()
    c.set("test", 1)

    # Assert
    assert c.get("test", type="int") == 1


def test_configuration_set_float():
    # Act
    c = Configuration()
    c.set("test", 2.3)

    # Assert
    assert c.get("test", type="float") == 2.3


def test_configuration_set_boolean():
    # Act
    c = Configuration()
    c.set("test", True)

    # Assert
    assert c.get("test", type="bool") is True


def test_configuration_set_multiple():
    # Act
    c = Configuration()
    c.set("test1", "test2").set("test2", 2).set(
        "test3", 3.4).set("test4", False)

    # Assert
    assert c.get("test1") == "test2"
    assert c.get("test2", type="int") == 2
    assert c.get("test3", type="float") == 3.4
    assert c.get("test4", type="bool") is False


def test_configuration_section():
    # Arrange
    c = Configuration()

    # Act
    s = c.section("Test")
    s.set("test", "test")

    # Assert
    assert s.get("test") == "test"


def test_configuration_section_multiple():
    # Arrange
    c = Configuration()

    # Act
    s1 = c.section("Test")
    s1.set("test", "section1")

    s2 = c.section("Test2")
    s2.set("test", "section2")

    # Assert
    assert s1.get("test") == "section1"
    assert s2.get("test") == "section2"


def test_configuration_section_set_str():
    # Arrange
    c = Configuration()

    # Act
    s = c.section("Test")
    s.set("test", "test")

    # Assert
    assert s.get("test") == "test"


def test_configuration_section_set_int():
    # Arrange
    c = Configuration()

    # Act
    s = c.section("Test")
    s.set("test", 1)

    # Assert
    assert s.get("test", type="int") == 1


def test_configuration_section_set_float():
    # Arrange
    c = Configuration()

    # Act
    s = c.section("Test")
    s.set("test", 2.3)

    # Assert
    assert s.get("test", type="float") == 2.3


def test_configuration_section_set_boolean():
    # Arrange
    c = Configuration()

    # Act
    s = c.section("Test")
    s.set("test", True)

    # Assert
    assert s.get("test", type="bool") is True


def test_configuration_section_set_multiple():
    # Arrange
    c = Configuration()

    # Act
    s = c.section("Test")
    s.set("test1", "test2").set("test2", 2).set(
        "test3", 3.4).set("test4", False)

    # Assert
    assert s.get("test1") == "test2"
    assert s.get("test2", type="int") == 2
    assert s.get("test3", type="float") == 3.4
    assert s.get("test4", type="bool") is False


def test_configuration_get_string():
    # Arrange
    c = Configuration()
    c.set("test", "value")

    # Act
    result = c.get("test")

    # Assert
    assert result == "value"


def test_configuration_get_int():
    # Arrange
    c = Configuration()
    c.set("test", 1)

    # Act
    result = c.get("test", type="int")

    # Assert
    assert result == 1


def test_configuration_get_float():
    # Arrange
    c = Configuration()
    c.set("test", 2.3)

    # Act
    result = c.get("test", type="float")

    # Assert
    assert result == 2.3


def test_configuration_get_boolean():
    # Arrange
    c = Configuration()
    c.set("test", True)

    # Act
    result = c.get("test", type="bool")

    # Assert
    assert result is True


def test_configuration_get_string_with_default():
    # Arrange
    c = Configuration()
    c.set("test", "value")

    # Act
    result = c.get("nonexistent", default="default_value")

    # Assert
    assert result == "default_value"


def test_configuration_get_int_with_default():
    # Arrange
    c = Configuration()
    c.set("test", 1)

    # Act
    result = c.get("nonexistent", type="int", default=42)

    # Assert
    assert result == 42


def test_configuration_get_float_with_default():
    # Arrange
    c = Configuration()
    c.set("test", 2.3)

    # Act
    result = c.get("nonexistent", type="float", default=3.14)

    # Assert
    assert result == 3.14


def test_configuration_get_boolean_with_default():
    # Arrange
    c = Configuration()
    c.set("test", True)

    # Act
    result = c.get("nonexistent", type="bool", default=False)

    # Assert
    assert result is False


def test_configuration_autoload(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    Configuration().set("test", "data2").persist()

    # Act
    c = Configuration()

    # Assert
    assert c.get("test") == "data2"


def test_configuration_load(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    Configuration().set("test", "data1").persist()

    # Act
    c = Configuration(auto_load=False)
    c.load()

    # Assert
    assert c.get("test") == "data1"


def test_configuration_load_notexists(monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    # Act
    c = Configuration(auto_load=False)
    c.load()

    # Assert
    assert c.get("test") is None


def test_configuration_open_editor_default(mocker, monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    mocker.patch('os.system', return_value=None)

    # Act
    c = Configuration()
    c.open_editor()

    # Assert
    os.system.assert_called_once_with(
        f"open -a 'TextEdit' '{str(plugin_data_p / 'config.ini')}'")


def test_configuration_open_editor_custom(mocker, monkeypatch, tmp_path):
    # Arrange
    plugin_data_p = tmp_path / "test.1h.py"
    plugin_data_p.mkdir()

    monkeypatch.setenv('SWIFTBAR_PLUGIN_DATA_PATH', plugin_data_p.as_posix())
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH', '/sbm/plugins/test.1h.py')

    mocker.patch('os.system', return_value=None)

    # Act
    c = Configuration()
    c.open_editor("Visual Studio Code")

    # Assert
    os.system.assert_called_once_with(
        f"open -a 'Visual Studio Code' '{str(plugin_data_p / 'config.ini')}'")
