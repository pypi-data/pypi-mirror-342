# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import threading

import pytest
from luminarycloud._client import Client, get_default_client
from luminarycloud._client.client import (
    _get_primary_domain_for_apiserver_domain,
    _is_internal_domain_for_lc_apiserver,
)
from luminarycloud._client.tracing import (
    _get_collector_endpoint,
)


@pytest.mark.parametrize(
    "input, expected",
    [
        ("apis.luminarycloud.com", False),
        ("apis.test0.int.luminarycloud.com", True),
        ("apis.main.int.luminarycloud.com", True),
        ("localhost", False),
        ("127.0.0.1", False),
        ("192.168.0.1", False),
        ("172.17.42.1", False),
        ("apis.e2-test.int.luminarycloud.com", True),
        ("apis.r-test.int.luminarycloud.com", True),
        ("apis.pr-test.int.luminarycloud.com", True),
        ("apis.bctest.int.luminarycloud.com", True),
        ("apis-r-pull.int.luminarycloud.com", True),
        ("apis-pr-test.int.luminarycloud.com", True),
    ],
)
def test_is_internal_domain_for_lc_apiserver(input: str, expected: bool) -> None:
    assert _is_internal_domain_for_lc_apiserver(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("apis.luminarycloud.com", "app.luminarycloud.com"),
        ("apis.test0.int.luminarycloud.com", "test0.int.luminarycloud.com"),
        ("apis.main.int.luminarycloud.com", "main.int.luminarycloud.com"),
        ("apis.itar-main.int.luminarycloud.com", "itar-main.int.luminarycloud.com"),
        ("localhost", None),
        ("127.0.0.1", None),
        ("192.168.0.1", None),
        ("172.17.42.1", None),
        ("apis.e2-test.int.luminarycloud.com", "e2-test.int.luminarycloud.com"),
        ("apis.r-test.int.luminarycloud.com", "r-test.int.luminarycloud.com"),
        ("apis.pr-test.int.luminarycloud.com", "pr-test.int.luminarycloud.com"),
        ("apis.bctest.int.luminarycloud.com", "bctest.int.luminarycloud.com"),
        ("apis-r-pull.int.luminarycloud.com", "r-pull.int.luminarycloud.com"),
    ],
)
def test_get_primary_domain_for_apiserver_domain(input: str, expected: str) -> None:
    assert _get_primary_domain_for_apiserver_domain(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("apis.luminarycloud.com", "https://app.luminarycloud.com/v1/traces"),
        ("apis.test0.int.luminarycloud.com", "https://test0.int.luminarycloud.com/v1/traces"),
        ("apis.main.int.luminarycloud.com", "https://main.int.luminarycloud.com/v1/traces"),
        ("apis.e2-test.int.luminarycloud.com", "https://e2-test.int.luminarycloud.com/v1/traces"),
        ("apis.r-test.int.luminarycloud.com", "https://r-test.int.luminarycloud.com/v1/traces"),
        ("apis.pr-test.int.luminarycloud.com", "https://pr-test.int.luminarycloud.com/v1/traces"),
        ("apis.bctest.int.luminarycloud.com", "https://bctest.int.luminarycloud.com/v1/traces"),
        ("apis-r-pull.int.luminarycloud.com", "https://r-pull.int.luminarycloud.com/v1/traces"),
    ],
)
def test_get_collector_endpoint_for_apiserver_domain(input: str, expected: str) -> None:
    assert _get_collector_endpoint(_get_primary_domain_for_apiserver_domain(input)) == expected


def test_default_client_multithreading(reraise) -> None:
    b = threading.Barrier(2)

    client1 = Client(target="foo")
    client2 = Client(target="bar")

    @reraise.wrap
    def thread1():
        original_client = get_default_client()
        with client1:
            assert get_default_client()._target == client1._target
            b.wait()
            assert get_default_client()._target == client1._target
        assert get_default_client()._target == original_client._target

    @reraise.wrap
    def thread2():
        original_client = get_default_client()
        with client2:
            assert get_default_client()._target == client2._target
            b.wait()
            assert get_default_client()._target == client2._target
        assert get_default_client()._target == original_client._target

    t = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)
    t.start()
    t2.start()
    t.join()
    t2.join()
