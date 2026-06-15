import yaml, urllib.request, json, sys

with open("/root/.hermes/config.yaml") as f:
    cfg = yaml.safe_load(f)
key = cfg["providers"]["deepseek"]["api_key"]

req = urllib.request.Request(
    "https://api.deepseek.com/v1/models",
    headers={"Authorization": f"Bearer {key}"}
)
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    print(f"OK - HTTP {resp.status}, models: {len(data.get('data', []))}")
except Exception as e:
    print(f"FAIL - {e}")
    sys.exit(1)
