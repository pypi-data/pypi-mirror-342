import os

from src.swiftbarmenu import Notification


def test_notification_str():
    n = Notification('Title', 'Subtitle', 'Body', 'https://example.com')

    assert n.__str__() == "Notification(title='Title', subtitle='Subtitle', body='Body', href='https://example.com')"


def test_notification_repr():
    n = Notification('Title', 'Subtitle', 'Body', 'https://example.com')

    assert n.__repr__() == "Notification(title='Title', subtitle='Subtitle', body='Body', href='https://example.com')"


def test_notification_full(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title', 'Subtitle', 'Body', 'https://example.com').show()

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&subtitle=Subtitle&body=Body&href=https%3A%2F%2Fexample.com'")


def test_notification_full_silent(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title', 'Subtitle', 'Body', 'https://example.com').show(True)

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&subtitle=Subtitle&body=Body&href=https%3A%2F%2Fexample.com&silent=true'")


def test_notification_simple(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title').show()

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title'")


def test_notification_simple_silent(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title').show(True)

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&silent=true'")


def test_notification_with_body(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title', body="This is a notification content").show()

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&body=This%20is%20a%20notification%20content'")


def test_notification_with_body_silent(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title', body="This is a notification content").show(True)

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&body=This%20is%20a%20notification%20content&silent=true'")


def test_notification_with_link(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title', href="https://example.com").show()

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&href=https%3A%2F%2Fexample.com'")


def test_notification_with_link_silent(mocker, monkeypatch):
    # Arrange
    monkeypatch.setenv('SWIFTBAR_PLUGIN_PATH',
                       '/usr/local/swiftbar_plugins/test_plugin.1h.py')
    mocker.patch('os.system', return_value=None)

    # Act
    Notification('Title', href="https://example.com").show(True)

    # Assert
    os.system.assert_called_once_with(
        "open -g 'swiftbar://notify?plugin=test_plugin.1h.py&title=Title&href=https%3A%2F%2Fexample.com&silent=true'")
