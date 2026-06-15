import yaml

with open("/root/workspace/.real_key") as f:
    real_key = f.read().strip()

with open("/root/.hermes/config.yaml") as f:
    cfg = yaml.safe_load(f)

old = cfg["providers"]["deepseek"]["api_key"]
print(f"Old: {old[:15]}... len={len(old)}")

cfg["providers"]["deepseek"]["api_key"] = real_key

with open("/root/.hermes/config.yaml", "w") as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)

with open("/root/.hermes/config.yaml") as f:
    cfg2 = yaml.safe_load(f)
new = cfg2["providers"]["deepseek"]["api_key"]
print(f"New: {new[:15]}... len={len(new)}")
print(f"OK: {new == real_key}")
