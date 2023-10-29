import boto3
import base64
from decouple import config

s3_client = boto3.client("s3", 
                  region_name=config('AWS_DEFAULT_REGION'), 
                  aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                  aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))


def upload_image_to_s3(file_name, image_string, extension):
    """
    Upload base64 image to s3
    """
    try:
        # Generate unique file name
        # file_name = 'profile/' + uuid.uuid4().hex + '.' + extension

        # Upload object
        s3_client.put_object(Body=image_string, Bucket=config('AWS_BUCKET_NAME'),
                             ContentType='image/{}'.format(extension), Key=file_name)

        return file_name
    except Exception as error:
        raise error