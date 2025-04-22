# GLOBAL
NO_FILE = "File not found. Please check the file path"
NO_DIR = "Directory not found"

# VALIDATIONS
FAULTY_KEY = 'Faulty key {0}'
FAULTY_VALUE = 'Faulty value {0}'
MISSING_REQUIRED_VALUE = 'Missing required value {0}'
INVALID_CHARACTERS_IN_INPUT = 'Invalid characters in {0}'

INVALID_URL = 'URL is invalid'
INVALID_EMAIL = 'Email is invalid'
INVALID_CREDENTIALS = "Could not login using the provided credentials, please check your credentials and try again"

# ORGANIZATION
ORGANIZATION_DOESNT_EXIST = "The requested organization does not exist"

# PROXY
PROXY_HTTP_ERROR = "A server error has occurred."
PROXY_UNAUTH_ERROR = "Unauthorized to perform this action."
PROXY_EMPTY_RESPONSE = "Cannot convert empty response to json"
PROXY_NOT_FOUND_ERROR = "The requested resource could not be found."

# USER
USER_EMPTY_TOKEN = "Can't Login using an empty token"
USER_LOGIN_FAILED = "Can't Authenticate using the provided username and password"
USER_NO_ORGANIZATION = "Please join an organization before using the SDK"

# CONTEXT
CONTEXT_CANT_SAVE = "Can't save context without domain username and organization"
CONTEXT_BAD_ARGUMENTS = "Please provide domain, username and password or token together."
CONTEXT_BAD_ENV_VARIABLES = "Can't authenticate using environment variables/config"

CONTEXT_SCOPE_BAD_SCOPE = "Cannot connect to {0}, please provide a slug"
CONTEXT_SCOPE_BAD_DEPENDENCIES = "Cannot connect to {0} since no {1} is present"

# IMAGE
IMAGE_BAD_TAG = "Image tag is invalid"
IMAGE_BAD_NAME = "Image name is invalid"
IMAGE_BAD_LOGO = "Image logo is not supported"
IMAGE_BAD_REGISTRY = "Image registry must be a string"
IMAGE_GET_FAULTY_PARAMS = "Cannot get image. Please provide a slug or image name and tag (all strings)."
IMAGE_CUSTOM_DOCKERFILE_REQUIRED = "Custom image requires a dockerfile"

# LABELS
LABEL_BAD_NAME = "Label name is invalid"
LABEL_BAD_KIND = "Label kind is invalid"
LABEL_BAD_COLOR = "Label color is invalid"
LABEL_NOT_FOUND = "Label not found"

# REGISTRY
REGISTRY_BAD_URL = "Registry url must be a string"
REGISTRY_BAD_URL_FORMAT = "Bad registry url format (example: good-url.io)"
REGISTRY_BAD_TYPE = "Registry type is not supported"
REGISTRY_BAD_TITLE = "Registry title must be a string"
REGISTRY_BAD_USERNAME = "Registry username must be a string"
REGISTRY_BAD_PASSWORD = "Registry password must be a string"
REGISTRY_USERNAME_AND_PASSWORD = "Please provide both username and password or neither"

# STORAGE_CLASS
STORAGE_CLASS_GET_FAULTY_PARAMS = "Cannot get Storage Class. Please provide a slug or Storage Class."
NOT_A_STORAGE_CLASS_OBJECT = "The given argument is not a Storage Class object. please provide a Storage Class object."
INVALID_STORAGE_CLASS_TITLE = "Title should contain only lowercase letters, numbers, and hyphens."

# VOLUME
VOLUME_GET_FAULTY_PARAMS = "Cannot get volume. Please provide a slug or volume name."
NOT_A_VOLUME_OBJECT = "The given argument is not a Volume object. please provide a Volume object."
INVALID_VOLUME_TITLE = "Title should contain only lowercase letters, numbers, and hyphens."

# COMMIT
COMMIT_FAULTY_SHA1 = "Commit sha1 must be a string"
LOCAL_COMMIT_DOESNT_EXIST_ERROR = "Local commit does not exist. Can't save config"

# PROJECT
PROJECT_GET_FAULTY_SLUG = "Cannot get project with empty slug or a non string slug"
PROJECT_CREATE_FAULTY_NAME = "Cannot create project with empty/non-string name"
PROJECT_ALREADY_CLONED = "Project already cloned"

