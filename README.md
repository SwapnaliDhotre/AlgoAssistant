# AlgoAssistant - Autonomous Agentic Framework for Algorand

**AlgoAssistant** is an open-source agentic system built using [Agency Swarm](https://github.com/VRSEN/agency-swarm) that automates interactions with the Algorand blockchain. It leverages multiple purpose-built agents to help developers, creators, and DeFi users build, publish, and transact on-chain with AI assistance.

## How to Run the App

### 1. Clone the Repository

git clone https://github.com/your-username/algobot-project.git
cd algobot-project

### 2.Create a Virtual Environment (optional)

python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Provide Your OpenAI API Key
On first run, the app will ask you for your OpenAI API key and save it to a .env file.
Alternatively, manually create a .env file:
python main.py

### 5. Run the App

python main.py



### Agent Architecture
The system is designed using autonomous agents that communicate with each other through the CEO agent.

## 1. CEOAgent
Acts as the primary interface for user input.
Routes requests to the appropriate functional agent.

## 2. SmartContractDevDeployer
Generates and compiles smart contracts based on user intent.
Uses Algorand SDK + Solc/Vyper.
Deploys contracts to the Algorand TestNet.

## 3. NFTDevPublisher
Generates NFT metadata and structure.
Publishes NFTs (demo supports OpenSea-compatible logic).
Future-ready for multichain publishing.

## 4. BlockchainReadWrite
Reads: balances, asset data, transactions, application state.
Writes: send Algos, opt-in/out of assets, call contracts.

## 5. DeFiManager
Swaps tokens (ASA to ASA).
Stakes and unstakes funds.
Rebalances across strategies to maximize yield.

## Sample Prompts
Create and deploy a smart contract that locks funds for 7 days.
Publish an NFT named 'AlgoKitty' with this image.
Check balance for address ABC123
Stake 100 Algo and rebalance portfolio weekly.
