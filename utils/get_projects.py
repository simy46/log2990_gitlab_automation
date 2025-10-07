import requests
from utils.consts import GITLAB_BASE_URL, HEADERS, COURSE_CODE, SESSION


def get_projects(prefix: str): # should probably cache to improv performance
    group_path = f"polytechnique-montr-al/{COURSE_CODE}/{SESSION}"
    group_url = f"{GITLAB_BASE_URL}/groups/{requests.utils.quote(group_path, safe='')}"
    group_resp = requests.get(group_url, headers=HEADERS)
    group_resp.raise_for_status()
    group_id = group_resp.json()["id"]

    projects = {}
    page = 1
    while True:
        params = {
            "include_subgroups": True,
            "per_page": 100,
            "page": page
        }
        r = requests.get(f"{GITLAB_BASE_URL}/groups/{group_id}/projects", headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()

        for p in data:
            name = p["name"]
            if name.startswith(f"{COURSE_CODE}-{prefix}"):
                projects[name] = p["id"]

        next_page = r.headers.get("X-Next-Page")
        if not next_page:
            break
        page = int(next_page)

    print("\nProjets récoltés :")
    for name, pid in sorted(projects.items()):
        print(f"{name} -> {pid}")

    return projects