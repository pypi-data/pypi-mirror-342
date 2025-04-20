

class DiffEmptyException(Exception):
    def __init__(self, message:str="aucun changement detecte, aucun message de commit peut etre genere"):
        self.message = message
        super().__init__(self.message)