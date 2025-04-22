from setuptools import setup, find_packages


setup(
    name='lightweight-s3',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "lightweight_s3": ["py.typed", "core/*.pyi"],
    },
    install_requires=[
        'requests'
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Lasota",
    author_email="grossmann.root@gmail.com",
    description="Lightweight S3 client with backblaze support",
    keywords="s3 backblaze boto3 client",
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    python_requires='>=3.11',
)

