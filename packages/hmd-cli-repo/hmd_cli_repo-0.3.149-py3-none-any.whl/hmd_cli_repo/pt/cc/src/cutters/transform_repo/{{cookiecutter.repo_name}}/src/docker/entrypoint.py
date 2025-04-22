import logging
import sys
import os
import json
from pathlib import Path

from {{ cookiecutter.module_name }}.{{ cookiecutter.module_name }} import do_transform

logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s - %(message)s",
    level=logging.ERROR,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



def entry_point():

    # initialize variables for transform I/O
    input_content_path = Path("/hmd_transform/input")
    output_content_path = Path("/hmd_transform/output")

    transform_instance_context = json.loads(
        os.environ.get("TRANSFORM_INSTANCE_CONTEXT").replace("'", '"')
    )
    transform_nid = os.environ.get("TRANSFORM_NID")

    do_transform(input_content_path, output_content_path, transform_nid, transform_instance_context)
    logger.info("Transform complete.")


if __name__ == "__main__":
    entry_point()