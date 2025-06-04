from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ethereum Node Configuration
    eth_node_url: str

    # Database Configuration
    database_url: str

    # API Configuration
    api_host: str
    api_port: int

    # Request Timeout
    request_timeout: int = 60 * 2  # seconds

    # maximum block range for analysis
    MAX_BLOCK_RANGE: int = 7000

    # Logging Configuration
    log_level: str = "INFO"

    # Allium API Key
    allium_api_key: str

    # Github Token
    github_token: str

    # Etherscan API Key
    etherscan_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Map environment variables to class attributes
        fields = {
            "eth_node_url": "ETH_NODE_URL",
            "database_url": "DATABASE_URL",
            "api_host": "API_HOST",
            "api_port": "API_PORT",
            "log_level": "LOG_LEVEL",
            "allium_api_key": "ALLIUM_API_KEY",
            "github_token": "GITHUB_TOKEN",
            "ehterscan_api_key": "ETHERSCAN_API_KEY"
        }


settings = Settings()
