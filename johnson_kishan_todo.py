import argparse
import json
import os

#code to define a class to manage the todo list
class TodoList:
    def __init__ (self, file_name = "TODO.json"):
        self.file_name = file_name
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists (self.file_name):
            with open (self.file_name, "r") as f:
                return json.load(f)
            return [] #will return an empty list if the file doesn't exist
        
    def save_tasks(self):
        with open(self.file_name, "w") as f:
            json.dump(self.tasks, f, indent = 2)

    def list_tasks(self):
        if not self.tasks: #checks to see if the task list is empty
            print("no tasks were found")
        else:
            print(f"Tasks in {self.file_name}:") #displays the file name
            for task in self.tasks:
                print(f"ID: {task['id']}, category: {task['category']}, description: {task['description']}, status: {task['status']}")

    def add_task(self, category, description):
        new_task = {
            "id": len(self.tasks) + 1,
            "category": category,
            "description": description,
            "status": "incomplete"

        }

        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Task added: {new_task}")

    def update_task(self, task_id, category = None, description = None, status = None):
        for task in self.tasks:
            if task["id"] == task_id:
                if category:
                    task["category"] = category
                if description:
                    task["description"] = description
                    if status:
                        if status in ["incomplete", "in progress", "complete"]:
                            task["status"] = status
                        else:
                            print ("status invalid. make sure to use 'in progress', 'complete', or 'incomplete'.")
                            return
                    self.save_tasks()
                    print(f"task is updated: {task}")
                    return
        print("task was not found")

#this is the main CLI function
def main():
    parser = argparse.ArgumentParser(description = "TODO List CLI Tool")
    parser.add_argument("--list-name", default = "TODO.json", help = "specify the todo list file name")
    subparsers = parser.add_subparsers(dest= "command", help= "commands")

    #list subcommand
    subparsers.add_parser("list", help = "lists all tasks")

    #add subcommand
    add_parser = subparsers.add_parser("add", help = "add new task")
    add_parser.add_argument ("category", help = "category of task")
    add_parser.add_argument ("description", help = "description of task")

    #update subcommand
    update_parser = subparsers.add_parser ("update", help = "update task")
    update_parser.add_argument ("id", type = int, help = "id of task to update")
    update_parser.add_argument("--category", help = "new category of tasks")
    update_parser.add_argument("--description", help = "new description of tasks")
    update_parser.add_argument("--status", help = "new task status which is (in progress, complete, incomplete)")

    args = parser.parse_args()
    todo_list = TodoList(args.list_names)

    if args.command == "list":
        todo_list.list_tasks()
    elif args.command == "add":
        todo_list.add_task(args.category, args.description)
    elif args.command == "update":
        todo_list.update_task(args.id, args.category, args.description, args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()