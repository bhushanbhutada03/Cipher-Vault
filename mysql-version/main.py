import json
from db import (
    insert_password,
    fetch_all_passwords,
    update_password_db,
    delete_password_db,
    fetch_by_website,
)

key = 123
pin = 6969


def list_all_saved_websites():
    rows = fetch_all_passwords()

    if not rows:
        print("No passwords saved yet.")
        return []

    for index, row in enumerate(rows, start=1):
        print(f"{index}. Website: {row[1]} | Username: {row[2]}")

    return rows


def add_new_password():
    website = input("Enter new Website : ")
    username = input("Enter new Username : ")
    password = pass_to_cipher(input("Enter new Password : "))

    insert_password(website, username, password)

    print("Password added successfully\n")


def update_password():
    rows = list_all_saved_websites()

    if not rows:
        return

    choice = input("Enter choice to update: ")

    if not choice.isdigit():
        print("Invalid input!")
        return

    choice = int(choice)

    if 1 <= choice <= len(rows):
        id = rows[choice - 1][0]

        newPass = pass_to_cipher(input("Enter new Password: "))
        update_password_db(id, newPass)
        print("Password Updated successfully\n")
    else:
        print("Invalid choice")


def delete_password():
    rows = list_all_saved_websites()

    if not rows:
        return

    choice = input("Enter choice to delete: ")

    if not choice.isdigit():
        print("Invalid input! Enter a number.")
        return

    choice = int(choice)

    if 1 <= choice <= len(rows):
        id = rows[choice - 1][0]
        delete_password_db(id)
        print("Deleted successfully\n")
    else:
        print("Invalid choice")


def Access_password():
    rows = list_all_saved_websites()

    if not rows:
        return

    p = input("Enter correct Pin : ")

    if not p.isdigit():
        print("Invalid PIN format\n")
        return

    p = int(p)

    if p != pin:
        print("Invalid PIN")
        return

    choice = input("Enter choice for Accessing Password : ")

    if not choice.isdigit():
        print("Invalid input\n")
        return

    choice = int(choice)

    if 1 <= choice <= len(rows):
        cipher = rows[choice - 1][3]
        username = rows[choice - 1][2]

        password = cipher_to_pass(cipher, p)
        print(f"Password for {username} is {password}")
    else:
        print("Invalid choice\n")


def search_by_website():
    website = input("Enter website to search: ").strip()

    if not website:
        print("Invalid input\n")
        return

    rows = fetch_by_website(website)

    if not rows:
        print("No records found")
        return

    for i, row in enumerate(rows, start=1):
        print(f"{i}. Website: {row[1]} | Username: {row[2]}")


def pass_to_cipher(password):
    arr = []
    for ch in password:
        arr.append(ord(ch) ^ key)
    return json.dumps(arr)


def cipher_to_pass(cipher, p):
    if p == pin:
        cipher = json.loads(cipher)
        arr = []
        for i in cipher:
            arr.append(chr(i ^ key))
        return "".join(arr)
    else:
        print("Incorrect PIN!\n")
        return None


def main():
    while True:
        print("\n Cipher Vault | Select a Valid Option")
        print("1. List All Saved Website Passwords")
        print("2. Add a New Password")
        print("3. Update an Existing Password")
        print("4. Delete a Password")
        print("5. Access (View) a Password")
        print("6. Search Passwords by Website")
        print("7. Exit the Program \n")

        ip = input("Enter your Choice :  ")

        match ip:
            case "1":
                list_all_saved_websites()
            case "2":
                add_new_password()
            case "3":
                update_password()
            case "4":
                delete_password()
            case "5":
                Access_password()
            case "6":
                search_by_website()
            case "7":
                break
            case _:
                print("Please Enter Valid Choice !")


if __name__ == "__main__":
    main()
