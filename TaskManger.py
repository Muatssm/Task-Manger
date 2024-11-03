import mysql.connector
import os
import time
from typing import Union


def select(query: str, fetch: str) -> Union[tuple, None]:
                result = None
                cursor.execute(query)
                if fetch == "all":
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()

                return result


class tasks_operations():
    def __init__(self, account: tuple):
            self.account: tuple = account
            self.table_tasks_name: str = "tasks"

    def add_task(self, title: str = None, description: str = None, status: str = None) -> str:

        org_dict = {
            "title": None,
            "description": None,
            "status": None,
            "task_user_id": None
        }
        valueslist = [title, description, status, self.account[0]]
        list_dict_keys = list(org_dict.keys())
        for i in range(0, len(list_dict_keys)):
            if valueslist[i] is None:
                del org_dict[list_dict_keys[i]]
            else:
                org_dict[list_dict_keys[i]] = valueslist[i]

        values_ListToStr = str(tuple(org_dict.values()))

        Keys_ListToStr = list(org_dict.keys())
        Keys_ListToStr = ", ".join(Keys_ListToStr)
        Keys_ListToStr = Keys_ListToStr.replace("'", "`")
                    
        query = f"INSERT INTO {self.table_tasks_name} ({Keys_ListToStr}) VALUES{values_ListToStr};"
        try:
            cursor.execute(query)
            conn.commit()
            return "Added Successfully"
        except Exception as e:
            return f"There Was An Error {e}"
                
    def get_tasks_list(self) -> list:
        query: str = f"SELECT * FROM {self.table_tasks_name} WHERE task_user_id={account[0]};" if self.account[-1] == "user" else f"SELECT task_id, title, description, status, created_at, username FROM {self.table_tasks_name} INNER JOIN users WHERE {self.table_tasks_name}.task_user_id = users.user_id;"
        results = select(query, "all")
        if results is None:
            return []
        else:
            tasks_list: list = []
            if self.account[-1] == "user":
                for i in results:
                    task_dict: dict = {
                        "task_id":  None,
                        "title": None,
                        "description": None,
                        "status":None,
                        "created_at": None,
                        "task_user_id": self.account[0]
                    }
                    task_dict["task_id"], task_dict["title"], task_dict["description"], task_dict["status"], task_dict["created_at"], task_dict["task_user_id"] = i
                    tasks_list.append(task_dict)

            else:
                for i in results:
                    task_dict: dict = {
                        "task_id":  None,
                        "title": None,
                        "description": None,
                        "status":None,
                        "created_at": None,
                        "username": None,
                    }
                    task_dict["task_id"], task_dict["title"], task_dict["description"], task_dict["status"], task_dict["created_at"], task_dict["username"] = i
                    tasks_list.append(task_dict)

            return tasks_list
                    
    def update_task_info(self, task_id: int, update_column: str, update_to_value: Union[str, int]) -> str:
        try:
            update_to_value = f"'{update_to_value}'" if isinstance(update_to_value, str) else update_to_value
            query = f"UPDATE `{self.table_tasks_name}` SET `{update_column}` = {update_to_value} WHERE task_id={task_id}"
            cursor.execute(query)
            conn.commit()
            return "Updated Successfully"
        except Exception as e:
            return f"There Was An Error {e}"

    def delete_task(self, task_id: int) -> str:
        try:
            query = f"DELETE FROM {self.table_tasks_name} WHERE task_id={task_id}"
            cursor.execute(query)
            conn.commit()
            return "Deleted Successfully"
        except Exception as e:
            return f"There Was An Error {e}"


