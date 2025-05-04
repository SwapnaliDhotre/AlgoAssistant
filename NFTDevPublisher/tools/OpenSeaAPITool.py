from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import os

opensea_api_key = os.getenv("OPENSEA_API_KEY")

class OpenSeaAPITool(BaseTool):
    """
    A tool for interacting with the OpenSea API for deploying and managing NFTs.
    It supports operations such as listing NFTs, updating metadata, and retrieving listing status.
    The tool handles authentication and API requests to OpenSea's endpoints.
    """

    asset_contract_address: str = Field(
        ..., description="The contract address of the NFT asset."
    )
    token_id: str = Field(
        ..., description="The token ID of the NFT."
    )
    operation: str = Field(
        ..., description="The operation to perform: 'list', 'update_metadata', or 'get_status'."
    )
    metadata: dict = Field(
        default=None, description="The metadata to update for the NFT, required for 'update_metadata' operation."
    )

    def run(self):
        """
        Executes the tool's main functionality based on the specified operation.
        """
        try:
            if self.operation == 'list':
                return self._list_nft()
            elif self.operation == 'update_metadata':
                return self._update_metadata()
            elif self.operation == 'get_status':
                return self._get_listing_status()
            else:
                return "Invalid operation specified."
        except Exception as e:
            return f"OpenSea API Error: {str(e)}"

    def _list_nft(self):
        """
        Lists an NFT on OpenSea.
        """
        url = f"https://api.opensea.io/api/v1/asset/{self.asset_contract_address}/{self.token_id}/"
        headers = {
            "Authorization": f"Bearer {opensea_api_key}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _update_metadata(self):
        """
        Updates the metadata of an NFT on OpenSea.
        """
        if not self.metadata:
            return "Metadata is required for updating."

        url = f"https://api.opensea.io/api/v1/asset/{self.asset_contract_address}/{self.token_id}/"
        headers = {
            "Authorization": f"Bearer {opensea_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.put(url, headers=headers, json=self.metadata)
        response.raise_for_status()
        return response.json()

    def _get_listing_status(self):
        """
        Retrieves the listing status of an NFT on OpenSea.
        """
        url = f"https://api.opensea.io/api/v1/asset/{self.asset_contract_address}/{self.token_id}/"
        headers = {
            "Authorization": f"Bearer {opensea_api_key}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()