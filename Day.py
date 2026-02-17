from Task import Task

# Klasa dnia do przechowywania listy zadań Task
class Day:
    def __init__(self,day:str,tasks:list=None):
        self.day = day
        self.tasks = tasks
    
    def add_todo(self,task:str,time_from, time_to):
        if task is None or time_from < 0 or time_to > 24 or time_from >= time_to:
            raise ValueError("Niepoprawne dane")
        new_task = Task(task,time_from,time_to)
        if self.verify_task(new_task):
            self.tasks.append(Task(task,time_from,time_to))
            return new_task
        return "Powtórka"
        

    def remove_todo(self,task:Task):
        if self.tasks is None:
            raise ValueError("Brak zadań do usunięcia")
        self.tasks.remove(task)

    def verify_task(self,new_task:Task):
        for task in self.tasks:
            if new_task == task:
                return 0
        return 1
        

    def change_time(self,task:Task,new_time_from:int,new_time_to:int):
        if new_time_from is None and new_time_to is None:
            raise ValueError("Brak nowych czasów")
        if task is None or new_time_from < 0 or new_time_to > 24 or new_time_from >= new_time_to:
            raise ValueError("Niepoprawne dane")
        if self.verify_task(task):
            self.remove_todo(task)
            new_task = Task(task.get_task(),new_time_from,new_time_to)
            self.task.append(new_task)
            return new_task      
        raise ValueError("Zadanie nie znalezione")

    