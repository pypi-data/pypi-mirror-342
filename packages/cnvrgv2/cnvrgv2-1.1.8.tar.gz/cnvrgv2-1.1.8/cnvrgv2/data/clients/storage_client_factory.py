import warnings

import urllib3

storage_clients_imports = [
    "from cnvrgv2.data.clients.s3.client import S3Storage",
    "from cnvrgv2.data.clients.azure.client import AzureStorage",
    "from cnvrgv2.data.clients.minio.client import MinioStorage",
    "from cnvrgv2.data.clients.gcp.client import GCPStorage"
]

for storage_client_import in storage_clients_imports:
    try:
        exec(storage_client_import)
    except Exception:
        continue

# Handle client-related warnings
# TODO: Move this somewhere else
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    from boto3.exceptions import PythonDeprecationWarning
    from urllib3.exceptions import InsecureRequestWarning
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)  # Sts download
    warnings.filterwarnings("ignore", category=PythonDeprecationWarning)  # Boto3
except Exception:
    pass


STORAGE_TYPE_GCS = "gcs"
STORAGE_TYPE_AZURE = "azure"
STORAGE_TYPE_S3 = "s3"
STORAGE_TYPE_MINIO = "minio"


def storage_client_factory(refresh_function):
    """
    Returns the relevant storage client depending on the storage meta got from the server
    @param refresh_function: Function that fetches dataset storage meta dictionary
    @return: storage client of type <BaseStorageClient>
    """
    storage_meta = refresh_function()

    if storage_meta is None:
        return None

    # TODO: Change all storage types to use refresh_function
    if storage_meta.get("storage") == STORAGE_TYPE_S3:
        return S3Storage(refresh_function, storage_meta=storage_meta)
    if storage_meta.get("storage") == STORAGE_TYPE_MINIO:
        return MinioStorage(storage_meta)
    if storage_meta.get("storage") == STORAGE_TYPE_AZURE:
        return AzureStorage(storage_meta)
    if storage_meta.get("storage") == STORAGE_TYPE_GCS:
        return GCPStorage(storage_meta)