if __name__ == "__main__":
    try:
        conn = mysql.connector.connect(host="localhost", user="root", database="task_manger")
        choices_msg: str = "1 - Add New Task\n2 - Update Task Status\n3 - Delete Task\n4 - Show Tasks List\n5 - Quit from the program"
        if conn.is_connected():
            cursor = conn.cursor()
            welcome_message: str = "Welcome to Your Task Manger "
            account_choice_msg: str = "Enter (1) To login Or (2) To sign up : "
            print(welcome_message)

            account_choice: str = input(account_choice_msg)
            account_choice: int = int(account_choice) if account_choice.isdigit() and account_choice in ["1",
                                                                                                         "2"] else None
            while not account_choice:
                print("error please Enter A accepted number [1 or 2]")
                os.system("cls")
                print(welcome_message)
                account_choice = input(account_choice_msg)
                account_choice: int = int(account_choice) if account_choice.isdigit() and account_choice in ["1",
                                                                                                             "2"] else None
            account: tuple = ()
            print("-" * 50)
            permessions = False
            if account_choice == 1:
                while True:
                    email = input("Enter Your Email : ")
                    password = input("Enter Your Password : ")
                    query: str = f"SELECT * FROM users WHERE email='{email}' AND password='{password}' ;"

                    result = select(query, "one")
                    if result is not None:
                        break
                    else:
                        print("There Is No Account Has This Email And Password")

                if result[-1] in ["admin", "owner"]:
                    permessions = True
                account = result

            else:
                username = input("Enter Your Username: ")
                email = input("Enter Your Email : ")
                password = input("Enter Your Password (More or equal 8 characters) : ")
                while len(password) > 12 or len(password) < 8:
                    print("Please Enter A password less than 12 characters And more or equal 8 characters")
                    password = input("Enter Your Password (More or equal 8 characters) : ")

                cursor.execute(
                    f"INSERT INTO users (`username`, `email`, `password`) VALUES('{username}', '{email}', '{password}');")
                conn.commit()
                query: str = f"SELECT * FROM users WHERE username='{username}'  ;"

                result = select(query, "one")
                account = result

            os.system("cls")
            print(f"Welcome {account[1]} To Task Manger")

            while True:
                print("-" * 50)
                user_operations_object: tasks_operations = tasks_operations(account)
                print(choices_msg)
                choice = input("Enter Your Choice : ")
                if not choice.isdigit() or int(choice) not in [1,2,3,4,5]:
                    print("Please Enter A correct Input (1, 2, 3, 4, 5)")
                else:
                    choice = int(choice)
                print("-" * 50)
                if choice == 1:
                    title: str = input("Enter Your Task Title (Press Enter To Skip) (Max 40 Char): ")
                    description: str = input("Enter Your Task Description (Press Enter To Skip) (Max 70 Char): ")
                    status: str = input("Enter Your Task Status (Press Enter To Skip) (Max 45 Char): ")                    
                    title = None if title == "" else title
                    description = None if description == "" else description
                    status = None if status == "" else status
                    accepted_or_rejected = user_operations_object.add_task(title, description, status)
                    print("-"*50+f"\nTask Info \nTask Title: {'Normal Task' if title==None else title} \nTask Description: {'No Description' if description==None else description}\nTask Status: {'Pending' if status==None else status}\n{accepted_or_rejected}")
                elif choice in [2, 3, 4]:
                    user_tasks_list = user_operations_object.get_tasks_list()
                    for idx, value in enumerate(user_tasks_list):
                        normal_msg = f"{idx+1} - Task Title: {value['title']}\n  | Task Description: {value['description']}\n  | Task Status: {value['status']}\n  | Created At: {value['created_at']}"
                        tasks_msgs = normal_msg if not permessions else normal_msg + f"\n  | User Task: {value['username']}"
                        print(tasks_msgs)

                    if not user_tasks_list:
                        print("There Was No Tasks To Updata its status")
                    else:
                        if choice == 2:
                            print("-"*50)
                            idx = int(input("Choice The Number Of The Task That You Want To Change its Status : "))
                            idx = idx-1
                            new_status = input("Enter Your New Status (Max 45 Char) : ")
                            task_id = user_tasks_list[idx]["task_id"]
                            chick = user_operations_object.update_task_info(task_id, "status", new_status)
                            print(chick)
                        elif choice == 3:
                            print("-"*50)
                            idx = int(input("Choice The Number Of The Task That You Want To Delete it : "))
                            idx = idx-1
                            task_id = user_tasks_list[idx]["task_id"]
                            chick = user_operations_object.delete_task(task_id)
                            print(chick)
                elif choice == 5:
                    break






    except Exception as e:
        print(f"There was an error : {e}")

    finally:
        if conn.is_connected():
            conn.commit()
            cursor.close()
            conn.close()
