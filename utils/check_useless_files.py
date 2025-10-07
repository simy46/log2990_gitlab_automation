import requests
from utils.consts import GITLAB_BASE_URL, HEADERS

UNWANTED_ROOT = {
    "node_modules",
    "coverage",
    "package.json",
    "yarn.lock",
}

SERVER_DIRS = {"server", "server-nest", "serveur"}

def check_useless_files(project_name: str, project_id: int):
    print("\n-------------------------------------------------------------------------------------------|")
    print(f"[{project_name}] Vérification des fichiers inutiles\n")

    r = requests.get(
        f"{GITLAB_BASE_URL}/projects/{project_id}/repository/tree",
        headers=HEADERS,
        params={"per_page": 100}
    )
    if r.status_code != 200:
        print(f"Erreur lors de la récupération des fichiers racine : {r.text}")
        return

    items = r.json()
    root_names = [item["name"] for item in items]

    penalty_count = 0

    for unwanted in UNWANTED_ROOT:
        if unwanted in root_names:
            penalty_count += 1
            print(f"-0,25 {unwanted} à la racine du projet")

    present_servers = [name for name in root_names if name.lower() in SERVER_DIRS]
    if len(present_servers) > 1:
        penalty_count += 1
        print(f"-0,25 Présence de plusieurs dossiers serveurs : {', '.join(present_servers)}") 

    if penalty_count == 0:
        print("Aucun fichier inutile détecté.")
