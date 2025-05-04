from agency_swarm.tools import BaseTool
from pydantic import Field
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os

infura_url = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

class DeFiSwapTool(BaseTool):
    """
    A tool for performing token swaps on decentralized exchanges (DEXs) like Uniswap or SushiSwap.
    It handles connecting to the DEX, executing the swap, and returning transaction details.
    """

    dex: str = Field(
        ..., description="The decentralized exchange to use: 'uniswap' or 'sushiswap'."
    )
    private_key: str = Field(
        ..., description="The private key of the user's wallet for signing transactions."
    )
    token_in: str = Field(
        ..., description="The address of the token to swap from."
    )
    token_out: str = Field(
        ..., description="The address of the token to swap to."
    )
    amount_in: int = Field(
        ..., description="The amount of the input token to swap."
    )
    slippage: float = Field(
        default=0.01, description="The acceptable slippage percentage for the swap."
    )

    def run(self):
        """
        Executes the tool's main functionality to perform a token swap.
        """
        try:
            if self.dex == 'uniswap':
                return self._swap_on_uniswap()
            elif self.dex == 'sushiswap':
                return self._swap_on_sushiswap()
            else:
                return "Invalid DEX specified."
        except Exception as e:
            return f"DeFi Swap Error: {str(e)}"

    def _swap_on_uniswap(self):
        """
        Performs a token swap on Uniswap.
        """
        # Uniswap Router contract address and ABI
        uniswap_router_address = "0x7a250d5630b4cf539739df2c5dacf5d2d7a3ebc0"
        uniswap_router_abi = json.loads('[...]')  # Uniswap V2 Router ABI

        # Connect to Uniswap Router
        uniswap_router = web3.eth.contract(address=uniswap_router_address, abi=uniswap_router_abi)

        # Calculate minimum amount out based on slippage
        amount_out_min = self._calculate_min_amount_out(self.amount_in, self.slippage)

        # Build transaction
        account = web3.eth.account.privateKeyToAccount(self.private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        txn = uniswap_router.functions.swapExactTokensForTokens(
            self.amount_in,
            amount_out_min,
            [self.token_in, self.token_out],
            account.address,
            (web3.eth.getBlock('latest')['timestamp'] + 1000)
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

    def _swap_on_sushiswap(self):
        """
        Performs a token swap on SushiSwap.
        """
        # SushiSwap Router contract address and ABI
        sushiswap_router_address = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
        sushiswap_router_abi = json.loads('[...]')  # SushiSwap Router ABI

        # Connect to SushiSwap Router
        sushiswap_router = web3.eth.contract(address=sushiswap_router_address, abi=sushiswap_router_abi)

        # Calculate minimum amount out based on slippage
        amount_out_min = self._calculate_min_amount_out(self.amount_in, self.slippage)

        # Build transaction
        account = web3.eth.account.privateKeyToAccount(self.private_key)
        nonce = web3.eth.getTransactionCount(account.address)
        txn = sushiswap_router.functions.swapExactTokensForTokens(
            self.amount_in,
            amount_out_min,
            [self.token_in, self.token_out],
            account.address,
            (web3.eth.getBlock('latest')['timestamp'] + 1000)
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

    def _calculate_min_amount_out(self, amount_in, slippage):
        """
        Calculates the minimum amount out based on the specified slippage.
        """
        # Placeholder for actual slippage calculation logic
        return int(amount_in * (1 - slippage))