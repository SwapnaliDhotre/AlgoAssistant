from agency_swarm.agents import Agent


class BlockchainReadWrite(Agent):
    def __init__(self):
        super().__init__(
            name="BlockchainReadWrite",
            description="The Blockchain Read/Write agent is responsible for reading and writing on the Algorand blockchain.",
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
