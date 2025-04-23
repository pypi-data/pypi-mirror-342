from langchain_openai import ChatOpenAI
from kosmoy_sdk import GatewayConfig
from kosmoy_sdk._kosmoy_base import KosmoyBase
from typing import Optional, Any
from pydantic import Field
from kosmoy_sdk.environment import KosmoyEnvironment


class CustomChatOpenAI(ChatOpenAI):
    """Extended ChatOpenAI that allows for additional configuration"""
    gateway_config: Optional[GatewayConfig] = Field(default=None, exclude=True)
    session: Optional[Any] = Field(default=None, exclude=True)


class KosmoyGatewayLangchain(CustomChatOpenAI, KosmoyBase):

    def __init__(
            self,
            app_id: str,
            api_key: str,
            model: str,
            use_guardrails: bool = False,
            environment: KosmoyEnvironment = KosmoyEnvironment.PRODUCTION,
            timeout: int = 30,
            max_retries: int = 3,
            **kwargs
    ):
        kwargs["metadata"] = {
            "use_guardrails": use_guardrails
        }

        CustomChatOpenAI.__init__(
            self,
            base_url=f"{environment.api_url}/gateway/invoke",
            api_key=api_key,
            model=model,
            default_headers={
                "app-id": app_id,
                "api-key": api_key,
                "use_guardrails": str(use_guardrails), # langchain is not passing it as metadata the way they claim
                "Content-Type": "application/json",
            },
            **kwargs
        )

        KosmoyBase.__init__(self, app_id=app_id, api_key=api_key, environment=environment, timeout=timeout,
                            max_retries=max_retries)

