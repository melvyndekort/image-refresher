import os
import pytest
import importlib


def test_no_ntfy_config():
    from image_refresher import ntfy
    importlib.reload(ntfy)
    assert not ntfy.NTFY_URL
    assert not ntfy.NTFY_TOKEN


def test_ntfy_config():
    os.environ['NTFY_URL'] = 'https://ntfy.example.com/topic'
    os.environ['NTFY_TOKEN'] = 'tk_abc123'
    from image_refresher import ntfy
    importlib.reload(ntfy)
    assert ntfy.NTFY_URL == 'https://ntfy.example.com/topic'
    assert ntfy.NTFY_TOKEN == 'tk_abc123'


def test_notify_success(monkeypatch):
    from image_refresher import ntfy

    called = False
    class response:
        status_code = 200

    def mock_post(url, data, headers):
        nonlocal called
        called = True
        assert url == 'https://ntfy.example.com/topic'
        assert data == 'test message'
        assert headers['Authorization'] == 'Bearer tk_abc123'
        return response()

    class logging:
        def error(message, *args):
            assert False

    monkeypatch.setattr(ntfy, 'NTFY_URL', 'https://ntfy.example.com/topic')
    monkeypatch.setattr(ntfy, 'NTFY_TOKEN', 'tk_abc123')
    monkeypatch.setattr(ntfy.requests, 'post', mock_post)
    monkeypatch.setattr(ntfy, 'logging', logging)

    ntfy.notify('test message')
    assert called


def test_notify_fail(monkeypatch):
    from image_refresher import ntfy

    called = []
    class response:
        status_code = 404

    def mock_post(url, data, headers):
        nonlocal called
        called.append('post')
        return response()

    class logging:
        def error(message, *args):
            nonlocal called
            called.append('error')
            assert '404' in str(args)

    monkeypatch.setattr(ntfy, 'NTFY_URL', 'https://ntfy.example.com/topic')
    monkeypatch.setattr(ntfy, 'NTFY_TOKEN', 'tk_abc123')
    monkeypatch.setattr(ntfy.requests, 'post', mock_post)
    monkeypatch.setattr(ntfy, 'logging', logging)

    ntfy.notify('test message')
    assert called == ['post', 'error']
