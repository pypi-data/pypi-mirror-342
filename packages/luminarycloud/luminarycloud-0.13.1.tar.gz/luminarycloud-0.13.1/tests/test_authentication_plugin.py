# Copyright 2023-2025 Luminary Cloud, Inc. All Rights Reserved.
import pytest
from unittest.mock import Mock, patch

import grpc
from luminarycloud._client.authentication_plugin import AuthenticationPlugin
from luminarycloud._auth import Auth0Client


# Test authentication plugin when using API key authentication
def test_authentication_plugin_with_api_key() -> None:
    """Test authentication plugin when using API key authentication"""
    auth0_client = Mock(spec=Auth0Client)
    api_key = "test-api-key-123"
    plugin = AuthenticationPlugin(auth0_client, api_key)

    context = Mock(spec=grpc.AuthMetadataContext)
    callback = Mock(spec=grpc.AuthMetadataPluginCallback)

    plugin(context, callback)

    # Should call callback with API key header
    callback.assert_called_once_with([("x-api-key", api_key)], None)
    # Should not try to fetch access token
    auth0_client.fetch_access_token.assert_not_called()


# Test authentication plugin when using bearer token authentication
def test_authentication_plugin_with_bearer_token() -> None:
    """Test authentication plugin when using bearer token authentication"""
    auth0_client = Mock(spec=Auth0Client)
    auth0_client.fetch_access_token.return_value = "test-token-xyz"
    plugin = AuthenticationPlugin(auth0_client)

    context = Mock(spec=grpc.AuthMetadataContext)
    callback = Mock(spec=grpc.AuthMetadataPluginCallback)

    plugin(context, callback)

    # Should call callback with bearer token header
    callback.assert_called_once_with([("authorization", "Bearer test-token-xyz")], None)
    # Should fetch access token
    auth0_client.fetch_access_token.assert_called_once()


# Test error handling
def test_authentication_plugin_error_handling() -> None:
    """Test authentication plugin error handling"""
    auth0_client = Mock(spec=Auth0Client)
    auth0_client.fetch_access_token.side_effect = Exception("Auth error")
    plugin = AuthenticationPlugin(auth0_client)

    context = Mock(spec=grpc.AuthMetadataContext)
    callback = Mock(spec=grpc.AuthMetadataPluginCallback)

    plugin(context, callback)

    # Should call callback with error
    callback.assert_called_once_with(None, auth0_client.fetch_access_token.side_effect)


# Test invalid API key and fallback to bearer token auth
def test_authentication_plugin_invalid_api_key() -> None:
    """Test authentication plugin with invalid API key"""
    auth0_client = Mock(spec=Auth0Client)
    auth0_client.fetch_access_token.return_value = "test-token-xyz"
    plugin = AuthenticationPlugin(auth0_client, api_key="")

    context = Mock(spec=grpc.AuthMetadataContext)
    callback = Mock(spec=grpc.AuthMetadataPluginCallback)

    plugin(context, callback)

    # Should fallback to bearer token auth
    callback.assert_called_once_with([("authorization", "Bearer test-token-xyz")], None)
