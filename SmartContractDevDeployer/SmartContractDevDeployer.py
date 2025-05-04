from agency_swarm.agents import Agent


class SmartContractDevDeployer(Agent):
    def __init__(self):
        super().__init__(
            name="SmartContractDevDeployer",
            description="The Smart Contract Developer and Deployer agent is responsible for developing smart contracts based on user input and deploying them on testnet or mainnet as specified by the user.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        return message
