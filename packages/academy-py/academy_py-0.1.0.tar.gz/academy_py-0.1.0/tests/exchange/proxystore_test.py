from __future__ import annotations

import pickle
from collections.abc import Generator
from typing import Any
from typing import Callable

import pytest
from proxystore.connectors.local import LocalConnector
from proxystore.proxy import Proxy
from proxystore.store import Store
from proxystore.store.executor import ProxyAlways
from proxystore.store.executor import ProxyNever

from academy.exchange.http import HttpExchange
from academy.exchange.proxystore import ProxyStoreExchange
from academy.exchange.thread import ThreadExchange
from academy.message import ActionRequest
from academy.message import ActionResponse
from academy.message import PingRequest
from testing.behavior import EmptyBehavior


@pytest.fixture
def store() -> Generator[Store[LocalConnector], None, None]:
    with Store(
        'proxystore-exchange-store-fixture',
        LocalConnector(),
        cache_size=0,
        register=True,
    ) as store:
        yield store


@pytest.mark.parametrize(
    ('should_proxy', 'resolve_async'),
    (
        (ProxyNever(), False),
        (ProxyAlways(), True),
        (ProxyAlways(), False),
        (lambda x: isinstance(x, str), True),
    ),
)
def test_basic_usage(
    should_proxy: Callable[[Any], bool],
    resolve_async: bool,
    exchange: ThreadExchange,
    store: Store[LocalConnector],
) -> None:
    with ProxyStoreExchange(
        exchange,
        store,
        should_proxy,
        resolve_async=resolve_async,
    ) as wrapped_exchange:
        src = wrapped_exchange.register_client()
        dest = wrapped_exchange.register_agent(EmptyBehavior)
        mailbox = wrapped_exchange.get_mailbox(dest)
        assert mailbox.exchange is wrapped_exchange
        assert mailbox.mailbox_id == dest

        ping = PingRequest(src=src, dest=dest)
        exchange.send(dest, ping)
        assert mailbox.recv() == ping

        request = ActionRequest(
            src=src,
            dest=dest,
            action='test',
            args=('value', 123),
            kwargs={'foo': 'value', 'bar': 123},
        )
        wrapped_exchange.send(dest, request)

        received = mailbox.recv()
        assert isinstance(received, ActionRequest)
        assert request.tag == received.tag

        for old, new in zip(request.args, received.args):
            assert (type(new) is Proxy) == should_proxy(old)
            # will resolve the proxy if it exists
            assert old == new

        for name in request.kwargs:
            old, new = request.kwargs[name], received.kwargs[name]
            assert (type(new) is Proxy) == should_proxy(old)
            assert old == new

        response = request.response('result')
        wrapped_exchange.send(dest, response)

        received = mailbox.recv()
        assert isinstance(received, ActionResponse)
        assert response.tag == received.tag
        assert (type(received.result) is Proxy) == should_proxy(
            response.result,
        )
        assert response.result == received.result

        assert wrapped_exchange.discover(EmptyBehavior) == (dest,)

        mailbox.close()
        wrapped_exchange.terminate(src)
        wrapped_exchange.terminate(dest)


def test_serialize(
    http_exchange_server: tuple[str, int],
    store: Store[LocalConnector],
) -> None:
    host, port = http_exchange_server
    with HttpExchange(host, port) as base_exchange:
        with ProxyStoreExchange(
            base_exchange,
            store,
            should_proxy=ProxyAlways(),
        ) as exchange:
            dumped = pickle.dumps(exchange)
            reconstructed = pickle.loads(dumped)
            reconstructed.close()
