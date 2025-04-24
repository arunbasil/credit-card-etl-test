import pytest
import pandas as pd
import s3fs
import yaml
import os
from utils.logger import get_logger

logger = get_logger(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "connections.yaml")

@pytest.fixture(scope="session")
def s3_paths():
    """Loads S3 paths from YAML config."""
    logger.info("Loading S3 paths from YAML config file")
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    return config["data_paths"]

def test_can_access_target_file(s3_paths):
    # test
    try:
        logger.info(f"Attempting to read target file from: {s3_paths['target']}")
        df = pd.read_csv(s3_paths["target"])
        logger.info(f"Loaded target CSV with {len(df)} rows")
        assert not df.empty
    except Exception as e:
        logger.exception("Could not access target CSV")
        pytest.fail(f"Could not access target CSV: {e}")
