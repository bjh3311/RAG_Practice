from pathlib import Path
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.core.config import settings

import yaml

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "mcp.yaml"

def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)
    
class MCPService:
    def __init__(self):
        self.prompt_config = load_prompt()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt_config["system_message"]),
            ("user", self.prompt_config["user_prompt"])
        ])

        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model="gpt-4o",
            temperature=0.3
        )
        self.rag_chain = (
            {
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser() # 단순 문자열 출력
        )
    
    async def summarize(self, content: str) -> str:
        result = await self.rag_chain.ainvoke(content)
        return result
