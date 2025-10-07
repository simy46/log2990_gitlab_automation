def get_choice() -> str:
    while True:
        choice = input("Choisissez la section (1 ou 2) : ")
        if choice in ['1', '2']:
            return choice
        else:
            print("Entrée invalide. Veuillez entrer 1 ou 2.")