# https://github.com/ollama/ollama-python
from ollama import chat, ChatResponse, ResponseError
import importlib.resources

# https://github.com/Soulter/hugging-chat-api
from hugchat import hugchat
from hugchat.login import Login

BdD = '''
create table etudiants(
	noetu  varchar(6)      not null,
	nom     varchar(10)     not null,
	prenom  varchar(10)     not null,
	primary key (noetu)) ;

create table matieres(
	codemat        varchar(8)      not null primary key,
	titre           varchar(10),
	responsable     varchar(4),
	diplome         varchar(20));

create table notes(
	noetu          varchar(6),
	codemat        varchar(8) ,
	noteex          numeric         check (noteex between 0 and 20),
	notecc          numeric         check (notecc between 0 and 20),
	primary key (noe, codemat),
	CONSTRAINT FK_noe       FOREIGN KEY (noe)       REFERENCES etudiants (noetu),
	CONSTRAINT FK_codemat   FOREIGN KEY (codemat)   REFERENCES matieres (codemat));
'''

sql1 = "select * from etudiants ;"
sql1e = "select * from etudiant ;"
erreur1 = '''
ERROR:  relation "etudiant" does not exist
LIGNE 1 : select * from etudiant;
                        ^
'''

sql2 = "select * from notes where noteex = 12;"
sql2e = "select * from notes where notex = 12;"
erreur2 = '''
ERROR:  column "notex" does not exist
LIGNE 1 : select * from notes where notex = 12;
                                        ^
'''

# Définir les codes de couleur
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


class LLM():
    def __init__(self,verbose, sgbd, modele, bd= None):
        self.prompt = str()
        self.modele = modele
        self.bd = bd
        self.sgbd = sgbd
        self.prompt_systeme = self.__build_prompt_contexte(sgbd, bd)
        self.verbose = verbose

    def __build_prompt_contexte(self, sgbd, bd = None):
        instruction_contexte = f'''
# Contexte 
Tu parles en français.
Tu es un assistant pour un élève en informatique qui apprend les fondements des bases de données relationnelles et le langage SQL.
Les élèves cherchent à apprendre SQL. Ils ne peuvent ni créer de tables ni modifier leur structure. 
Ils peuvent uniquement proposer des requêtes du langage de manipulation des données (MLD) en SQL. 
Ils te proposent des erreurs de requêtes SQL, tu es chargé de les aider à comprendre leurs erreurs.
'''

        instruction_sgbd = f'''
# Description de la base de données relationnelle

## SGBD

Le SGBD utilisé est {sgbd}.
'''
        if bd is None: instruction_base_de_donnees = ""
        else : instruction_base_de_donnees = f'''
## Schéma relationnel de la base de données 

{bd}
'''
        instruction_systeme = f'''
# Instructions

L'élève te propose *une erreur SQL*, prends le soin de l'expliquer *en français*.
Réponds en français et uniquement à la question posée. 
Réponds directement, sans faire de préambule, en t'appuyant sur les informations de la description de la base de données et sur l'erreur.
La base de données est *bien construite*. Les *noms des tables et des attributs sont corrects*. Toutes les *tables ont bien été créées*.
S'il y a des erreurs, elles viennent *nécessairement* de la requête. 
'''
        instruction = instruction_contexte + instruction_sgbd + instruction_base_de_donnees + instruction_systeme
        return instruction

    def run(self, erreur, sql_attendu, sql_soumis):
        return ""


class OllamaLLM(LLM):
    def __init__(self,verbose, sgbd, modele="gemma3:1b", bd = None):
        super().__init__(verbose,sgbd, modele,bd)

    def run(self, erreur, sql_attendu, sql_soumis):
        try:
            self.prompt = "Expliquer l'erreur suivante :\n```sql\n" + erreur + '\n```\n'
            self.prompt += f"Voici la requête SQL qui a généré cette erreur : \n```sql\n{sql_soumis}\n```\n"
            if sql_attendu != "" and sql_attendu != None: self.prompt += f"Voici la requête SQL corrigée : \n```sql\n{sql_attendu}\n```\n"
            response: ChatResponse = chat(model=self.modele, options={"temperature": 0.0}, messages=[
                {'role': 'system', 'content': self.prompt_systeme}, {
                    'role': 'user',
                    'content': self.prompt,
                },
            ])
            # print(response['message']['content'])
            if self.verbose:
                print(f"{CYAN}{self.prompt_systeme}{RESET}")
                print(f"{CYAN}{self.prompt}{RESET}")

            return (f"{GREEN}"+response.message.content + f"{RESET}\n---\n"
                    + f"{BLUE}Source : Ollama (https://ollama.com/) avec {self.modele} (https://ollama.com/library/{self.modele}){RESET}\n"
                    + f"{BLUE}Attention, Ollama/{self.modele} ne garantit pas la validité de l'aide'. Veuillez vérifier la réponse et vous rapprocher de vos enseignants si nécessaire.{RESET}")
        except Exception as e:
            return super().run(erreur, sql_attendu, sql_soumis)

class HuggingLLM(LLM):
    def __init__(self, verbose, sgbd,modele,bd = None):
        super().__init__(verbose,sgbd,modele,bd)

    def run(self, erreur, sql_attendu, sql_soumis):
        try:
            EMAIL = "emmanuel.desmontils@univ-nantes.fr"
            PASSWD = ""
            with importlib.resources.files("querycraft.cookies").joinpath('') as cookie_path_dir :
                cpd = str(cookie_path_dir)+'/'
                #print(cpd)
                #cookie_path_dir = "./cookies/"  # NOTE: trailing slash (/) is required to avoid errors
                sign = Login(EMAIL, PASSWD)
                cookies = sign.login(cookie_dir_path=cpd, save_cookies=True)

                chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

                # Create a new conversation with an assistant
                ASSISTANT_ID = self.modele  # get the assistant id from https://huggingface.co/chat/assistants
                chatbot.new_conversation(assistant=ASSISTANT_ID, switch_to=True)
                self.prompt = f"Soit la base de donnée relationnelle suivante :\n\n{self.bd}\n"
                self.prompt += f"Le SGBD utilisé est {self.sgbd}.\n"
                self.prompt += f"Voici une erreur SQL :\n---\n{erreur}\n---\n"
                self.prompt += f"Voici la requête SQL qui a généré cette erreur : \n```sql\n{sql_soumis}\n```\n"
                if sql_attendu != "" and sql_attendu != None :self.prompt += f"Voici la requête SQL corrigée : \n```sql\n{sql_attendu}\n```\n"
                self.prompt += "Explique moi l'erreur et la correction."
                if self.verbose:
                    print(f"{CYAN}{self.prompt}{RESET}")
                return (f"{GREEN}"+chatbot.chat(self.prompt).wait_until_done() + f"{RESET}\n---\n"
                        + f"{BLUE}Source : HuggingChat (https://huggingface.co/chat/), assistant Mia-DB (https://hf.co/chat/assistant/{self.modele}) {RESET}\n"
                        + f"{BLUE}Attention, HuggingChat/Mia-DB ne garantit pas la validité de l'aide. Veuillez vérifier la réponse et vous rapprocher de vos enseignants si nécessaire.{RESET}")
        except Exception as e:
            return super().run(erreur, sql_attendu, sql_soumis)# + f"\nPb HuggingChat : {e}"

def main():
    mess = HuggingLLM(True,"PostgreSQL","67bc5132aea628b3325f2f8b",BdD).run(erreur2, sql2, sql2e)
    print(mess)


if __name__ == '__main__':
    main()
