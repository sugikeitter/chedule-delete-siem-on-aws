# schedule-delete-siem-on-aws

## Setup

```bash
git clone https://github.com/sugikeitter/schedule-delete-siem-on-aws.git

cd schedule-delete-siem-on-aws

# Edit template.yaml
vim template.yaml
```

### Edit `template.yaml`
| Replace | Note | Example |
|---|---|---|
| `<YOUR_SIEM_OPERATE_ROLE_ARN>` | Your `siem-LambdaEsLoaderServiceRole` or your custome role. | `arn:aws:iam::123456789012:role/siem-LambdaEsLoaderServiceRoleXXXXXXX` |
| `<TARGET_HOSTNAME>` | Your OpenSearch host name. | `xxxxxx.ap-northeast-1.es.amazonaws.com` |
| `RETENTION_DAYS: 7` | The period of time before deletion. | `RETENTION_DAYS: 21 # about 3 weeks`, `RETENTION_DAYS: 365 # about 1 year` |
| `# INCLUDE_LIST: 'log-aws-waf'` | Comma delimited keyword list you want to delete. If you set INCLUDE_LIST, this Lambda function delete only indices including keyword. | `INCLUDE_LIST: 'log-aws-waf, log-aws-vpcflowlogs, log-aws-s3accesslog` |
| `# EXCLUDE_LIST: 'log-aws-cloudtrail, metrics-opensearch-index'` | Comma delimited keyword list you don't want to delete. | `EXCLUDE_LIST: 'log-aws-cloudtrail'` |
| `Schedule: "rate(12 hours)"` | The execution interval. For more information, see [document](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-schedule.html#sam-function-schedule-schedule) | `Schedule: "rate(6 hours)"` |

## Build & Deploy
```bash
# You can use `sam build --use-container` if you installed container runtime.
sam build

# Use `sam deploy --guided` if you deploy for the first time.
sam deploy
```
