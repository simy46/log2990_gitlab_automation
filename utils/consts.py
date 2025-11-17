COURSE_CODE = "LOG2990"
SESSION = "20253"

GITLAB_BASE_URL = "https://gitlab.com/api/v4"
GITLAB_TOKEN = "dont push you secret key" # check readme 
HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN} 

# for development
OUTPUT_DIR = "commits"

# check_dead_branches.py and check_mr_on_small_branches.py
MAIN_BRANCHES = {"main", "master", "prod", "qa", "dev", "dev-temp", "temp-dev"} # check with real SWE


# check_useless_files.py
UNWANTED_ROOT = {
    "node_modules",
    "coverage",
    "package.json",
    "yarn.lock",
}
SERVER_DIRS = {"server", "server-nest", "serveur"}

# deploy tag prefix
DEPLOY_PREFIX = "deploy"