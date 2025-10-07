from utils.get_choice import get_choice
from utils.get_projects import get_projects
from utils.check_mr_approvals import check_mr_approvals


if __name__ == "__main__":
    choice = get_choice()
    PROJECTS = get_projects(choice)

    for project_name, project_id in PROJECTS.items():
        check_mr_approvals(project_name, project_id)