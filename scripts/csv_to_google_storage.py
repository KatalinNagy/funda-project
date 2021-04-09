from google.cloud import storage
from google.oauth2 import service_account


def upload_to_google_storage():
    service_account_path = '/home/katalin/bucket_credentials/portfolio-projects-310210-6f276e48986d.json'
    credentials = service_account.Credentials.from_service_account_file(
        service_account_path)
    client = storage.Client('portfolio_projects', credentials)
    bucket = client.get_bucket('de_portfolio_bucket')
    blob = bucket.blob('funda.csv')
    blob.upload_from_filename('/home/katalin/PycharmProjectsFolder/funda-project/data/funda.csv')


def main():
    upload_to_google_storage()

if __name__ == "__main__":
    main()
