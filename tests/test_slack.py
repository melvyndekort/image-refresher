import os
import pytest
import importlib


def test_no_webhook_url():
    from image_refresher import slack
    importlib.reload(slack)
    assert not slack.webhook


def test_webhook_url():
    os.environ['REFRESHER_SLACK_WEBHOOK_URL'] = 'foobar'
    from image_refresher import slack
    importlib.reload(slack)
    assert slack.webhook


def test_notify_success(monkeypatch):
    from image_refresher import slack

    called = False
    class response:
        status_code = 200
        body = 'ok'

    class mock:
        def send(text):
            nonlocal called
            called = True
            assert text == 'foobar'
            return response()

    class logging:
        def error(message, *args):
            assert False

    monkeypatch.setattr(slack, 'webhook', mock)
    monkeypatch.setattr(slack, 'logging', logging)

    slack.notify('foobar')
    assert called

def test_notify_fail(monkeypatch):
    from image_refresher import slack

    called = []
    class response:
        status_code = 404
        body = 'fail'

    class mock:
        def send(text):
            nonlocal called
            called.append('send')
            assert text == 'foobar'
            return response()

    class logging:
        def error(message, *args):
            nonlocal called
            called.append('error')
            assert 'fail' in args

    monkeypatch.setattr(slack, 'webhook', mock)
    monkeypatch.setattr(slack, 'logging', logging)

    slack.notify('foobar')
    assert called == ['send', 'error']
