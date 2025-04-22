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

# def test_source_csv_structure(s3_paths):
#     """Ensure all rows in source CSV have the same number of columns."""
#     try:
#         logger.info("Validating row consistency in source CSV")
#         fs = s3fs.S3FileSystem()
#         with fs.open(s3_paths["source"], 'r') as f:
#             lines = f.readlines()
#         header_cols = len(lines[0].strip().split(","))
#         logger.info(f"Header has {header_cols} columns")
#         for idx, line in enumerate(lines[1:], start=2):
#             if len(line.strip().split(",")) != header_cols:
#                 logger.error(f"Inconsistent column count at line {idx}")
#                 pytest.fail(f"Inconsistent column count at line {idx}")
#         logger.info("Source CSV passed structure validation")
#     except Exception as e:
#         logger.exception("Failed to validate source CSV row structure")
#         pytest.fail(f"Failed to validate row structure: {e}")
#
# def test_target_csv_skips_bad_lines(s3_paths):
#     """Test that target CSV loads even if it has malformed rows by skipping them."""
#     try:
#         logger.info("Testing target CSV read with on_bad_lines='skip'")
#         fs = s3fs.S3FileSystem()
#         with fs.open(s3_paths["target"], "r") as f:
#             df = pd.read_csv(f, on_bad_lines="skip")
#         logger.info(f"Target CSV loaded with {len(df)} rows (bad lines skipped)")
#         logger.debug(f"Sample rows:\n{df.head()}")
#         assert not df.empty, "Target CSV was empty after skipping bad rows."
#     except Exception as e:
#         logger.exception("Failed to read target CSV with bad rows skipped")
#         pytest.fail(f"Failed to read target CSV with bad rows skipped: {e}")
#
# def test_can_access_source_file(s3_paths):
#     """Check if source CSV in S3 is accessible."""
#     try:
#         logger.info(f"Attempting to read source file: {s3_paths['source']}")
#         df = pd.read_csv(s3_paths["source"])
#         logger.info(f"Loaded source CSV with {len(df)} rows")
#         assert not df.empty
#     except Exception as e:
#         logger.exception("Could not access source CSV")
#         pytest.fail(f"Could not access source CSV: {e}")

def test_can_access_target_file(s3_paths):

    try:
        logger.info(f"Attempting to read target file from: {s3_paths['target']}")
        df = pd.read_csv(s3_paths["target"])
        logger.info(f"Loaded target CSV with {len(df)} rows")
        assert not df.empty
    except Exception as e:
        logger.exception("Could not access target CSV")
        pytest.fail(f"Could not access target CSV: {e}")
