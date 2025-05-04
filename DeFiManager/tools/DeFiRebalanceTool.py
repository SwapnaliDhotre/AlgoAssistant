from agency_swarm.tools import BaseTool
from pydantic import Field
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os

infura_url = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

class DeFiRebalanceTool(BaseTool):
    """
    A tool for rebalancing a DeFi portfolio by adjusting token allocations across different DeFi protocols.
    It handles connecting to the protocols, executing the rebalancing operations, and returning transaction details.
    """

    private_key: str = Field(
        ..., description="The private key of the user's wallet for signing transactions."
    )
    target_allocations: dict = Field(
        ..., description="A dictionary specifying the target allocations for each token in the portfolio."
    )
    current_allocations: dict = Field(
        ..., description="A dictionary specifying the current allocations for each token in the portfolio."
    )
    protocols: dict = Field(
        ..., description="A dictionary specifying the DeFi protocols and their respective contract addresses."
    )

    def run(self):
        """
        Executes the tool's main functionality to rebalance the DeFi portfolio.
        """
        try:
            transactions = []
            for token, target_allocation in self.target_allocations.items():
                current_allocation = self.current_allocations.get(token, 0)
                if current_allocation != target_allocation:
                    protocol = self.protocols.get(token)
                    if protocol:
                        tx_hash = self._rebalance_token(token, current_allocation, target_allocation, protocol)
                        transactions.append(tx_hash)
            return f"Rebalancing transactions: {transactions}"
        except Exception as e:
            return f"DeFi Rebalance Error: {str(e)}"

    def _rebalance_token(self, token, current_allocation, target_allocation, protocol):
        """
        Rebalances a specific token to achieve the target allocation.
        """
        # Calculate the amount to adjust
        amount_to_adjust = target_allocation - current_allocation

        # Connect to the protocol's contract
        protocol_abi = json.loads('[...]')  # Protocol Contract ABI
        protocol_contract = web3.eth.contract(address=protocol['address'], abi=protocol_abi)

        # Build transaction
        account = web3.eth.account.privateKeyToAccount(self.private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        txn = protocol_contract.functions.adjustAllocation(
            token,
            amount_to_adjust
        ).buildTransaction({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': web3.toWei('5', 'gwei'),
            'nonce': nonce,
        })

        # Sign and send transaction
        signed_txn = web3.eth.account.signTransaction(txn, private_key=self.private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return web3.toHex(tx_hash)