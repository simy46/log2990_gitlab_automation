import requests
from utils.consts import GITLAB_BASE_URL, HEADERS

def check_mr_approvals(project_name: str, project_id: int):
    print(f"\n 8.4.1. [{project_name}] Vérification des approbations de MR")

    mr_url = f"{GITLAB_BASE_URL}/projects/{project_id}/merge_requests?state=merged&per_page=100"
    mrs = requests.get(mr_url, headers=HEADERS).json()

    if not isinstance(mrs, list):
        print(f"    _Erreur lors de la récupération des MRs : {mrs}")
        return

    total_mrs = len(mrs)
    no_approval_mrs = []

    for mr in mrs:
        mr_iid = mr["iid"]
        title = mr["title"]
        state = mr["state"]
        mr_label = f"!{mr_iid}"

        approvals_url = f"{GITLAB_BASE_URL}/projects/{project_id}/merge_requests/{mr_iid}/approvals"
        approvals = requests.get(approvals_url, headers=HEADERS).json()

        approved_by = approvals.get("approved_by", [])
        nb_approvals = len(approved_by)

        if nb_approvals <= 0:
            no_approval_mrs.append(mr_label)
            print(f"    _-{mr_label} [{state}] : \"{title}\" n'a aucune approbation")

    if total_mrs == 0:
        print(f"    _Aucune MR fusionnée pour {project_name}.")
        print(f"    _-0,5 aucune MR n'a été \"Merged\", cela démontre une compréhension lacunaire de l'outil")
    else:
        no_approval_count = len(no_approval_mrs)
        percentage_no_approval = (no_approval_count / total_mrs) * 100
        print(f"\n    {no_approval_count}/{total_mrs} MR(s) sans approbation ({percentage_no_approval:.1f}%)")

        if no_approval_count > 1: # si au moins deux MR fusionnées n'a pas été approuvées
            mr_list_str = ", ".join(no_approval_mrs)
            print(f"    _-0,25 les MR fusionnées ne sont pas majoritairement approuvées ({mr_list_str}). Astuce: Assignez un nombre minimal d'approvals par défaut (préférablement au moins 2 reviewers).")
        else:
            print("    _Ok.")
