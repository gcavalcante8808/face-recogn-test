import boto3
import os


class S3Storage(object):
    def __init__(self):
        """
        Map s3 env vars into obj attrs and create bucket if needed.
        """
        self.s3_access_key = os.getenv('S3_ACCESS_KEY')
        self.s3_secret_key = os.getenv('S3_SECRET_KEY')
        self.s3_endpoint_url = os.getenv('S3_ENDPOINT_URL')
        self.s3_bucket = os.getenv('S3_BUCKET')

        self.session = boto3.Session(
            aws_access_key_id=self.s3_access_key,
            aws_secret_access_key=self.s3_secret_key
        )

        self.s3 = self.session.resource('s3',
            endpoint_url=self.s3_endpoint_url,
            config=boto3.session.Config(signature_version='s3v4')
        )

        self.bucket = self.get_or_create_bucket()

    def get_or_create_bucket(self):
        """
        Get or create a bucket.
        """
        #Create bucket is idempotent. Lets see.
        if not self.s3.Bucket(self.s3_bucket) in self.s3.buckets.all():
            bucket = self.s3.create_bucket(Bucket=self.s3_bucket)

        bucket = self.s3.Bucket(self.s3_bucket)
        return bucket

    def upload_fileobj(self, obj, filename):
        """
        Upload a Binary File to s3.
        """
        self.bucket.upload_fileobj(obj, filename)

s3_client = S3Storage()