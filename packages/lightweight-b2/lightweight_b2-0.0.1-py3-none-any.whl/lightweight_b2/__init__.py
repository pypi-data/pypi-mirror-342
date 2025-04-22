from .core.b2_client import B2Client as B2Client
from .core.storage_connection_parameters import StorageConnectionParameters as StorageConnectionParameters

__all__ = [
    'B2Client',
    'StorageConnectionParameters'
]

__version__ = "0.0.1"
__author__ = "Daniel Lasota <grossmann.root@gmail.com>"
__description__ = "B2 client. Supports Backblaze. Missing memory leak feature (unlike boto3) but work in progress"
__email__ = "grossmann.root@gmail.com"
__url__ = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
__status__ = "development"
__date__ = "22-04-2025"
