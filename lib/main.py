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
    
    ob = open('important.txt', 'r')
    ab = ob.readline().split(';')
    ob.close()

    def updateUser(self):
        b = MyBdd().update(self.ab[5], self.name_input.text, self.surname_input.text, self.ab[4], 0)
        if b:
            self.text_label.color = (0, 0, 0, 1)
            self.text_label.text = "Loading ..."
            ob = open('important.txt', 'w')
            for i in MyBdd().recupOne(self.ab[5]):
                ob.write(f"{i};")
            ob.close()
            
            updatePopup()
            sm.current = "Home"
        else:
            self.text_label.color = (1, 0, 0, 1)
            self.text_label.text = "Erreur ! "

class HomePage(Screen):
    ob = open('important.txt', 'r')
    ab = ob.readline().split(';')
    ob.close()
    name = ObjectProperty()
    pre = ObjectProperty()
    def refresh(self):
        ob = open('important.txt', 'r')
        self.ab = ob.readline().split(';')
        ob.close()
        print(self.ab)
        sm.current = "Home"
    def suppr(self):
        print(self.ab[5])
        MyBdd().delete(self.ab[5])
        ob = open('important.txt', 'w')
        for i in range(5):
            ob.write(f"{i};")
        ob.close()
        deletePopup()
        sm.transition.direction = "down"
        sm.current = "Login"

    def update(self):
        sm.transition.direction = "up"
        sm.current = "Update"

class MyApp(App):
    def build(self):
        return sm
# Fonction Gloabale
def updatePopup():
    pop = Popup(title='Mis à Jour Effectué, Relance appli',
                  content=Label(text="Relance l'application", color=(1,0,0,1), font_size="21sp"),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def deletePopup():
    pop = Popup(title='Utilisateur Supprimé !',
                  content=Label(text="Relance l'application", color=(1,0,0,1), font_size="21sp"),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def connectPopup():
    pop = Popup(title='Utilisateur Ajouté !',
                  content=Label(text="Relance l'application", color=(1,0,0,1), font_size="21sp"),
                  size_hint=(None, None), size=(400, 400))
    pop.open()







kv = Builder.load_file("kv.kv")
# Page Controller Variable
sm = PageManager()
sm.add_widget(HomePage(name="Home"))
sm.add_widget(RegisterPage(name="Register"))
sm.add_widget(LoginPage(name="Login"))
sm.add_widget(UpdatePage(name="Update"))
sm.current = "Home"

if __name__ == "__main__":
    MyApp().run()