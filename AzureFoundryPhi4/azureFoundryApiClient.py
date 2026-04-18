from openai import OpenAI

def getClient() -> OpenAI :
    client = OpenAI(
        base_url = "https://dcs-foundry.services.ai.azure.com/openai/v1/",
        api_key = "..."
    )
    return client