# LIBRARY
LIBRARY_GET_FAULTY_SLUG = "Cannot get library with empty slug or a non string slug"

# DATASET
DATASET_GET_FAULTY_SLUG = "Cannot get dataset with empty slug or a non string slug"
DATASET_CREATE_FAULTY_NAME = "Cannot create dataset with empty/non-string name"
DATASET_CREATE_FAULTY_CATEGORY = "Cannot create dataset with empty/non-string category"
DATASET_CREATE_FAULTY_CATEGORY_VALUE = "Dataset category must be one of [general, images, audio, video, text, tabular]"
NOT_A_DATASET_LIST_OBJECT = "datasets must be a list of datasets objects"
NOT_A_DATASET_OBJECT = "dataset parameter missing or not a dataset object"
NOT_A_VALID_DIRECTORY_NAME = "{} is invalid directory name, should contain letters, numbers, '_' , '-' "

# QUERY
QUERY_GET_FAULTY_SLUG = "Cannot get query with empty slug or a non string slug"
QUERY_CREATE_FAULTY_NAME = "Cannot create query with empty/non-string name"
QUERY_CREATE_FAULTY_QUERY = "Cannot create query with empty/non-string query"
QUERY_LIST_FAULTY_PARAMS = "Cannot list with {0}"

# ORGANIZATION
ORGANIZATION_GET_FAULTY_SLUG = "Cannot get organization with empty slug or a non string slug"
ORGANIZATION_CREATE_FAULTY_NAME = "Cannot create organization with empty name or a non string name"
ORGANIZATION_NOT_FOUND = "Organization not found"

# MACHINES
MACHINE_GET_FAULTY_SLUG = "Cannot get machine with empty slug or a non string slug"
MACHINE_GPU_VALUES_WITHOUT_GPU = 'Cannot set gpu values to a non gpu enabled machine'

# SPARK DRIVERS
SPARK_DRIVER_GET_FAULTY_SLUG = "Cannot get spark driver with empty or a non string slug"

# CLUSTER
CLUSTER_GET_FAULTY_SLUG = 'Cannot get cluster with empty or a non string slug'
CLUSTER_ONE_TYPE = 'The given arguments: {} and {} cannot be sent together'

# TEMPLATES
TEMPLATE_GET_FAULTY_SLUG = "Cannot get template with empty slug or a non string slug"
TEMPLATE_FAULTY_MIG_VALUE = 'Mig device must be one of the following: [mig-1g.5g, mig-2g.20g, mig-3g.25g]'
TEMPLATE_FAULTY_GPU = 'Faulty gpu or worker gpu count {0}'
TEMPLATE_FAULTY_MIG = 'Faulty mig value {0}'
TEMPLATE_FAULTY_TYPE = 'Kube template type must be one of the following: [regular, mpi, kubernetes, pytorch, ' \
                       'spark_on_kubernetes,ray,ray_modin] '

# CLONE
CONFIG_YAML_NOT_FOUND = "Couldn't find config file. Please clone project/dataset before syncing."
NOT_ENOUGH_SPACE = "Not enough space on disk to download dataset commit"

# EXPERIMENT
MISSING_EXPERIMENT_ARGUMENT = "The function sent as command must get experiment as an argument"
EXPERIMENT_CANNOT_BE_A_FUNCTION = "Function as command is supported in local experiments only." \
                                  " Add local=True or send a string command instead"
EXPERIMENT_MISSING_COMMAND_ARGUMENT = "Command Cannot be blank"
EXPERIMENT_FAULTY_PARAMETERS_INT = "Discrete values may only contain numbers"
EXPERIMENT_FAULTY_PARAMETERS_LIST = "Values must be of a type list"
EXPERIMENT_FAULTY_PARAMETERS_VALUES = "values cannot be empty"
EXPERIMENT_FAULTY_PARAMETERS_STEPS = "The given parameters must be a list of lists of integers"
EXPERIMENT_FAULTY_PARAMETERS_KEY = "Key cannot be empty"
EXPERIMENT_FAULTY_PARAMETERS = "Steps should be positive integer"
EXPERIMENT_FAULTY_PARAMETERS_TYPE = "Ensure the type is: [discrete, float, integer, categorical]."
EXPERIMENT_DUPLICATE_PARAMETERS = "Duplicate keys in parameters {0}"

