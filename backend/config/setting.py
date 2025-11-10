import os

from pydantic import BaseModel

class Config(BaseModel):
    # Directory
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @property
    def artifact_dir(self) -> str:
        artifact_dir = os.path.join(self.base_dir, "artifacts")
        os.makedirs(artifact_dir, exist_ok=True)
        return artifact_dir 

    # Database url
    database_url: str = os.getenv("DB_URL")

    # Secret key
    secret_key: str = os.getenv("SECRET_KEY", "Chả cho biết đâu")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    refresh_token_expire_days: int = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
    security_algorithm: str = os.getenv("SECURITY_ALGORITHM", "HS256")


config = Config()