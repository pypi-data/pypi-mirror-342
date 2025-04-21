import os

import httpx

api_key = os.getenv("METASO_API_KEY", "")

client = httpx.Client(
    base_url="https://metaso.cn/api/open",
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=60,
)
