from pathlib import Path
from langchain_openai import ChatOpenAI
from app.core.config import settings
from mcp_use import MCPClient, MCPAgent
import json
import yaml

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "mcp.yaml"
CONFIG_PATH = Path(__file__).parent.parent / "core" / "multi_server_config.json"


def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)
    
class MCPService:
    def __init__(self):
        self.prompt_config = load_prompt()
        self.client = MCPClient.from_config_file(str(CONFIG_PATH))
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model="gpt-4o",
            temperature=0.3
        )
        self.agent = MCPAgent(
            llm=self.llm,
            client=self.client,
            system_prompt_template=self.prompt_config["system_message"]
        )
        
    async def summarize(self, content: str) -> str:
        result = await self.agent.run(content)
        return result
