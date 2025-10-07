from utils.get_choice import get_choice
from utils.get_projects import get_projects
from utils.check_issues import check_issues


if __name__ == "__main__":
    choice = get_choice()
    PROJECTS = get_projects(choice)

    for project_name, project_id in PROJECTS.items():
        check_issues(project_name, project_id)