from utils.get_choice import get_choice
from utils.get_projects import get_projects
from utils.check_dead_branches import check_dead_branch


if __name__ == "__main__":
    choice = get_choice()
    PROJECTS = get_projects(choice)
    
    for project_name, project_id in PROJECTS.items():
        check_dead_branch(project_name, project_id)