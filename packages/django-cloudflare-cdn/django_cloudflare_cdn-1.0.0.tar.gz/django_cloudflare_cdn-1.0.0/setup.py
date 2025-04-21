from setuptools import setup, find_packages

setup(
    name='django-cloudflare-cdn',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'django>=3.2',
        'django-storages>=1.10',
        'boto3>=1.18.0',
    ],
    description='A Django package for serving static files via S3-compatible CDN (Cloudflare R2).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Himel',
    author_email='python.package@himosoft.com.bd',
    url='https://github.com/Swe-HimelRana/django-cloudflare-cdn',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    include_package_data=True,
    keywords='django, cloudflare, cdn, storage, static files, s3, boto3',
    project_urls={
        'Documentation': 'https://github.com/Swe-HimelRana/django-cloudflare-cdn/blob/main/README.md',
        'Source': 'https://github.com/Swe-HimelRana/django-cloudflare-cdn',
        'Tracker': 'https://github.com/Swe-HimelRana/django-cloudflare-cdn/issues',
    },
)
