import json, os, glob

dumps = sorted(glob.glob("/root/.hermes/sessions/request_dump_*.json"), key=os.path.getmtime, reverse=True)
latest = dumps[0]
print(f"Dump: {os.path.basename(latest)}")

with open(latest) as f:
    data = json.load(f)

req = data.get("request", {})
headers = req.get("headers", {})
auth = headers.get("authorization", headers.get("Authorization", "NOT FOUND"))
print(f"URL: {req.get('url', 'N/A')}")
print(f"Auth: {auth[:40]}...")
print(f"Auth len: {len(auth) if auth else 0}")

# Also show the body if it's a chat completion
body = req.get("body", "")
if isinstance(body, dict):
    model = body.get("model", "N/A")
    msgs = body.get("messages", [])
    print(f"Model: {model}")
    print(f"Messages: {len(msgs)}")
