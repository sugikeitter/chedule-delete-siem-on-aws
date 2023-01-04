import datetime
import os

import boto3
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection

AOS_HOSTNAME = os.getenv('AOS_HOSTNAME')
# Delete logs XX days old.
DAYS = int(os.getenv('RETENTION_DAYS'))


def handler(event, context):
  # Create OpenSearch client
  awsauth = create_awsauth(AOS_HOSTNAME)
  aos_client = create_aos_client(awsauth, AOS_HOSTNAME)
  # YYYY-MM-DD, XX days ago.
  dt_now = datetime.datetime.now()
  dt_before = datetime.timedelta(days=DAYS)
  dt = dt_now - dt_before
  yyyy_mm = dt.strftime('%Y-%m')
  yyyy_mm_dd = dt.strftime('%Y-%m-%d')
  print(yyyy_mm) # DEBUG
  print(yyyy_mm_dd) # DEBUG

  # GET /_cat/indices で YYYY-MM が XX 日前のものを抜き出して index_names へ
  #  ex) ["log-aws-aaa-YYYY-MM", "log-aws-bbb-YYYY-MM", "log-aws-ccc-YYYY-MM"]
  indices = aos_client.cat.indices()
  index_names = []
  for i in indices.split("\n"):
    i_list = i.split()
    if len(i_list) <= 2:
      break
    index_name = i_list[2]
    if yyyy_mm in index_name:
      index_names.append(index_name)
  # XX 日前の YYYY-MM-DD を抜き出して、log-aws-***-YYYY-MM を bulk で削除
  print('=== GET _cat/indices/ ===')
  print(index_names) # DEBUG
  for index_name in index_names:
    print('=== POST ' + index_name + '/_delete_by_query ===') # DEBUG
    res = aos_client.delete_by_query(
      index=index_name,
      body={
        "query": {
          "range": {
            "eventTime": {
              "lte": yyyy_mm_dd + "T00:00:00Z"
            }
          }
        }
      }
    )
    print(res) # DEBUG

    
def create_awsauth(aos_hostname):
  aos_region = aos_hostname.split('.')[1]
  credentials = boto3.Session().get_credentials()
  return AWSV4SignerAuth(credentials, aos_region)


def create_aos_client(awsauth, aos_hostname):
  return OpenSearch(
    hosts=[{'host': aos_hostname, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    http_compress=True,
    verify_certs=True,
    retry_on_timeout=True,
    connection_class=RequestsHttpConnection,
    timeout=60)
