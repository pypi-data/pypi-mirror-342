# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
"""
sdkutil.py contains helper functions that maybe useful when using the Luminary
Python SDK.

This code is not actually a part of the SDK; it is an internal utility library
to make things like connecting to preview environments easier.
"""

import ssl
import socket
import base64
import grpc
import luminarycloud as lc


def get_self_signed_ssl_certificate(host: str, port: int = 443) -> str:
    """
    We use self-signed certs for our test environments. Normally most languages and frameworks
    accommodate self signed certs via some flags. However python+grpc actively discourages
    use of self-signed certs. The only way to get around that is to fetch the certificate and
    define it as a root certificate.
    :param host: the host
    :param port: port
    :return: cert/PEM in string format.
    """
    # The following code fetches the certificate in bytes
    context = ssl._create_unverified_context()  # type: ignore
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert(True)
    assert cert, "No cert was found"

    # decode gives us line length of 76 ascii chars for base64.
    # Convert it to 64 ascii chars per line.
    der_base64 = base64.encodebytes(cert).decode("ascii").replace("\n", "")
    lines = []
    while der_base64:
        lines.append(der_base64[0:64])
        der_base64 = der_base64[64:]
    return "-----BEGIN CERTIFICATE-----\n" + "\n".join(lines) + "\n-----END CERTIFICATE-----"


def get_client_for_env(env_name: str) -> lc.Client:
    """
    Configures and returns a LC SDK client connected to the specified environment.

    :param env_name: any valid env name, e.g. prod, test0, main, itar-prod, etc. or any preview env name
    :return: luminarycloud.Client
    """
    if env_name == "prod":
        # default client will be for prod
        return lc.Client(
            target="apis.luminarycloud.com",
            # below params are kwargs to Auth0Client constructor
            domain="luminarycloud-prod.us.auth0.com",
            client_id="JTsXa4fbArSCl6i9xylUpwrwpovtkss1",
            audience="https://apis.luminarycloud.com",
        )
    elif env_name == "test0":
        return lc.Client(
            target="apis.test0.int.luminarycloud.com",
            # below params are kwargs to Auth0Client constructor
            domain="luminarycloud-staging.us.auth0.com",
            client_id="emcjuelZOrvwlmAqVgqrdchw2cyY58mN",
            audience="https://api-staging.luminarycloud.com",
        )
    else:
        target = "apis.main.int.luminarycloud.com"
        credentials = None
        if env_name != "main":
            # must be a preview env
            target = f"apis-{env_name}.int.luminarycloud.com"
            root_certs = get_self_signed_ssl_certificate(target).encode("utf-8")
            credentials = grpc.ssl_channel_credentials(root_certificates=root_certs)
        return lc.Client(
            target=target,
            channel_credentials=credentials,
            # below params are kwargs to Auth0Client constructor
            domain="luminarycloud-dev.us.auth0.com",
            client_id="mbM8OSEk5ShoU5iKfzUxSinKluPlxGQ9",
            audience="https://api-dev.luminarycloud.com",
        )
