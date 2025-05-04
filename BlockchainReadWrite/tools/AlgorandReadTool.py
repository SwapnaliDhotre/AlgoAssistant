from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

algorand_api_key = os.getenv("ALGORAND_API_KEY")
algorand_api_url = os.getenv("ALGORAND_API_URL", "https://api.algoexplorer.io")

class AlgorandReadTool(BaseTool):
    """
    A tool for reading data from the Algorand blockchain.
    It supports operations such as retrieving account information, transaction details, and asset information.
    The tool utilizes the Algorand API to fetch the required data.
    """

    operation: str = Field(
        ..., description="The operation to perform: 'account_info', 'transaction_details', or 'asset_info'."
    )
    account_address: str = Field(
        default=None, description="The Algorand account address, required for 'account_info' operation."
    )
    transaction_id: str = Field(
        default=None, description="The transaction ID, required for 'transaction_details' operation."
    )
    asset_id: str = Field(
        default=None, description="The asset ID, required for 'asset_info' operation."
    )

    def run(self):
        """
        Executes the tool's main functionality based on the specified operation.
        """
        try:
            if self.operation == 'account_info':
                return self._get_account_info()
            elif self.operation == 'transaction_details':
                return self._get_transaction_details()
            elif self.operation == 'asset_info':
                return self._get_asset_info()
            else:
                return "Invalid operation specified."
        except Exception as e:
            return f"Algorand API Error: {str(e)}"

    def _get_account_info(self):
        """
        Retrieves account information from the Algorand blockchain.
        """
        if not self.account_address:
            return "Account address is required for retrieving account information."

        url = f"{algorand_api_url}/v2/accounts/{self.account_address}"
        headers = {
            "X-Algo-API-Token": algorand_api_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _get_transaction_details(self):
        """
        Retrieves transaction details from the Algorand blockchain.
        """
        if not self.transaction_id:
            return "Transaction ID is required for retrieving transaction details."

        url = f"{algorand_api_url}/v2/transactions/{self.transaction_id}"
        headers = {
            "X-Algo-API-Token": algorand_api_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _get_asset_info(self):
        """
        Retrieves asset information from the Algorand blockchain.
        """
        if not self.asset_id:
            return "Asset ID is required for retrieving asset information."

        url = f"{algorand_api_url}/v2/assets/{self.asset_id}"
        headers = {
            "X-Algo-API-Token": algorand_api_key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()