# ENDPOINT
ENDPOINT_NOT_RUNNING = "Endpoint {0} is not running"
ENDPOINT_UPDATE_TIMEOUT = "Update endpoint {0} timeout"

# WORKFLOW
WORKFLOW_FINAL_STATE = "Workflow reached a final state {0}, different from desired one"

# WEBAPP
EXPERIMENT_SLUGS_NOT_FOUND = "Experiments slugs not found"

# FLOW
FLOW_GET_FAULTY_SLUG = "Cannot get flows with empty slug or a non string slug"
FLOW_GET_FAULTY_YAML = "Yaml is not valid"
FLOW_GET_FAULTY_INPUT = "Only one parameter is expected. Please resend the request with only one parameter"

# FLOW_VERSION
FLOW_VERSION_GET_FAULTY_SLUG = "Cannot get flows version with empty slug or a non string slug"

# CRON
CRON_ARGUMENTS_MISSING = "Invalid cron syntax. Cron string must contain at least five arguments (format: * * * * *)"
CRON_INVALID_ARGUMENT = "Invalid cron syntax. Cron string accepts * and natural numbers. Optional timezone is a string"
CRON_INVALID_TIMEZONE = "Given timezone does not exist"

# ARGUMENTS
ARGUMENT_BAD_TYPE = "Wrong attribute type, expected {0}, got {1}"
SERIES_NOT_A_LIST = "Series must be a list"
BOTH_GROUP_AND_STEP = "Must include step when using group and visa versa"
ONLY_HEATMAP_CAN_HAVE_GROUPS = "Only Heatmaps support groups and steps"
SERIES_NOT_A_HEATMAP = "Heatmap series must be composed of tuples of the same length made of real numbers"
SERIES_NOT_A_VALID_LIST = "Series must only have real numbers"
EMPTY_KAFKA_BROKERS_LIST = "Must be a list containing one broker url or more"
EMPTY_KAFKA_INPUT_TOPICS = "Must be a list containing one topic or more"
EMPTY_ARGUMENT = "{} cannot be empty"
NOT_LIST = "{} is not a list"
INVALID_CRON_ARGUMENT = "{0} must be a number between {1} and {2}"
FILE_TOTAL = "File total is mandatory for azure callback. Please provide a mutable counter - list containing zero [0]"
NOT_SUPPORTED = "{} are not supported"
SECRETS_NOT_SUPPORTED = "{} are not supported, use update_secret or delete_secret methods"

# GIT
CANT_USE_BOTH_SSH_AND_TOKEN = "Can't use both SSH and Token for authentication with git"
INVALID_SSH_KEY_TYPE = "SSH Key Type needs to be plain/file"
CANT_READ_SSH_KEY_FILE = "Can't read SSH key file"

# CLI - CONFIG FILE
CONFIG_FILE_MISSING = "Config file doesn't exist."
LOCAL_CONFIG_MISSING_DATA_OWNER_SLUG = "Cannot preform operation. Couldn't find project or dataset name" \
                                       " in local config file. Try cloning the project or dataset first."

# CLI - CREDENTIALS
CREDENTIALS_MISSING = "Some credentials are missing. Cannot authenticate, try logging in first."

# CLI - PROJECT
DIRECTORY_ALREADY_LINKED = "Directory is already linked to {0}"
NOT_A_GIT_PROJECT = "Project {0} is not a git project"
PROJECT_NOT_EXIST = "Project {0} is not a cnvrg project"

# CLI - MEMBERS
MEMBER_NOT_VALID_ROLE = "{0} is not a valid role, valid roles are: admin, manager, member, reviewer"

# CLI - SSH
SSH_FAILED_TO_START = "Failed to start ssh. Ssh status: {0}"
SSH_FAILED_GET_REQUIRED_PARAMS = "Failed to get required ssh params. Ssh status: {0}"

# DATASOURCES
DATASOURCE_GET_FAULTY_SLUG = "Cannot get data source with empty slug or a non string slug"
DATASOURCE_NOT_VALID_PARAM = "{0} is not a valid {1}"
DATASOURCE_FAULTY_STORAGE_TYPE = "storage type is not valid. Valid types are : {0}"
DATASOURCE_BAD_FORCE_ARGUMENTS = "Force and skip_if_exists cannot both be set to true"
DATASOURCE_ALREADY_CLONED = "The datasource is already cloned"
