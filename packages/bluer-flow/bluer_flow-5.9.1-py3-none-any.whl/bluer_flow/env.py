from bluer_options.env import load_config, load_env, get_env

load_env(__name__)
load_config(__name__)


BLUER_FLOW_DEFAULT_WORKFLOW_PATTERN = get_env("BLUER_FLOW_DEFAULT_WORKFLOW_PATTERN")
