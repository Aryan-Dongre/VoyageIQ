import os 
from dotenv import load_dotenv

load_dotenv()


def get_azure_secret(secret_name):
    # from azure.identity import AzureCliCredential    
    # AzureCliCredential is Uses the Azure CLI login, mainly for local development.
    
    from azure.identity import DefaultAzureCredential
    # DefaultAzureCredentia is use for Flexible authentication for local + Azure environments
    from azure.keyvault.secrets import SecretClient

    key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")

    # credential = AzureCliCredential()
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url=key_vault_url, 
        credential=credential
    )

    return client.get_secret(secret_name).value

def get_secret(env_name, azure_secret_name):

    use_key_vault = os.getenv("USE_AZURE_KEY_VAULT", "false").lower() == "true"

    if use_key_vault:
        return get_azure_secret(azure_secret_name)
    
    return os.getenv(env_name)

class Config:
    # If Azure Key Vault is used, fetch the secret from there; otherwise, use the environment variable
    
    SECRET_KEY= get_secret("SECRET_KEY", "VOYAGEIQ-SECRET-KEY")  
    
    DB_HOST= os.getenv("DB_HOST")
    DB_NAME= os.getenv("DB_NAME")
    DB_USER= os.getenv("DB_USER")

    DB_PASSWORD= get_secret("DB_PASSWORD", "VOYAGEIQ-DB-PASSWORD")
    DB_PORT= os.getenv("DB_PORT")

    # API KEYS
    SERPAPI_API_KEY= get_secret("SERPAPI_API_KEY", "VOYAGEIQ-SERPAPI-KEY")
    WEATHER_API= os.getenv("WEATHER_API")

     # Azure Functions URL
    AIRPORT_API_URL = os.getenv("AIRPORT_API_URL", "")
    HOTEL_API_URL = os.getenv("HOTEL_API_URL", "")
    FLIGHT_API_URL = os.getenv("FLIGHT_API_URL", "")
