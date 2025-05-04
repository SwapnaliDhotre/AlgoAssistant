from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json
import os

pinata_api_key = os.getenv("PINATA_API_KEY")
pinata_secret_api_key = os.getenv("PINATA_SECRET_API_KEY")

class NFTCreationTool(BaseTool):
    """
    A tool for creating NFTs based on user specifications.
    It supports the generation of NFT metadata, including attributes like name, description, image, and additional properties.
    The tool also handles the storage of associated files, such as images, on IPFS using Pinata.
    """

    name: str = Field(
        ..., description="The name of the NFT."
    )
    description: str = Field(
        ..., description="A description of the NFT."
    )
    image_path: str = Field(
        ..., description="The local file path to the image associated with the NFT."
    )
    additional_properties: dict = Field(
        default={}, description="Any additional properties to include in the NFT metadata."
    )

    def run(self):
        """
        Executes the tool's main functionality: create NFT metadata and store the image on IPFS.
        """
        try:
            # Upload the image to IPFS
            image_ipfs_hash = self._upload_to_ipfs(self.image_path)

            # Create NFT metadata
            metadata = {
                "name": self.name,
                "description": self.description,
                "image": f"ipfs://{image_ipfs_hash}",
                **self.additional_properties
            }

            # Optionally, upload metadata to IPFS
            metadata_ipfs_hash = self._upload_metadata_to_ipfs(metadata)

            return {
                "metadata": metadata,
                "metadata_ipfs_hash": metadata_ipfs_hash
            }
        except Exception as e:
            return f"NFT Creation Error: {str(e)}"

    def _upload_to_ipfs(self, file_path):
        """
        Uploads a file to IPFS using Pinata and returns the IPFS hash.
        """
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": pinata_api_key,
            "pinata_secret_api_key": pinata_secret_api_key
        }
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            ipfs_hash = response.json()['IpfsHash']
            return ipfs_hash

    def _upload_metadata_to_ipfs(self, metadata):
        """
        Uploads metadata to IPFS using Pinata and returns the IPFS hash.
        """
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        headers = {
            "Content-Type": "application/json",
            "pinata_api_key": pinata_api_key,
            "pinata_secret_api_key": pinata_secret_api_key
        }
        response = requests.post(url, data=json.dumps(metadata), headers=headers)
        response.raise_for_status()
        ipfs_hash = response.json()['IpfsHash']
        return ipfs_hash