import requests
from utils.consts import GITLAB_BASE_URL, HEADERS, DEPLOY_PREFIX

def check_tag(project_name: str, project_id: int, sprint: str):
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
    sprint_sha = None

    for tag in tags:
        if tag["name"].lower() == expected_tag:
            exact_match = tag["name"]
            sprint_sha = tag["commit"]["id"]
            break

    print(f"\n 8.1. [{project_name}] Vérification des tags pour {expected_tag}")

    if not exact_match:
        print(f"    _-1 Absence du tag \"{expected_tag}\"")
        if tags:
            print("        _Tags existants dans le projet :")
            for t in tags:
                print(f"            _- {t['name']} → {t['commit']['id']}")
        else:
            print("            _(Aucun tag dans le projet)")
        return

    print(f"    _Tag trouvé : {exact_match} → {sprint_sha}")

    deploy_tags = []
    deploy_match_found = False

    for tag in tags:
        tag_name = tag["name"].lower()
        tag_sha = tag["commit"]["id"]

        if tag_name.startswith(DEPLOY_PREFIX):
            deploy_tags.append((tag_name, tag_sha))
            if tag_sha == sprint_sha:
                deploy_match_found = True

    if deploy_tags:
        print("    _Tags de déploiement trouvés :")
        for name, sha in deploy_tags:
            print(f"        _- {name} → {sha}")
    else:
        print("    _(Aucun tag de déploiement trouvé)")

    if not deploy_match_found:
        print(f"    _-1 Tag de déploiement pas sur le même commit que {expected_tag}")
        print(f"        _Commit attendu : {sprint_sha}")
        return

    print("    _Ok (un tag de déploiement pointe bien sur le même commit).")
