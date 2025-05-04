from agency_swarm.agents import Agent


class NFTDevPublisher(Agent):
    def __init__(self):
        super().__init__(
            name="NFTDevPublisher",
            description="The NFT Developer and Publisher agent is responsible for developing NFTs as specified by the user and deploying/publishing them on OpenSea.",
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
