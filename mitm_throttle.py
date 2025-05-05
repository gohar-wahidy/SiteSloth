from mitmproxy import http
import asyncio
import json
import os

CONFIG_FILE = "throttle_config.json"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        THROTTLED_DOMAINS = json.load(f)
else:
    THROTTLED_DOMAINS = {}

print("[*] Loaded throttle config:", THROTTLED_DOMAINS)

class ThrottleAddon:
    def responseheaders(self, flow: http.HTTPFlow):
        hostname = flow.request.pretty_host.lower()
        for domain in THROTTLED_DOMAINS:
            if domain in hostname:
                flow.response.stream = self.make_stream(domain)

    def make_stream(self, domain):
        speed_kbps = THROTTLED_DOMAINS[domain]
        chunk_size = speed_kbps * 1024 // 10

        async def stream_handler(flow: http.HTTPFlow):
            async for chunk in flow.response.stream_chunks():
                for i in range(0, len(chunk.content), chunk_size):
                    part = chunk.content[i:i+chunk_size]
                    flow.response.stream_data(part)
                    await asyncio.sleep(0.1)

        return stream_handler

addons = [ThrottleAddon()]
