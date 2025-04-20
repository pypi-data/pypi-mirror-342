import logging

from stac_generator.core import (
    CollectionGenerator,
    PointConfig,
    PointGenerator,
    RasterConfig,
    RasterGenerator,
    VectorConfig,
    VectorGenerator,
)
from stac_generator.factory import StacGeneratorFactory

__all__ = (
    "CollectionGenerator",
    "PointConfig",
    "PointGenerator",
    "RasterConfig",
    "RasterGenerator",
    "StacGeneratorFactory",
    "VectorConfig",
    "VectorGenerator",
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Attempt to disable logging from other modules - does not work yet
disable_logging = ["httpcore", "httpx"]

for name in logging.root.manager.loggerDict:
    if not name.startswith(__name__) or name in disable_logging:
        logging.getLogger(name).disabled = True
