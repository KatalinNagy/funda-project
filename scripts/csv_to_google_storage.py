from google.cloud import storage
from google.oauth2 import service_account


def upload_to_google_storage(service_account_path, project, bucket,
                             file):

    credentials = service_account.Credentials.from_service_account_file(
        service_account_path)
    client = storage.Client(project, credentials)
    bucket = client.get_bucket(bucket)
    blob = bucket.blob('funda.csv')
    blob.upload_from_filename(file)


def main():
    upload_to_google_storage()

if __name__ == "__main__":
    main()
