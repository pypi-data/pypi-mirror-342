from .core.s3_client import S3Client as S3Client
from .core.storage_connection_parameters import StorageConnectionParameters

__all__ = [
    'S3Client',
    'StorageConnectionParameters'
]

__version__ = "0.0.1"
__author__ = "Daniel Lasota <grossmann.root@gmail.com>"
__description__ = "S3 client. Supports Backblaze. Missing memory leak feature (unlike boto3) but work in progress"
__email__ = "grossmann.root@gmail.com"
__url__ = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
__status__ = "development"
__date__ = "22-04-2025"
