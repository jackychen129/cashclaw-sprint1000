from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import httpx

from .config import settings


@dataclass
class Route:
    provider: str
    model: str
    base_url: str
    api_key: str


class ModelOrchestrator:
    def __init__(self) -> None:
        self.timeout = 45.0

    def pick_route(self, quality: str) -> Route:
        policy = settings.model_routing_policy
        wants_quality = quality in {"high", "quality"}

        if policy == "local_first" and not wants_quality:
            return Route("local", settings.local_model_name, settings.local_model_base_url, settings.local_model_api_key)
        if policy == "online_first":
            return Route("online", settings.online_model_name, settings.online_model_base_url, settings.online_model_api_key)
        if policy == "quality_first":
            return Route("online", settings.online_model_name, settings.online_model_base_url, settings.online_model_api_key)

        return Route("local", settings.local_model_name, settings.local_model_base_url, settings.local_model_api_key)

    async def complete(self, prompt: str, quality: str = "balanced") -> tuple[str, str]:
        route = self.pick_route(quality)
        content = await self._call_openai_compatible(route, prompt)
        return content, f"{route.provider}:{route.model}"

    async def _call_openai_compatible(self, route: Route, prompt: str) -> str:
        payload = {
            "model": route.model,
            "messages": [
                {"role": "system", "content": "You are a practical business execution assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        headers = {"Content-Type": "application/json"}
        if route.api_key:
            headers["Authorization"] = f"Bearer {route.api_key}"

        url = f"{route.base_url.rstrip('/')}/chat/completions"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
