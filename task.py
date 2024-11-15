import json

class Task:
    def __init__(self, task_id, title, description, priority, status='Pending'):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority  
        self.status = status  
    
    def update(self, title=None, description=None, priority=None, status=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if status is not None:
            self.status = status

    def mark_as_complete(self):
        """Mark the task as completed."""
        self.status = 'Completed'

    def __repr__(self):
        return f"Task({self.task_id}, {self.title}, {self.priority}, {self.status})"

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, title, description, priority):
        task_id = len(self.tasks) + 1  
        new_task = Task(task_id, title, description, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def view_tasks(self):
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority, reverse=True)
        for task in sorted_tasks:
            # Print task details in the required format
            print(f"ID: {task.task_id}, Title: {task.title}, Description: {task.description}, Priority: {task.priority}, Status: {task.status}")

    def update_task(self, task_id, title=None, description=None, priority=None, status=None):
        task = self.find_task_by_id(task_id)  
        if task: 
            task.update(title, description, priority, status)  
            self.save_tasks() 
        else:
            print(f"Task with ID {task_id} not found.")  

    def delete_task(self, task_id):
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
        else:
            print(f"Task with ID {task_id} not found.")

    def filter_tasks(self, status=None, priority=None):
        filtered_tasks = self.tasks
        if status:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        
        if filtered_tasks:
            for task in filtered_tasks:
                # Print filtered tasks with readable format
                print(f"ID: {task.task_id}, Title: {task.title}, Description: {task.description}, Priority: {task.priority}, Status: {task.status}")
        else:
            print("No tasks found with the given filters.")

    def find_task_by_id(self, task_id):
        return next((task for task in self.tasks if task.task_id == task_id), None)

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, indent=4)  # Add indent here to format JSON

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(**task_data)
                    self.tasks.append(task)
        except FileNotFoundError:
            print("No previous tasks found. Starting fresh.")

def display_menu():
    print("\nTask Manager Menu:")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Filter Tasks")
    print("6. Exit")

def main():
    task_manager = TaskManager()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            priority = input("Enter priority (High, Medium, Low): ")
            task_manager.add_task(title, description, priority)

        elif choice == '2':
            task_manager.view_tasks()

        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (or leave blank to keep current): ")
            description = input("Enter new description (or leave blank to keep current): ")
            priority = input("Enter new priority (High, Medium, Low) (or leave blank to keep current): ")
            status = input("Enter new status (Pending, Completed) (or leave blank to keep current): ")

            task_manager.update_task(task_id, 
                                     title or None, 
                                     description or None, 
                                     priority or None, 
                                     status or None)

        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            task_manager.delete_task(task_id)

        elif choice == '5':
            status = input("Enter status to filter by (Pending, Completed): ")
            priority = input("Enter priority to filter by (High, Medium, Low): ")
            task_manager.filter_tasks(status, priority)

        elif choice == '6':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
