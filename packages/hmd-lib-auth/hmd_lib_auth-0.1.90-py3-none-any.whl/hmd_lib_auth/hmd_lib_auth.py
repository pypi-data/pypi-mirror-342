from typing import Optional
from urllib.parse import urlparse
import os
import requests
import boto3
from boto3 import Session
from aws_requests_auth.aws_auth import AWSRequestsAuth
from hmd_cli_tools.hmd_cli_tools import get_cloud_region, get_secret, get_session


def api_iam_auth(
    api_host: str, api_hmd_region: str = None, profile: str = None
) -> Optional[AWSRequestsAuth]:
    if api_hmd_region:
        api_region = get_cloud_region(api_hmd_region)
    else:
        api_region = os.environ.get("AWS_DEFAULT_REGION")
    profile = profile or os.environ.get("AWS_PROFILE")
    access_key = None
    secret_key = None
    session_token = None

    if profile:
        session = boto3.session.Session(region_name=api_region, profile_name=profile)
        credentials = session.get_credentials()
        access_key = credentials.access_key
        secret_key = credentials.secret_key
    elif os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get(
        "AWS_SECRET_ACCESS_KEY"
    ):
        access_key = os.environ["AWS_ACCESS_KEY_ID"]
        secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        session_token = os.environ.get("AWS_SESSION_TOKEN")

    if access_key and secret_key and api_region:
        return AWSRequestsAuth(
            aws_access_key=access_key,
            aws_secret_access_key=secret_key,
            aws_token=session_token,
            aws_host=urlparse(api_host).netloc,
            aws_region=api_region,
            aws_service="execute-api",
        )
    else:
        return None


def trust_clients_param_name(standard_name: str) -> str:
    return f"{standard_name}-trusted-clients"


def okta_service_account_token_by_secret_name(
    secret_name: str, session: Session = None
) -> str:
    session = session or get_session()
    client_secrets = get_secret((session or get_session()), secret_name, use_cache=True)

    return okta_service_account_token(
        client_secrets["client_id"], client_secrets["client_secret"], session
    )


def okta_service_account_token_by_service(
    instance_name: str, repo_name: str, deployment_id: str, session: Session = None
):
    session = session or get_session()

    return okta_service_account_token_by_secret_name(
        f"okta-{instance_name}-{repo_name}-{deployment_id}", session
    )


def okta_service_account_token(
    client_id: str,
    client_secret: str,
    session: Session = None,
    okta_host_url: str = None,
) -> str:
    """
    Service Accounts can provide their Okta
    Client ID and Client Secret and generate an Authorization Token
    """

    if not okta_host_url:
        session = session or get_session()
        okta_secrets = get_secret(session, "okta", use_cache=True)
        okta_host_url = okta_secrets["services_issuer"]

    okta_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "service",
        "grant_type": "client_credentials",
    }

    response = requests.post(f"{okta_host_url}/v1/token", data=okta_data)
    if response.status_code != 200:
        raise Exception("Unauthorized")
    else:
        resp_json = response.json()
        return resp_json["access_token"]
