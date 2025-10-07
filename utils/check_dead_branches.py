import requests
from datetime import datetime, timedelta
from utils.consts import GITLAB_BASE_URL, HEADERS

def check_dead_branch(project_name: str, project_id: int, weeks: int = 3):
    print(f"\n 8.3. [{project_name}] Vérification des branches mortes")

    cutoff_date = datetime.utcnow() - timedelta(weeks=weeks)
    stale_branches = []
    total_branches = 0
    page = 1

    while True:
        r = requests.get(
            f"{GITLAB_BASE_URL}/projects/{project_id}/repository/branches",
            headers=HEADERS,
            params={"per_page": 100, "page": page}
        )

        if r.status_code != 200:
            print(f"    -Erreur lors de la récupération des branches : {r.text}")
            return

        branches = r.json()
        if not branches:
            break

        for b in branches:
            branch_name = b["name"]
            total_branches += 1

            if branch_name in ("main", "master", "dev"):
                continue

            committed_date_str = b["commit"]["committed_date"]
            committed_date = datetime.strptime(
                committed_date_str, "%Y-%m-%dT%H:%M:%S.%f%z"
            ).astimezone().replace(tzinfo=None)

            if committed_date < cutoff_date:
                stale_branches.append(branch_name)

        next_page = r.headers.get("X-Next-Page")
        if not next_page:
            break
        page = int(next_page)

    print(f"    _Nombre total de branches : {total_branches}")

    if stale_branches:
        branches_str = ", ".join(stale_branches)
        print(f"    _-1 présence de branche morte [{branches_str}]")
    else:
        print("    _Ok.")
