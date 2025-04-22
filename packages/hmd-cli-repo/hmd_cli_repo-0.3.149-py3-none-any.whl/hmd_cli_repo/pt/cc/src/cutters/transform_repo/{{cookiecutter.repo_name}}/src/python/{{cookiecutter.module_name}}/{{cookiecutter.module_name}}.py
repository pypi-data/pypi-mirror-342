import logging
import sys
import os
import json
from pathlib import Path
import shutil
from typing import Dict

logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.ERROR,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def do_transform(
    input_content_path: str,
    output_content_path: str,
    transform_nid: str,
    transform_instance_context: Dict,
) -> int:
    """Function to do the actual Transform work

    Args:
        input_content_path (str): filepath for input files
        output_content_path (str): filepath for output files
        transform_nid (str): NID of running TransformInstance
        transform_instance_context (Dict): context dictionary for the running TransformInstance

    Returns:
        int: exit code
    """
    for x in os.listdir(input_content_path):
        logger.info(f"Processing input file {x}...")
        shutil.copy(input_content_path / x, output_content_path / "sample_output.txt")

    secret_path = Path("/run/secrets")

    for x in os.listdir(secret_path):
        logger.info(f"This is how to locate a secret: {x} in {secret_path}")

    logger.info(f"Transform_nid: {transform_nid}")
    logger.info(f"Transform_instance_context: {transform_instance_context}")

    return 0
