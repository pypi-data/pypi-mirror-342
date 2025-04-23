# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
import grpc
import pytest
from luminarycloud.exceptions import AuthenticationError, SDKException


def test_sdk_exception():
    # Test basic exception creation and message
    message = "Test error message"
    exc = SDKException(message)
    assert str(exc) == message
    assert repr(exc) == "SDKException: Test error message"
    assert exc._render_traceback_() == ["Test error message"]


def test_authentication_exception():
    # Test with custom message
    custom_message = "Custom auth error"
    exc = AuthenticationError(custom_message, grpc.StatusCode.UNAUTHENTICATED)
    assert str(exc) == custom_message
    assert repr(exc) == f"AuthenticationError: {custom_message}"
    assert exc._render_traceback_() == [
        "Authentication failed; please check your credentials and try again."
    ]


def test_exception_raising():
    # Test that exceptions are raised correctly
    with pytest.raises(SDKException) as exc_info:
        raise SDKException("Test error")
    assert str(exc_info.value) == "Test error"

    with pytest.raises(AuthenticationError) as exc_info:
        raise AuthenticationError("Authentication failed", grpc.StatusCode.UNAUTHENTICATED)
    assert str(exc_info.value) == "Authentication failed"
