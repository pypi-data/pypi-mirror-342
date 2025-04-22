import os
import asyncio
from json import loads
from boto3 import Session
from typing import Dict, List, Tuple
from hmd_cli_tools.hmd_cli_tools import (
    make_standard_name,
    get_session,
    get_secret,
    get_param_store_parameter,
)
from .hmd_lib_auth import trust_clients_param_name
from okta_jwt_verifier import AccessTokenVerifier, JWTUtils
from jose import jwt
from requests import request


def verify_token(event: Dict, session: Session = None, standard_name: str = ""):
    session = session or get_session()

    async def _verify_token():
        token = auth_token(event)
        issuer, audience = _get_issuer_and_audience(
            token, session, trusted_clients(standard_name, session)
        )

        auth0_domain = None
        try:
            auth0_domain = get_secret(
                session, "auth0-provider", secret_property="domain", use_cache=True
            )
        except Exception as e:
            print(e)
            pass

        if auth0_domain is not None and auth0_domain in issuer:
            jwks_json = request("GET", f"https://{auth0_domain}/.well-known/jwks.json")
            jwks = jwks_json.json()

            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }

            if rsa_key:
                if not isinstance(audience, list):
                    audience = [audience]
                for aud in audience:
                    try:
                        payload = jwt.decode(
                            token,
                            rsa_key,
                            algorithms="RS256",
                            audience=aud,
                            issuer=issuer,
                        )
                        break
                    except jwt.ExpiredSignatureError:
                        continue
                    except jwt.JWTClaimsError:
                        continue
                    except Exception as e:
                        print(e)
                        continue
                else:
                    raise Exception("Unauthorized")
            return

        try:
            jwt_verifier = AccessTokenVerifier(issuer, audience=audience)
            await jwt_verifier.verify(token)
            print("Token validated successfully.")
        except Exception as e:
            print(e)
            raise Exception("Unauthorized")

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_verify_token())


def get_claims(token: str):
    _, claims, _, _ = JWTUtils.parse_token(token)

    return claims


def _get_issuer_and_audience(
    token: str, session: Session, additional_clients: Dict
) -> Tuple[str, str]:
    okta_secrets = get_secret(session, "okta", use_cache=True)
    trusted_human_clients = []
    human_clients_param = os.environ.get("TRUSTED_HUMAN_CLIENTS")

    if human_clients_param is not None:
        clients_param = get_param_store_parameter(human_clients_param, session=session)
        human_clients = loads(clients_param)
        if "trusted_clients" in human_clients:
            trusted_human_clients.extend(human_clients["trusted_clients"])

    _, claims, _, _ = JWTUtils.parse_token(token)
    client_id = claims.get("cid", "")
    is_human_user = client_id in [
        okta_secrets.get("ns_client_id"),
        *trusted_human_clients,
    ]

    auth0_domain = None
    try:
        auth0_domain = get_secret(
            session, "auth0-provider", secret_property="domain", use_cache=True
        )
    except Exception as e:
        print(e)
        pass

    if auth0_domain is not None:
        return claims.get("iss", ""), claims.get("aud", "")

    audience = "api://neuronsphere"
    issuer = okta_secrets["services_issuer"]

    if is_human_user:
        issuer = okta_secrets["ns_issuer"]
    else:
        audience = f"{audience}-services"

        if additional_clients.get(client_id):
            issuer = additional_clients[client_id]["issuer"]

    return issuer, audience


def trusted_clients(standard_name: str, session: Session) -> Dict:
    try:
        return loads(
            get_param_store_parameter(trust_clients_param_name(standard_name), session)
        )
    except Exception as e:
        print(e)
        return {}


def is_token_expired(token: str) -> bool:
    try:
        JWTUtils.verify_expiration(token)
        return False
    except Exception as e:
        print(e)
        return True


def service_name(
    instance_name: str = "",
    repo_name: str = "",
    deployment_id: str = "",
    environment: str = "",
    hmd_region: str = "",
    customer_code: str = "",
    standard_name: str = "",
) -> str:
    return (
        standard_name
        or make_standard_name(
            instance_name,
            repo_name,
            deployment_id,
            environment,
            hmd_region,
            customer_code,
        )
    ).replace("-", "_")


def opa_input(event: Dict) -> Dict:
    input_dict = {
        "input": {
            "token": auth_token(event),
            "path": path(event),
            "method": http_method(event),
        }
    }

    if body(event):
        input_dict["request_body"] = body(event)

    return input_dict


def opa_bearer_token() -> str:
    bearer_token = os.environ.get("OPA_TOKEN")

    if not bearer_token:
        # we're assuming local users wishing to use OPA will
        # explicitly pass a token
        sess = get_session()
        bearer_token = get_secret(sess, "openpolicyagent", use_cache=True).get(
            "bearer_token"
        )

    return bearer_token


def path(event: Dict) -> List[str]:
    # in case the "pathParameters" is in the Dict with a value of None
    if event.get("pathParameters", "") is None:
        event["pathParameters"] = {}
    return (
        event.get("pathParameters", {}).get("proxy", "") or event.get("path", "")
    ).split("/")


def auth_token(event: Dict) -> str:
    headers = event.get("headers", {})
    response = headers.get("Authorization", "") or headers.get("authorization", "")
    # TODO: once all clients are using the standard, we might want to drop support
    if response.startswith("Bearer "):
        response = response.split(" ", 1)[-1]

    return response


def http_method(event: Dict) -> str:
    return event.get("requestContext", {}).get("httpMethod", "") or event.get(
        "httpMethod", ""
    )


def body(event: Dict) -> Dict:
    return event.get("body", {})
