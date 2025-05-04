from agency_swarm.tools import BaseTool
from pydantic import Field
from web3 import Web3
import os

infura_project_id = os.getenv("INFURA_PROJECT_ID")  # Ensure you have your Infura Project ID set in your environment variables

class BlockchainDeploymentAPI(BaseTool):
    """
    A tool for deploying smart contracts on blockchain networks.
    It supports both testnet and mainnet deployments, and includes features for connecting to blockchain nodes,
    sending transactions, and retrieving deployment status and transaction details.
    """

    network: str = Field(
        ..., description="The blockchain network to connect to. Supported values are 'mainnet', 'ropsten', 'rinkeby', etc."
    )
    private_key: str = Field(
        ..., description="The private key of the account used for deploying the contract."
    )
    contract_abi: list = Field(
        ..., description="The ABI of the smart contract to be deployed."
    )
    contract_bytecode: str = Field(
        ..., description="The bytecode of the smart contract to be deployed."
    )

    def run(self):
        """
        Executes the tool's main functionality: deploy a smart contract and retrieve transaction details.
        """
        try:
            # Connect to the specified network
            w3 = self._connect_to_network()

            # Get the account from the private key
            account = w3.eth.account.from_key(self.private_key)

            # Create the contract deployment transaction
            contract = w3.eth.contract(abi=self.contract_abi, bytecode=self.contract_bytecode)
            transaction = contract.constructor().buildTransaction({
                'from': account.address,
                'nonce': w3.eth.getTransactionCount(account.address),
                'gas': 2000000,
                'gasPrice': w3.toWei('50', 'gwei')
            })

            # Sign the transaction
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key=self.private_key)

            # Send the transaction
            txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

            # Retrieve transaction details
            txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

            return {
                "transaction_hash": txn_hash.hex(),
                "contract_address": txn_receipt.contractAddress,
                "status": txn_receipt.status
            }
        except Exception as e:
            return f"Deployment Error: {str(e)}"

    def _connect_to_network(self):
        """
        Connects to the specified Ethereum network using Infura.
        """
        infura_url = f"https://{self.network}.infura.io/v3/{infura_project_id}"
        return Web3(Web3.HTTPProvider(infura_url))