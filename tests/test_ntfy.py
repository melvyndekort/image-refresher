import os
import pytest
import importlib


def test_no_apprise_config():
    from image_refresher import ntfy
    importlib.reload(ntfy)
    assert not ntfy.APPRISE_URL
    assert not ntfy.APPRISE_TAG
    assert not ntfy.APPRISE_KEY


def test_apprise_config():
    os.environ['APPRISE_URL'] = 'https://apprise.example.com'
    os.environ['APPRISE_TAG'] = 'test'
    os.environ['APPRISE_KEY'] = 'mykey'
    from image_refresher import ntfy
    importlib.reload(ntfy)
    assert ntfy.APPRISE_URL == 'https://apprise.example.com'
    assert ntfy.APPRISE_TAG == 'test'
    assert ntfy.APPRISE_KEY == 'mykey'


def test_notify_success(monkeypatch):
    from image_refresher import ntfy

    called = False
    class response:
        status_code = 200

    def mock_post(url, json, timeout):
        nonlocal called
        called = True
        assert url == 'https://apprise.example.com/notify/mykey'
        assert json['body'] == 'test message'
        assert json['tag'] == 'test'
        assert timeout == 10
        return response()

    monkeypatch.setattr(ntfy, 'APPRISE_URL', 'https://apprise.example.com')
    monkeypatch.setattr(ntfy, 'APPRISE_TAG', 'test')
    monkeypatch.setattr(ntfy, 'APPRISE_KEY', 'mykey')
    monkeypatch.setattr(ntfy.requests, 'post', mock_post)

    ntfy.notify('test message')
    assert called


def test_notify_fail(monkeypatch):
    from image_refresher import ntfy

    called = []
    class response:
        status_code = 404

    def mock_post(url, json, timeout):
        nonlocal called
        called.append('post')
        return response()

    class logger:
        def error(message, *args):
            nonlocal called
            called.append('error')
            assert '404' in str(args)

    monkeypatch.setattr(ntfy, 'APPRISE_URL', 'https://apprise.example.com')
    monkeypatch.setattr(ntfy, 'APPRISE_TAG', 'test')
    monkeypatch.setattr(ntfy, 'APPRISE_KEY', 'mykey')
    monkeypatch.setattr(ntfy.requests, 'post', mock_post)
    monkeypatch.setattr(ntfy, 'logger', logger)

    ntfy.notify('test message')
    assert called == ['post', 'error']
