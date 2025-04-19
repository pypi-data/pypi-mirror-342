from typing import List

from web3 import Web3
from web3.datastructures import AttributeDict


def get_result(response):
    """
    Processes the response from the web3 call and converts any bytes
    values to hex strings.
    """
    if isinstance(response, List):
        return [get_result(item) for item in response]
    elif isinstance(response, AttributeDict):
        return dict_values_to_hex(response.__dict__)
    else:
        return response


def dict_values_to_hex(response_dict):
    """
    Converts all bytes values in a dictionary to hex strings.
    """
    for item in response_dict.items():
        if isinstance(item[1], bytes):
            response_dict[item[0]] = Web3.to_hex(item[1])

    return response_dict
