import requests
from utils.consts import GITLAB_BASE_URL, HEADERS, MAIN_BRANCHES


def check_mr_on_small_branches(project_name: str, project_id: int):
    print(f"\n 8.4.1. [{project_name}] Vérification des MR vers branches secondaires")

    mrs_resp = requests.get(
        f"{GITLAB_BASE_URL}/projects/{project_id}/merge_requests",
        headers=HEADERS,
        params={"state": "merged", "per_page": 100}
    )

    if mrs_resp.status_code != 200:
        print(f"    _Erreur lors de la récupération des MRs : {mrs_resp.text}")
        return

    mrs = mrs_resp.json()
    if not isinstance(mrs, list) or not mrs:
        print("    _Aucune MR fusionnée.")
        return

    small_branch_mrs = []
    for mr in mrs:
        target_branch = mr.get("target_branch", "")
        if target_branch.lower() not in MAIN_BRANCHES:
            small_branch_mrs.append(f"!{mr['iid']} ({target_branch})")

    if small_branch_mrs:
        print(f"    _-0,25 les MR sont utilisées entre petites branches ({', '.join(small_branch_mrs)}). Astuce : git merge <branch-name> pour fusionner sous-branches entre elles, et MR uniquement pour fusionner vers la branche principale.")
    else:
        print("    _Ok.")
