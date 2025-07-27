from file_work import read_text, write_text


def add_user(user_id: int, path: str):
    users = read_text(path)
    print(users)
    list_users = users.split("\n")
    int_users = [int(x) for x in list_users]
    print(int_users)
    if user_id not in list(users):
        int_users.append(user_id)
        write_text(path, int_users)
    else:
        print("User also added")
