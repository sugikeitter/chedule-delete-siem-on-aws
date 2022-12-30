# schedule-delete-siem-on-aws

## Setup

```bash
git clone https://github.com/sugikeitter/schedule-delete-siem-on-aws.git

cd schedule-delete-siem-on-aws

# Edit template.yaml
vim template.yaml
```

| REPLACE | Note | Example |
|---|---|---|
| `<TARGET_HOSTNAME>` | Your OpenSearch host name | `xxxxxx.ap-northeast-1.es.amazonaws.com` |


## Build & Deploy
```bash
# You can use `sam build --use-container` if you installed container runtime.
sam build

# Use `sam deploy --guided` if you deploy for the first time.
sam deploy
```
