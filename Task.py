
# Klasa Task do przechowywania danych o treści zadania, czasie rozpoczęcia 
# i czasie zakończenia
class Task:
    def __init__(self, task:str, time_form:str,time_to:str):
        self.name = task
        self.time_from = time_form
        self.time_to = time_to

    def __eq__(self,other):
        return self.name == other.name and self.time_from == other.time_from and self.time_to == other.time_to
    
    def get_task(self):
        return self.name