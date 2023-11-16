def get_token_from_file(filename):
    try:
        with open(filename, 'r') as file:
            token = file.readline().strip()
        return token
    except FileNotFoundError:
        print(f"Пользователь {filename} не найден.")
        return None