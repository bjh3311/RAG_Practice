from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    
    class Config:
        env_file = ".env"  # .env 파일에서 환경변수 자동 로드

settings = Settings()