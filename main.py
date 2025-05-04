from agency_swarm import Agency, set_openai_client
from DeFiManager import DeFiManager
from BlockchainReadWrite import BlockchainReadWrite
from NFTDevPublisher import NFTDevPublisher
from SmartContractDevDeployer import SmartContractDevDeployer
from CEOAgent import CEOAgent
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),)
set_openai_client(client)

ceo = CEOAgent()
smart_contract_dev = SmartContractDevDeployer()
nft_dev = NFTDevPublisher()
blockchain_rw = BlockchainReadWrite()
defi_manager = DeFiManager()

agency = Agency([ceo, [ceo, smart_contract_dev],
                 [ceo, nft_dev],
                 [ceo, blockchain_rw],
                 [ceo, defi_manager],
                 [smart_contract_dev, blockchain_rw],
                 [nft_dev, blockchain_rw],
                 [defi_manager, blockchain_rw]],
                shared_instructions='./agency_manifesto.md',
                max_prompt_tokens=25000,
                temperature=0.3)

if __name__ == '__main__':
    agency.demo_gradio(height=300)
