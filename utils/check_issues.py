import requests
from utils.consts import GITLAB_BASE_URL, HEADERS
from collections import defaultdict

def check_issues(project_name: str, project_id: int):
    page = 1
    issues_open = []
    unassigned_by_section = defaultdict(list)
    sections_count = defaultdict(int)

    while True:
        r = requests.get(
            f"{GITLAB_BASE_URL}/projects/{project_id}/issues",
            headers=HEADERS,
            params={"per_page": 100, "page": page, "state": "opened"}
        )

        if r.status_code != 200:
            print(f"[{project_name}] Erreur lors de la récupération des issues : {r.text}")
            return

        issues = r.json()

        for issue in issues:
            iid = issue["iid"]
            labels = issue.get("labels", [])
            assignees = issue.get("assignees", [])

            section = labels[0] if labels else "Open"
            sections_count[section] += 1

            if not assignees:
                unassigned_by_section[section].append(f"#{iid}")

            if section == "Open":
                issues_open.append(f"#{iid}")

        next_page = r.headers.get("X-Next-Page")
        if not next_page:
            break
        page = int(next_page)

    print("\n-------------------------------------------------------------------------------------------|")
    print(f"[{project_name}] Vérification des issues ouvertes\n")

    if issues_open:
        nb_open = len(issues_open)
        penalty = min(nb_open * 0.1, 0.5)
        issues_str = ", ".join(issues_open)
        print(f"-{penalty:.1f} certains issues du sprint sont encore dans la colonne initiale \"open\" ({issues_str})")
    else:
        print("Aucune issue dans la colonne \"Open\".")