from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import bigquery

def upload_csv_to_bigquery(service_account_path, project, table_id,
                           source_file_name):

    credentials = service_account.Credentials.from_service_account_file(
        service_account_path)

    client = bigquery.Client(project, credentials)

    job_config = bigquery.LoadJobConfig(
        source_format='CSV')

    with open(source_file_name, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file, table_id, job_config=job_config
        )
