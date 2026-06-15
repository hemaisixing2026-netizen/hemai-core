#!/bin/bash
REAL_KEY=\
cd /root/.hermes
python3 -c "
import yaml
with open('config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['providers']['deepseek']['api_key'] = '\'
with open('config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
print('Done')
"
# verify
NEW_KEY=\
echo "New key length: \"
echo "New key start: \"
echo "New key end: \"
# test
HTTP=\
echo "HTTP: \"
