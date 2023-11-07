import os
import pytest
import docker
from image_refresher import main


def test_get_image_id_success(monkeypatch):
    class mock:
        def get(name):
            cont = mock()
            cont.id = '1234'
            return cont
    
    mydocker = mock()
    mydocker.images = mock

    monkeypatch.setattr(main, 'client', mydocker)
    result = main.get_image_id('exists')
    assert result == '1234'

def test_get_image_id_fail(monkeypatch):
    class mock:
        def get(name):
            raise docker.errors.APIError('')
    
    mydocker = mock()
    mydocker.images = mock

    monkeypatch.setattr(main, 'client', mydocker)
    result = main.get_image_id('none')
    assert not result

def test_refresh_new(monkeypatch):
    called = []
    class mock:
        def get(name):
            assert name == 'new'
            nonlocal called
            called.append('get')

            raise docker.errors.APIError('')

        def pull(name):
            assert name == 'new'
            nonlocal called
            called.append('pull')

            cont = mock()
            cont.id = '1234'
            return cont
    
    mydocker = mock()
    mydocker.images = mock

    monkeypatch.setattr(main, 'client', mydocker)
    main.refresh('new')
    assert called == ['get', 'pull']

def test_refresh_needed(monkeypatch):
    called = []
    class mock:
        def get(name):
            assert name == 'update'
            nonlocal called
            called.append('get')

            cont = mock()
            cont.id = '1234'
            return cont

        def pull(name):
            assert name == 'update'
            nonlocal called
            called.append('pull')

            cont = mock()
            cont.id = '5678'
            return cont

        def remove(id):
            assert id == '1234'
            nonlocal called
            called.append('remove')
    
    mydocker = mock()
    mydocker.images = mock

    monkeypatch.setattr(main, 'client', mydocker)
    main.refresh('update')
    assert called == ['get', 'pull', 'remove']

def test_refresh_not_needed(monkeypatch):
    called = []
    class mock:
        def get(name):
            assert name == 'same'
            nonlocal called
            called.append('get')

            cont = mock()
            cont.id = '1234'
            return cont

        def pull(name):
            assert name == 'same'
            nonlocal called
            called.append('pull')

            cont = mock()
            cont.id = '1234'
            return cont
    
    mydocker = mock()
    mydocker.images = mock

    monkeypatch.setattr(main, 'client', mydocker)
    main.refresh('same')
    assert called == ['get', 'pull']

def test_main_success(monkeypatch):
    called = []
    class mock:
        def add_job(refresh, trigger, name, args):
            assert name in ['foo', 'bar']
            assert len(args) == 1
            assert args[0] in ['foo', 'bar']

            nonlocal called
            called.append('add_job_' + name)

        def start():
            nonlocal called
            called.append('start')
    
    def mock_refresh(name):
        assert name in ['foo', 'bar']

    monkeypatch.setattr(main, 'scheduler', mock)
    monkeypatch.setattr(main, 'refresh', mock_refresh)

    os.environ['REFRESHER_IMAGE_1'] = 'foo'
    os.environ['REFRESHER_IMAGE_2'] = 'bar'
    main.main()
    assert called == ['add_job_foo', 'add_job_bar', 'start']
