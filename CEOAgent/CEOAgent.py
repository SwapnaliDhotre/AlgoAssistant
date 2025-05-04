from agency_swarm.agents import Agent


class CEOAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CEOAgent",
            description="The CEO agent is responsible for managing communication and ensuring that user queries are directed to the appropriate agents within the BlockchainSolutionsAgency. It serves as the entry point for user interaction.",
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
