# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud._auth import credentials_store
import tempfile


def test_credentials_store() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        store = credentials_store.CredentialsStore("foo", tmpdir)
        # Values start empty
        got = store.recall("foo")
        assert got is None, "unexpected value for empty key"
        # Should be able to set multiple values
        store.save("foo", "bar")
        store.save("aaa", "bbb")
        got = store.recall("foo")
        assert got == "bar", "value should be bar"
        got = store.recall("aaa")
        assert got == "bbb", "value should be bbb"

        # Different store should not see values.
        store2 = credentials_store.CredentialsStore("bar", tmpdir)
        got = store2.recall("foo")
        assert got is None, "unexpected value for empty key"

        # Second store should be able to work with the first.
        store3 = credentials_store.CredentialsStore("foo", tmpdir)
        got = store3.recall("foo")
        assert got == "bar", "value should be bar"
        store3.save("foo", None)
        got = store.recall("foo")
        assert got is None, "unexpected value for empty key"
        got = store3.recall("foo")
        assert got is None, "unexpected value for empty key"
