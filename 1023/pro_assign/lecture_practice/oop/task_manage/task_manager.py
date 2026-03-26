from task import Task
class Task_manager:
    def __init__(self):
        self.tasks=[]
        self.next_id=1

    def add_task(self,title,category,priority):
        if isinstance(title,str) and title and category and isinstance(category,str):
            task=Task(task_id=self.next_id,title=title,category=category,priority=priority)
            self.tasks.append(task)
            self.next_id+=1
            return True
        else:
            print("Title cannot be empty")
            return False
        
    def delete_task(self, task_id):
        for task in self.tasks.copy():
            if task.task_id==task_id:
                self.tasks.remove(task)
                print("Task deleted successfully" )
                return True
        print('task not found')
        return False

    def filter_tasks(self, filter_by, value):
        result=[]
        filter=filter.lower()
        if not filter_by in ["category", "priority", "is_completed"]:
            print('invalid')
            return
        match filter_by:
            case 'category':
                pass
            case 'priority':
                pass
            case 'is_completed':
                pass
        

