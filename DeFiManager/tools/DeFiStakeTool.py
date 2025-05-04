from agency_swarm.tools import BaseTool
from pydantic import Field
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os

infura_url = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

class DeFiStakeTool(BaseTool):
    """
    A tool for staking tokens in DeFi protocols such as liquidity pools or yield farming platforms.
    It handles connecting to the protocol, executing the staking operation, and returning transaction details.
    """

    protocol: str = Field(
        ..., description="The DeFi protocol to use for staking, e.g., 'uniswap', 'sushiswap', etc."
    )
    private_key: str = Field(
        ..., description="The private key of the user's wallet for signing transactions."
    )
    token_address: str = Field(
        ..., description="The address of the token to stake."
    )
    amount: int = Field(
        ..., description="The amount of the token to stake."
    )
    pool_address: str = Field(
        ..., description="The address of the liquidity pool or yield farming contract."
    )

    def run(self):
        """
        Executes the tool's main functionality to perform token staking.
        """
        try:
            if self.protocol == 'uniswap':
                return self._stake_on_uniswap()
            elif self.protocol == 'sushiswap':
                return self._stake_on_sushiswap()
            else:
                return "Invalid protocol specified."
        except Exception as e:
            return f"DeFi Stake Error: {str(e)}"

    def _stake_on_uniswap(self):
        """
        Performs token staking on Uniswap.
        """
        # Uniswap Staking contract ABI
        staking_abi = json.loads('[...]')  # Uniswap Staking Contract ABI

        # Connect to the staking contract
        staking_contract = web3.eth.contract(address=self.pool_address, abi=staking_abi)

        # Build transaction
        account = web3.eth.account.privateKeyToAccount(self.private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        txn = staking_contract.functions.stake(
            self.token_address,
            self.amount
        ).buildTransaction({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': web3.toWei('5', 'gwei'),
            'nonce': nonce,
        })

        # Sign and send transaction
        signed_txn = web3.eth.account.signTransaction(txn, private_key=self.private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return f"Transaction sent with hash: {web3.toHex(tx_hash)}"

    def _stake_on_sushiswap(self):
        """
        Performs token staking on SushiSwap.
        """
        # SushiSwap Staking contract ABI
        staking_abi = json.loads('[...]')  # SushiSwap Staking Contract ABI

        # Connect to the staking contract
        staking_contract = web3.eth.contract(address=self.pool_address, abi=staking_abi)

        # Build transaction
        account = web3.eth.account.privateKeyToAccount(self.private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        txn = staking_contract.functions.stake(
            self.token_address,
            self.amount
        ).buildTransaction({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': web3.toWei('5', 'gwei'),
            'nonce': nonce,
        })

        # Sign and send transaction
        signed_txn = web3.eth.account.signTransaction(txn, private_key=self.private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return f"Transaction sent with hash: {web3.toHex(tx_hash)}"