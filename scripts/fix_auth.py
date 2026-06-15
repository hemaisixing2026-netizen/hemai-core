import yaml, json, hashlib

# Read key from config.yaml
with open("/root/.hermes/config.yaml") as f:
    cfg = yaml.safe_load(f)
key = cfg["providers"]["deepseek"]["api_key"]

# Read auth.json
with open("/root/.hermes/auth.json") as f:
    auth = json.load(f)

# Add deepseek credential
fingerprint = "sha256:" + hashlib.sha256(key.encode()).hexdigest()
auth["credential_pool"]["deepseek"] = [{
    "id": "deepseek-direct",
    "label": "DEEPSEEK_API_KEY",
    "auth_type": "api_key",
    "priority": 0,
    "source": "config",
    "last_status": None,
    "last_status_at": None,
    "last_error_code": None,
    "last_error_reason": None,
    "last_error_message": None,
    "last_error_reset_at": None,
    "base_url": "https://api.deepseek.com",
    "request_count": 0,
    "secret_fingerprint": fingerprint
}]

with open("/root/.hermes/auth.json", "w") as f:
    json.dump(auth, f, indent=2)
    f.write("\n")

print(f"Added deepseek credential, fingerprint: {fingerprint}")
print("DeepSeek pool size:", len(auth["credential_pool"]["deepseek"]))
