import click
from flask import Flask, jsonify, request
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider

from ._utils import get_result

app = Flask(__name__)

provider = EthereumTesterProvider()
w3 = Web3(provider)


@app.route("/", methods=["POST"])
def rpc():
    """
    Handles JSON-RPC requests.
    Expects a JSON payload with the following structure:
    {
        "jsonrpc": "2.0",
        "method": "<method_name>",
        "params": [<param1>, <param2>, ...],
        "id": <request_id>
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        method = data["method"]
        params = data.get("params", [])
        request_id = data.get("id", 1)

        response = w3.manager.request_blocking(method, params)
        rpc_response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": get_result(response),
        }
        return jsonify(rpc_response)
    except Exception as e:
        return jsonify(
            {
                "jsonrpc": "2.0",
                "id": data.get("id", 1),
                "error": {"code": -32603, "message": str(e)},
            }
        )


@click.command()
@click.option("--port", default=8545, help="Port to run the server on")
@click.option("--debug", is_flag=True, help="Run the server in debug mode")
def main(port: int, debug: bool) -> None:
    """
    Main entry point for the RPC server.

    :param port: Port to run the server on
    :param debug: Run the server in debug mode
    """

    # List accounts
    accounts_response = w3.eth.accounts
    click.secho("Accounts:", fg="yellow")
    for account in accounts_response:
        click.secho(account, fg="yellow")
    click.secho("\n", fg="yellow")

    kwargs = {"debug": debug}
    app.run(
        host="0.0.0.0",
        port=port,
        **kwargs,
    )
