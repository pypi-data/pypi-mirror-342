import logging
import sys
import os
import json
from pathlib import Path

import nbformat
import datetime
import papermill as pm


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

    notebook = transform_instance_context["notebook"]
    params = transform_instance_context["params"]

    # add input and output paths to params
    params["transform_input_path"] = str(input_content_path)
    params["transform_output_path"] = str(output_content_path)

    input_path = Path("/app/notebooks") / notebook
    output_path = output_content_path / notebook
    pm.execute_notebook(input_path, output_path, parameters=params)

    logger.info("Transform complete.")


if __name__ == "__main__":
    entry_point()
