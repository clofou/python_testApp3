import sys
sys.path.append("services/")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
from services.sqlBdd import MyBdd
from kivy.properties import ObjectProperty

# Page Controller
class PageManager(ScreenManager):
    pass

# Toutes Les Pages
class SearchPage(Screen):
    pass

class LoginPage(Screen):
    mail_input = ObjectProperty()
    password_input = ObjectProperty()
    text_label = ObjectProperty()
    def seConnecter(self):
        a = MyBdd().login(self.mail_input.text, self.password_input.text)
        if a:
            self.text_label.color = (0, 0, 0, 1)
            self.text_label.text = "Loading ..."
            ob = open('important.txt', 'w')
            for i in MyBdd().recupOne(self.mail_input.text):
                ob.write(f"{i};")
            ob.close()
            sm.transition.direction = "up"
            sm.current = "Home"
        else:
            self.text_label.color = (1, 0, 0, 1)
            self.text_label.text = "Email ou Mot de Passe Incorrect"

class RegisterPage(Screen):
    mail_input = ObjectProperty()
    password_input = ObjectProperty()
    name_input = ObjectProperty()
    surname_input = ObjectProperty()
    note_input = ObjectProperty()
    text_label = ObjectProperty()
    def createUser(self):
        b = False
        if self.note_input.text != "":
            b = MyBdd().register(self.mail_input.text, self.password_input.text, self.name_input.text, self.surname_input.text, float(self.note_input.text), 0)
        if b:
            self.text_label.color = (0, 0, 0, 1)
            self.text_label.text = "Loading ..."
            connectPopup()
            sm.current = "Login"
        else:
            self.text_label.color = (1, 0, 0, 1)
            self.text_label.text = "Erreur ! "

class UpdatePage(Screen):
    name_input = ObjectProperty()
    surname_input = ObjectProperty()
    text_label = ObjectProperty()

    def yo(self):
        ob = open('important.txt', 'r')
        ab = ob.readline().split(';')
        self.name_input.text = ab[1]
        self.surname_input.text = ab[2]
        ob.close()

    def updateUser(self):
        ob = open('important.txt', 'r')
        ab = ob.readline().split(';')
        b = MyBdd().update(ab[5], self.name_input.text, self.surname_input.text, ab[4], 0)
        if b:
            self.text_label.color = (0, 0, 0, 1)
            self.text_label.text = "Loading ..."
            ob = open('important.txt', 'w')
            for i in MyBdd().recupOne(ab[5]):
                ob.write(f"{i};")
            ob.close()
            
            updatePopup()
            sm.current = "Home"
        else:
            self.text_label.color = (1, 0, 0, 1)
            self.text_label.text = "Erreur ! "

class HomePage(Screen):
    lname = ObjectProperty()
    pre = ObjectProperty()
    email = ObjectProperty()
    note = ObjectProperty()
    def suppr(self):
        ob = open('important.txt', 'r')
        ab = ob.readline().split(';')
        MyBdd().delete(ab[5])
        ob.close()
        ob = open('important.txt', 'w')
        for i in range(6):
            ob.write(f"{i};")
        ob.close()
        deletePopup()
        sm.transition.direction = "down"
        sm.current = "Login"
    def yo(self):
        ob = open('important.txt', 'r')
        ab = ob.readline().split(';')
        self.lname.text = "Nom: " + ab[1]
        self.pre.text = "Prenom: " + ab[2]
        self.email.text = "Email: " + ab[5]
        self.note.text = "Note: " + ab[4]
        ob.close()
    def update(self):
        sm.transition.direction = "up"
        sm.current = "Update"

class MyApp(App):
    def build(self):
        return sm
# Fonction Gloabale
def updatePopup():
    pop = Popup(title='update',
                  content=Label(text="Mis à Jour Effectué", color=(0,1,0,1), font_size="21sp"),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def deletePopup():
    pop = Popup(title='Suppression',
                  content=Label(text="Utilisateur Supprimé avec succès!", color=(1,0,0,1), font_size="21sp"),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def connectPopup():
    pop = Popup(title='Ajout',
                  content=Label(text="Utilisateur Ajouté !", color=(1,0,0,1), font_size="21sp"),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def refresh():
    sm.clear_widgets()
    sm.add_widget(HomePage(name="Home"))
    sm.add_widget(RegisterPage(name="Register"))
    sm.add_widget(LoginPage(name="Login"))
    sm.add_widget(UpdatePage(name="Update"))






kv = Builder.load_file("kv.kv")
# Page Controller Variable
sm = PageManager()
sm.add_widget(HomePage(name="Home")) 
sm.add_widget(RegisterPage(name="Register"))
sm.add_widget(LoginPage(name="Login"))
sm.add_widget(UpdatePage(name="Update"))
sm.add_widget(SearchPage(name="Search"))
lk = open('important.txt', 'r')
bk = lk.readline().split(';')
if (bk[0] != 0):
    sm.current = "Home"
else:
    sm.current = "Login"

if __name__ == "__main__":
    MyApp().run()