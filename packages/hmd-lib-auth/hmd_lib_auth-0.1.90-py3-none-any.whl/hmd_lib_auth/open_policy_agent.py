import os
import requests
from typing import List, Tuple
from hmd_cli_tools.hmd_cli_tools import get_neuronsphere_domain


def validate_authorization(
    service: str,
    rules: List[str],
    input_dict: dict,
    opa_server: str = os.environ.get("OPA_SERVER"),
    token: str = os.environ.get("OPA_TOKEN"),
) -> Tuple[bool, dict]:
    """
    queries OPA to determine whether the input satisfies the given policy rules
    """

    if not opa_server:
        opa_server = f"https://base-opa.{get_neuronsphere_domain(os.environ['HMD_CUSTOMER_CODE'], os.environ['HMD_ENVIRONMENT'])}"

    headers = None
    if token:
        headers = {"Authorization": f"Bearer {token}"}

    # TODO: explore using Query API instead
    rsp = requests.post(
        f"{opa_server}/v1/data/base/{service}/main",
        json=input_dict,
        headers=headers,
    )

    policy = {
        rule_name: rule_value
        for (rule_name, rule_value) in rsp.json().get("result", {}).items()
        if rule_name in rules
    }

    # TODO: optimize
    #
    # the intent is that we want to verify that each rule required is allowed
    # for the user. If it isn't, we return False so the caller knows to reject.
    # We want to limit policy decisions being made by the caller.
    authorized = True
    for rule in rules:
        if policy.get(rule, False) == False:
            authorized = False
            break

    return authorized, policy
