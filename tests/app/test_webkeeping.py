# -*- encoding: utf-8 -*-
"""
tests.app.test_webkeeping module

"""
import asyncio

import pytest

from keri.app.keeping import Manager
from keri.app.webkeeping import WebKeeper
from keri.core import Salter


class FakeStorageHandle:
    """Async storage handle with local writes and explicit sync commit."""

    def __init__(self, backend, namespace):
        self.backend = backend
        self.namespace = namespace
        self.local = dict(self.backend.persisted.get(namespace, {}))

    def get(self, key, default=None):
        return self.local.get(key, default)

    def __getitem__(self, key):
        return self.local[key]

    def __setitem__(self, key, value):
        self.local[key] = value

    async def sync(self):
        self.backend.persisted[self.namespace] = dict(self.local)


class FakeStorageBackend:
    """Minimal async opener that mimics PyScript storage commit semantics."""

    def __init__(self):
        self.persisted = {}

    async def open(self, namespace):
        return FakeStorageHandle(self, namespace)


def test_webkeeper_configuration():
    with pytest.raises(RuntimeError):
        WebKeeper(reopen=True)

    with pytest.raises(TypeError):
        WebKeeper(unknown=True)


def test_webkeeper_manager_persistence():
    async def run():
        backend = FakeStorageBackend()
        keeper = WebKeeper(name="manager", storageOpener=backend.open)
        await keeper.reopen(clear=True)

        raw = b"0123456789abcdef"
        salt = Salter(raw=raw).qb64
        manager = Manager(ks=keeper, salt=salt)
        verfers, _ = manager.incept(salt=salt, temp=True)
        pre = verfers[0].qb64
        signature = manager.sign(ser=b"persisted", verfers=verfers)[0].qb64

        await keeper.aclose()

        keeper = WebKeeper(name="manager", storageOpener=backend.open)
        await keeper.reopen()
        assert keeper.prms.get(pre) is not None
        assert keeper.sits.get(pre) is not None

        manager = Manager(ks=keeper)
        verfers = [keeper.pris.get(verfers[0].qb64b).verfer]
        assert manager.sign(ser=b"persisted", verfers=verfers)[0].qb64 == signature

        await keeper.aclose(clear=True)

    asyncio.run(run())


def test_webkeeper_reopen_flushes_pending_state():
    async def run():
        backend = FakeStorageBackend()
        keeper = WebKeeper(name="reopen", storageOpener=backend.open)
        await keeper.reopen(clear=True)
        keeper.gbls.pin("item", "value")

        await keeper.reopen()
        assert keeper.gbls.get("item") == "value"

        await keeper.aclose(clear=True)

    asyncio.run(run())


def test_webkeeper_sync_close_without_event_loop():
    backend = FakeStorageBackend()
    keeper = WebKeeper(name="sync-close", storageOpener=backend.open)
    asyncio.run(keeper.reopen(clear=True))
    keeper.gbls.pin("item", "value")

    keeper.close()
    assert not keeper.opened
    assert keeper.db is None

    asyncio.run(keeper.reopen())
    assert keeper.gbls.get("item") == "value"
    asyncio.run(keeper.aclose(clear=True))


def test_webkeeper_sync_close_rejects_running_event_loop():
    async def run():
        backend = FakeStorageBackend()
        keeper = WebKeeper(name="async-close", storageOpener=backend.open)
        await keeper.reopen(clear=True)
        keeper.gbls.pin("item", "value")

        with pytest.raises(RuntimeError, match="use await aclose"):
            keeper.close()

        assert keeper.opened
        assert keeper.gbls.get("item") == "value"

        await keeper.aclose()
        await keeper.reopen()
        assert keeper.gbls.get("item") == "value"
        await keeper.aclose(clear=True)

    asyncio.run(run())
