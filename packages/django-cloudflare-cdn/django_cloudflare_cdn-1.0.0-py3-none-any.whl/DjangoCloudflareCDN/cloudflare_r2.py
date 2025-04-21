from django.conf import settings

# Default Storage Backend
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS Credentials & Bucket Settings
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = settings.AWS_S3_ENDPOINT_URL
AWS_S3_OBJECT_PARAMETERS = settings.AWS_S3_OBJECT_PARAMETERS

# Static File Settings
AWS_STATIC_LOCATION = 'static'
AWS_S3_CUSTOM_DOMAIN = f'{settings.AWS_S3_CUSTOM_DOMAIN}'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Optional: Uncomment for default ACL
# AWS_DEFAULT_ACL = 'public-read'