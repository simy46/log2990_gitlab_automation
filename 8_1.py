from utils.get_choice import get_choice
from utils.get_projects import get_projects
from utils.check_tag import check_tag
from utils.get_sprint import get_sprint


if __name__ == "__main__":
    choice = get_choice()
    sprint = get_sprint()
    PROJECTS = get_projects(choice)

    for project_name, project_id in PROJECTS.items():
        check_tag(project_name, project_id, sprint)