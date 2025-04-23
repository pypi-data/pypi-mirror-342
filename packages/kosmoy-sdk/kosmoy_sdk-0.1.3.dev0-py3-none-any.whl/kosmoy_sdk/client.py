from kosmoy_sdk.environment import KosmoyEnvironment
from openai import OpenAI
from kosmoy_sdk._kosmoy_base import KosmoyBase
from kosmoy_sdk.exceptions import FunctionalityNotImplemented


class CustomChatCompletions:
    def __init__(self, client):
        self.client = client
        self._completions = CustomCompletions(client)
    
    @property
    def completions(self):
        return self._completions

class CustomCompletions:
    def __init__(self, client):
        self.client = client
        
    def create(self,
                model,
                use_guardrails: bool = False,
                *args, **kwargs):
        if kwargs.get('streaming'):
            raise FunctionalityNotImplemented("This functionality is not implemented in this version")
        kwargs["metadata"] = {
            "use_guardrails": use_guardrails
        }
        return self.client._client.chat.completions.create(model=model, *args, **kwargs)


class CustomOpenAI:
    def __init__(self, *args, **kwargs):
        self._client = OpenAI(*args, **kwargs)
        self._chat = CustomChatCompletions(client=self)

    @property
    def chat(self) -> CustomChatCompletions:
        return self._chat

    @property
    def beta(self):
        return self._client.beta

class GatewayClient(KosmoyBase):
    def __init__(
        self,
        app_id: str,
        api_key: str,
        environment: KosmoyEnvironment = KosmoyEnvironment.PRODUCTION,
        timeout: int = 30,
        max_retries: int = 3
    ):
        super().__init__(app_id=app_id, api_key=api_key, environment=environment, timeout=timeout, max_retries=max_retries)
        
        self.client = CustomOpenAI(
            base_url=f"{self.gateway_config.base_url}/gateway/invoke",
            api_key=api_key,
            default_headers={
                "app-id": app_id,
                "api-key": api_key,
                "Content-Type": "application/json"
            }
        )
