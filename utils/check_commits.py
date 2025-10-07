import os
import requests
from utils.consts import GITLAB_BASE_URL, HEADERS

OUTPUT_DIR = "commits"

def check_commits(project_name: str, project_id: int):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(OUTPUT_DIR, f"{project_name}.txt")

    all_commits = []
    page = 1

    while True:
        r = requests.get(
            f"{GITLAB_BASE_URL}/projects/{project_id}/repository/commits",
            headers=HEADERS,
            params={"per_page": 100, "page": page}
        )

        if r.status_code != 200:
            print(f"8.2. [{project_name}] Erreur lors de la récupération des commits : {r.text}")
            break

        commits = r.json()
        if not commits:
            break

        all_commits.extend(commits)

        next_page = r.headers.get("X-Next-Page")
        if not next_page:
            break
        page = int(next_page)

    with open(output_file, "w", encoding="utf-8") as f:
        for c in all_commits:
            sha = c["id"]
            message = c["title"].replace("\n", " ")
            f.write(f"{sha} | {message}\n")

    print(f"\n 8.2. [{project_name}] {len(all_commits)} commits exportés vers {output_file}")
