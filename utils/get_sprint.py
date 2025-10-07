def get_sprint() -> str:
    while True:
        sprint = input("Entrez le nom du sprint (1, 2 ou 3). Utilisé seulement pour la vérification du tag: ").strip()
        if sprint in ["1", "2", "3"]:
            return sprint
        else:
            print("Entrée invalide. Veuillez entrer un nom de sprint valide (1, 2, 3).")