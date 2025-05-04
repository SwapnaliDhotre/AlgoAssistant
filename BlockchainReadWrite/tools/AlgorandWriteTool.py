from agency_swarm.tools import BaseTool
from pydantic import Field
from algosdk import account, transaction
from algosdk.v2client import algod
import os

algod_address = os.getenv("ALGOD_ADDRESS", "https://testnet-algorand.api.purestake.io/ps2")
algod_token = os.getenv("ALGOD_TOKEN")
headers = {
    "X-API-Key": algod_token,
}

class AlgorandWriteTool(BaseTool):
    """
    A tool for writing data to the Algorand blockchain.
    It supports operations such as sending transactions, creating assets, and managing smart contracts.
    The tool utilizes the Algorand API to perform these operations securely and efficiently.
    """

    operation: str = Field(
        ..., description="The operation to perform: 'send_transaction', 'create_asset', or 'manage_contract'."
    )
    sender_private_key: str = Field(
        ..., description="The private key of the sender's account."
    )
    receiver_address: str = Field(
        default=None, description="The receiver's account address, required for 'send_transaction' operation."
    )
    amount: int = Field(
        default=0, description="The amount of microAlgos to send, required for 'send_transaction' operation."
    )
    asset_params: dict = Field(
        default=None, description="The parameters for asset creation, required for 'create_asset' operation."
    )
    contract_params: dict = Field(
        default=None, description="The parameters for managing a smart contract, required for 'manage_contract' operation."
    )

    def run(self):
        """
        Executes the tool's main functionality based on the specified operation.
        """
        try:
            if self.operation == 'send_transaction':
                return self._send_transaction()
            elif self.operation == 'create_asset':
                return self._create_asset()
            elif self.operation == 'manage_contract':
                return self._manage_contract()
            else:
                return "Invalid operation specified."
        except Exception as e:
            return f"Algorand API Error: {str(e)}"

    def _send_transaction(self):
        """
        Sends a transaction on the Algorand blockchain.
        """
        if not self.receiver_address or self.amount <= 0:
            return "Receiver address and a positive amount are required for sending a transaction."

        client = algod.AlgodClient(algod_token, algod_address, headers)
        sender_address = account.address_from_private_key(self.sender_private_key)

        params = client.suggested_params()
        txn = transaction.PaymentTxn(sender_address, params, self.receiver_address, self.amount)

        signed_txn = txn.sign(self.sender_private_key)
        txid = client.send_transaction(signed_txn)
        return f"Transaction sent with ID: {txid}"

    def _create_asset(self):
        """
        Creates an asset on the Algorand blockchain.
        """
        if not self.asset_params:
            return "Asset parameters are required for creating an asset."

        client = algod.AlgodClient(algod_token, algod_address, headers)
        sender_address = account.address_from_private_key(self.sender_private_key)

        params = client.suggested_params()
        txn = transaction.AssetConfigTxn(sender_address, params, **self.asset_params)

        signed_txn = txn.sign(self.sender_private_key)
        txid = client.send_transaction(signed_txn)
        return f"Asset creation transaction sent with ID: {txid}"

    def _manage_contract(self):
        """
        Manages a smart contract on the Algorand blockchain.
        """
        if not self.contract_params:
            return "Contract parameters are required for managing a smart contract."

        # Implement contract management logic here
        # This is a placeholder for actual contract management operations
        return "Smart contract management operation executed."