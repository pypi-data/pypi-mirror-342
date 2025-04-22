.. transforms

Anatomy of an HMD Transform
===============================

An HMD Transform can take many forms, but it has at a minimum a mini context and basic project structure that supports
docker and python.

Context:
+++++++++
#. TRANSFORM_INSTANCE_CONTEXT: the configuration for a Transform instance

    - Type: json
    - Default: standard input defined in the respective transform engine
    - Custom: input supplied as an argument in the CLI

#. I/O directories: file system which can be shared between multiple docker
   images and ultimately serve to transport the transformed content through the Transform workflow

    - Type: directory
    - Default: ``/hmd_transform/input``, ``/hmd_transform/output``

Project Structure:
+++++++++++++++++++
#. Docker:
    - *Dockerfile*: defines variables for the context and copies in the entrypoint script

    .. code-block:: dockerfile

        FROM python:3.9
        COPY requirements.txt ${FUNCTION_DIR}

        RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
            pip install -r requirements.txt

        ENV TRANSFORM_INSTANCE_CONTEXT default
        ENV TRANSFORM_NID default

        COPY entrypoint.py ${FUNCTION_DIR}
        ENTRYPOINT [ "python", "entrypoint.py" ]


    - *entrypoint.py*: the script used to import the python package

    .. code-block:: python

        from <repo_name>.<repo_name> import entry_point

        if __name__ == "__main__":
            entry_point(input_content_path, output_content_path, transform_nid, transform_instance_context)



#. Python:
    - *<module_name>.py*: the code to implement the transformation

    A basic structure is provided to set up logging, context variables and enable the entrypoint script to successfully
    import the python package. Additionally, a basic transform is defined under ``do_transform()`` in order to
    illustrate how the context is used and how the code is tested.

    .. code-block:: python

        import logging
        import sys
        import os
        from pathlib import Path

        logging.basicConfig(
            stream=sys.stdout,
            format="%(levelname)s %(asctime)s - %(message)s",
            level=logging.ERROR,
        )

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)


        def entry_point(input_content_path, output_content_path, transform_nid, transform_instance_context):
            # DO STUFF

#. Meta-data:
    - *manifest.json*: defined with a standard structure to support python and docker commands

#. Test:
    - Test_suite:
        - *01__transform_run.robot*: robot test template with a templated test case that runs the transform container in
          the local NeuronSphere environment with expected mounts and environment variables. 

        .. note::
            Proper sequencing of the files within the test suite is dependent upon the naming convention used.
            Specifically, the file names must start with ``01__``, ``02__``, ``03__``, etc. in order for robot to
            interpret the sequence correctly.

    - Running the robot tests:

        Use the code below to execute the test suite.

        .. code-block:: bash

            hmd bender