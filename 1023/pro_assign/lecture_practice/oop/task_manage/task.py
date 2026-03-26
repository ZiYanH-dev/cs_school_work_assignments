class Task:
    def __init__(self, task_id, title, category, priority):
        self.task_id=task_id
        self.title=title
        self.category=category
        self.priority=priority
        self.is_complete=False
    
    def mark_completed(self):
        self.is_complete=True

    def __str__(self):
        stats={
            'id':self.task_id,
            'title':self.title,
            'category':self.category,
            'priority':self.priority
        }
        return str(stats)