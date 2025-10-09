import requests
from utils.consts import GITLAB_BASE_URL, HEADERS, MAIN_BRANCHES

def check_mr_on_small_branches(project_name: str, project_id: int):
    print(f"\n 8.4.1. [{project_name}] Vérification de l'utilisation des MR (branches principales vs secondaires)")

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

    main_branch_count = 0
    small_branch_count = 0
    small_branch_mrs = []

    for mr in mrs:
        target_branch = mr.get("target_branch", "").lower()
        mr_label = f"!{mr['iid']} ({target_branch})"
        if target_branch in MAIN_BRANCHES:
            main_branch_count += 1
        else:
            small_branch_count += 1
            small_branch_mrs.append(mr_label)

    total_mrs = main_branch_count + small_branch_count
    ratio_small = small_branch_count / total_mrs if total_mrs > 0 else 0

    print(f"    _Nombre de MR vers branches principales : {main_branch_count}")
    print(f"    _Nombre de MR vers branches secondaires : {small_branch_count}")

    if small_branch_mrs:
        print(f"    _MR vers petites branches : {', '.join(small_branch_mrs)}")

    print(f"    _Ratio MR vers petites branches : {ratio_small:.1%}")

    if ratio_small > 0.25:
        print("    _-0,25 les MR sont utilisées majoritairement entre petites branches. Astuce : git merge <branch-name> pour fusionner sous-branches entre elles, et MR uniquement pour fusionner vers la branche principale.")
    else:
        print("    _Ok.")
