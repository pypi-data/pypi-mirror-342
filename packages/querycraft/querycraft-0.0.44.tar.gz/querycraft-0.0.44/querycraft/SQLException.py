
from querycraft.LLM import *

class SQLException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    def __unicode__(self):
        return self.message

class SQLQueryException(SQLException):
    model = "gemma3:1b"
    cache = dict()

    @classmethod
    def set_model(cls, model):
        cls.model = model

    @classmethod
    def get_model(cls):
        return cls.model

    def __init__(self,verbose, message, sqlhs, sqlok, sgbd, bd = ""):
        super().__init__(message)
        self.sqlhs = sqlhs
        if sqlok is None : self.sqlok = ""
        else: self.sqlok = sqlok
        self.sgbd = sgbd
        if self.sqlhs+self.sqlok in SQLQueryException.cache:
            self.hints = SQLQueryException.cache[self.sqlhs]
        else:
            self.hints = OllamaLLM(verbose,self.sgbd,SQLQueryException.get_model(),bd).run(str(self.message), self.sqlok, self.sqlhs)
            if self.hints == "":
                self.hints = HuggingLLM(verbose,self.sgbd,"67bc5132aea628b3325f2f8b",bd).run(str(self.message), self.sqlok, self.sqlhs)
            SQLQueryException.cache[self.sqlhs+self.sqlok] = self.hints

    def __str__(self):
        mssg = f"{RED}Erreur sur la requête SQL avec {self.sgbd} :\n -> Requête proposée : {self.sqlhs}\n -> Message {self.sgbd} :\n{self.message}{RESET}"
        if self.hints != "":
            mssg += f"\n{GREEN} -> Aide :{RESET} {self.hints}"
        return mssg
    def __repr__(self):
        return self.__str__()
    def __unicode__(self):
        return self.__str__()