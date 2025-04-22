from __future__ import annotations

import multiprocessing
import threading
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest

from academy.behavior import Behavior
from academy.behavior import loop
from academy.exception import BadEntityIdError
from academy.exchange import Exchange
from academy.exchange.http import HttpExchange
from academy.identifier import AgentId
from academy.launcher import Launcher
from academy.launcher.executor import ExecutorLauncher
from testing.behavior import SleepBehavior
from testing.constant import TEST_CONNECTION_TIMEOUT
from testing.constant import TEST_LOOP_SLEEP


def test_protocol() -> None:
    executor = ThreadPoolExecutor(max_workers=1)
    with ExecutorLauncher(executor) as launcher:
        assert isinstance(launcher, Launcher)
        assert isinstance(repr(launcher), str)
        assert isinstance(str(launcher), str)


def test_launch_agents_threads(exchange: Exchange) -> None:
    behavior = SleepBehavior(TEST_LOOP_SLEEP)
    executor = ThreadPoolExecutor(max_workers=2)
    with ExecutorLauncher(executor, close_exchange=False) as launcher:
        handle1 = launcher.launch(behavior, exchange).bind_as_client()
        handle2 = launcher.launch(behavior, exchange).bind_as_client()

        assert len(launcher.running()) == 2  # noqa: PLR2004

        time.sleep(5 * TEST_LOOP_SLEEP)

        handle1.shutdown()
        handle2.shutdown()

        handle1.close()
        handle2.close()

        launcher.wait(handle1.agent_id)
        launcher.wait(handle2.agent_id)

        assert len(launcher.running()) == 0


def test_launch_agents_processes(
    http_exchange_server: tuple[str, int],
) -> None:
    behavior = SleepBehavior(TEST_LOOP_SLEEP)
    context = multiprocessing.get_context('spawn')
    executor = ProcessPoolExecutor(max_workers=2, mp_context=context)
    host, port = http_exchange_server

    with HttpExchange(host, port) as exchange:
        with ExecutorLauncher(executor) as launcher:
            handle1 = launcher.launch(behavior, exchange).bind_as_client()
            handle2 = launcher.launch(behavior, exchange).bind_as_client()

            assert handle1.ping(timeout=TEST_CONNECTION_TIMEOUT) > 0
            assert handle2.ping(timeout=TEST_CONNECTION_TIMEOUT) > 0

            handle1.shutdown()
            handle2.shutdown()

            handle1.close()
            handle2.close()


def test_wait_bad_identifier(exchange: Exchange) -> None:
    executor = ThreadPoolExecutor(max_workers=1)
    with ExecutorLauncher(executor) as launcher:
        agent_id: AgentId[Any] = AgentId.new()

        with pytest.raises(BadEntityIdError):
            launcher.wait(agent_id)


def test_wait_timeout(exchange: Exchange) -> None:
    behavior = SleepBehavior(TEST_LOOP_SLEEP)
    executor = ThreadPoolExecutor(max_workers=1)
    with ExecutorLauncher(executor) as launcher:
        handle = launcher.launch(behavior, exchange).bind_as_client()

        with pytest.raises(TimeoutError):
            launcher.wait(handle.agent_id, timeout=TEST_LOOP_SLEEP)

        handle.shutdown()
        handle.close()


class FailOnStartupBehavior(Behavior):
    def __init__(self, max_errors: int | None = None) -> None:
        self.errors = 0
        self.max_errors = max_errors

    def on_setup(self) -> None:
        if self.max_errors is None or self.errors < self.max_errors:
            self.errors += 1
            raise RuntimeError('Agent startup failed')

    @loop
    def exit_after_startup(self, shutdown: threading.Event) -> None:
        shutdown.set()


def test_restart_on_error(exchange: Exchange) -> None:
    behavior = FailOnStartupBehavior(max_errors=2)
    # This test only works because we are using a ThreadPoolExecutor so
    # the state inside FailOnStartupBehavior is shared.
    executor = ThreadPoolExecutor(max_workers=1)
    with ExecutorLauncher(
        executor,
        close_exchange=False,
        max_restarts=3,
    ) as launcher:
        handle = launcher.launch(behavior, exchange).bind_as_client()
        launcher.wait(handle.agent_id)
        handle.close()
        assert behavior.errors == 2  # noqa: PLR2004


@pytest.mark.parametrize('ignore_error', (True, False))
def test_wait_ignore_agent_errors(
    ignore_error: bool,
    exchange: Exchange,
) -> None:
    behavior = FailOnStartupBehavior()
    executor = ThreadPoolExecutor(max_workers=1)
    launcher = ExecutorLauncher(executor, close_exchange=False)

    handle = launcher.launch(behavior, exchange).bind_as_client()
    if ignore_error:
        launcher.wait(handle.agent_id, ignore_error=ignore_error)
    else:
        with pytest.raises(RuntimeError, match='Agent startup failed'):
            launcher.wait(handle.agent_id, ignore_error=ignore_error)
    handle.close()

    with pytest.raises(RuntimeError, match='Agent startup failed'):
        launcher.close()
    executor.shutdown()
