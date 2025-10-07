import requests
from utils.consts import GITLAB_BASE_URL, HEADERS

def check_tag(project_name: str, project_id: int, sprint: str, expected_commit: str = None):
    expected_tag = f"sprint{sprint}".lower()

    r = requests.get(
        f"{GITLAB_BASE_URL}/projects/{project_id}/repository/tags",
        headers=HEADERS,
        params={"per_page": 100}
    )

    if r.status_code != 200:
        print(f"    [{project_name}] Erreur lors de la récupération des tags : {r.text}")
        return

    tags = r.json()
    exact_match = None
    exact_sha = None

    for tag in tags:
        tag_name = tag["name"]
        tag_sha = tag["commit"]["id"]

        if tag_name.lower() == expected_tag:
            exact_match = tag_name
            exact_sha = tag_sha
            break

    print(f"\n 8.1. [{project_name}] Vérification des tags pour {expected_tag}")

    if not exact_match:
        print(f"    _-1 Absence du tag \"{expected_tag}\"")

        if tags:
            print("    _Tags existants dans le projet :")
            for t in tags:
                print(f"    _- {t['name']} → {t['commit']['id']}")
        else:
            print("    _(Aucun tag dans le projet)")
        return

    print(f"    _Tag trouvé : {exact_match} → {exact_sha}")

    if expected_commit and expected_commit != exact_sha:
        print(f"    _-1 Tag de déploiement \"{exact_match}\" pas sur le même commit que la remise")
    else:
        print("    _Ok.")
