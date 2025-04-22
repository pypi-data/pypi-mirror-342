transform_instance_name = "ms-transform"

provider_params = {"iso_date": "2024-02-12", "schema_name": "example_test"}

img_seq_params = [
    {
        "HMD_ENVIRONMENT": "default",
        "HMD_CUSTOMER_CODE": "default",
        "HMD_AUTH_TOKEN": "default",
        "TARGET_LIBRARIAN": "device",
        "SYNC_DIRECTION": "pull",
        "CONTENT_ITEM_PATH": "source:/2024-01-12/foo/example.csv",
        "FILE_PATH": "/hmd_transform/input/2024-02-12/foo/example.csv",
        "hmd_device_librarian_url": "default",
        "hmd_device_librarian_key": "testkey",
    },
    {
        "HMD_ENVIRONMENT": "default",
        "HMD_CUSTOMER_CODE": "default",
        "HMD_AUTH_TOKEN": "default",
        "INPUT_PATH": "/hmd_transform/input/2024-02-12/foo/example.csv",
        "OUTPUT_PATH": "/hmd_transform/output/2024-02-12/foo/example.csv",
    },
    {
        "HMD_ENVIRONMENT": "default",
        "HMD_CUSTOMER_CODE": "default",
        "HMD_AUTH_TOKEN": "default",
        "TARGET_LIBRARIAN": "datalake",
        "SYNC_DIRECTION": "push",
        "CONTENT_ITEM_TYPE": "example_csv"
        "CONTENT_ITEM_PATH": "final:/2024-01-12/foo/example.csv",
        "FILE_PATH": "/hmd_transform/output/2024-02-12/foo/example.csv",
        "hmd_datalake_librarian_url": "default",
        "hmd_datalake_librarian_key": "testkey",
    },
]
