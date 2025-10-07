from utils.get_choice import get_choice
from utils.get_sprint import get_sprint
from utils.get_projects import get_projects
from utils.check_tag import check_tag
from utils.check_commits import check_commits
from utils.check_useless_files import check_useless_files
from utils.check_dead_branches import check_dead_branch
from utils.check_mr_approvals import check_mr_approvals
from utils.check_issues import check_issues

if __name__ == "__main__":
    try:
        choice = get_choice()
        sprint = get_sprint()
        PROJECTS = get_projects(choice)

        print("\n===========================================================================================|")
        print(f"DÉBUT DE LA CORRECTION POUR LE GROUPE {choice}")
        print("===========================================================================================|")

        for project_name, project_id in PROJECTS.items():
            print("\n===========================================================================================|")
            print(f" {project_name}")
            print("===========================================================================================|")

            check_tag(project_name, project_id, sprint)
            check_commits(project_name, project_id)
            check_dead_branch(project_name, project_id)
            check_mr_approvals(project_name, project_id)
            check_issues(project_name, project_id)
            check_useless_files(project_name, project_id)

    except Exception as e:
        print(f"\n{e}")
        print("Tu as surement oublié de set le GITLAB_TOKEN dans /utils/consts.py")
        print("Voir README.md pour les étapes à suivre")