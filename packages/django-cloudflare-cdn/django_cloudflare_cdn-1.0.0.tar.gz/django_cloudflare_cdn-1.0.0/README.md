# DjangoCloudflareCDN

## Overview

DjangoCloudflareCDN is a simple Python package that allows you to easily integrate Cloudflare R2 with Django for serving static and media files. It provides a seamless setup using `django-storages` and `boto3` to configure Django’s storage backends for Cloudflare R2.

## Features

- Integrates Cloudflare R2 as the static and media file storage for Django.
- Supports custom domain setup for Cloudflare R2.
- Automatically configures `django-storages` for S3-compatible storage with Cloudflare R2.
- Provides customizable settings for Cloudflare R2, including access keys and cache control.

## Installation

   ```bash
   pip install django-cloudflare-cdn
   ```

## Usage
1. Add DjangoCloudflareCDN to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    # other apps
    'DjangoCloudflareCDN',
]
```
2. Import the Cloudflare R2 settings in your settings.py

```python
# settings.py

from DjangoCloudflareCDN import cloudflare_r2
```

3. Configure Cloudflare R2 credentials and settings

```python
# settings.py

# Cloudflare R2 Settings
AWS_ACCESS_KEY_ID = '<your-access-key>'
AWS_SECRET_ACCESS_KEY = '<your-secret-key>'
AWS_STORAGE_BUCKET_NAME = '<your-bucket-name>'
AWS_S3_ENDPOINT_URL = 'https://<your-account-id>.r2.cloudflarestorage.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.r2.cloudflarestorage.com'

# Static File Settings
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# Use S3Boto3Storage as the default storage backend
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

4. Run the collectstatic command to upload your static files to Cloudflare R2 (Depends on api configuration)

```python
python manage.py collectstatic
```

# Optional Settings

Custom ACL for Files: Uncomment the AWS_DEFAULT_ACL line to make all files publicly readable.

```python
    #settins.py

    AWS_DEFAULT_ACL = 'public-read'
```
Cache Control: Customize the cache control settings for your files.

```python
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400'
    }
```

# Troubleshooting

- Ensure that your Cloudflare R2 bucket is properly configured.

- Double-check your Cloudflare R2 credentials (Access Key and Secret Key).

- If files are not showing up, ensure that you have run the collectstatic command.