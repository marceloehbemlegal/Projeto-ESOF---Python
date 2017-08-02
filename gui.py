import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import _mysql as sql
from pathlib import Path


user_list = {}
db = sql.connect('localhost', 'root', '7621', 'recicla_ufu_contas')
current_user = ""


db.query("SELECT * FROM contas")

results = db.store_result()

rows = results.fetch_row(maxrows=0)

for eachRow in rows:
    u = str(eachRow[0], 'utf-8')
    ps = str(eachRow[1], 'utf-8')
    pt = str(eachRow[2], 'utf-8')
    user_list[u] = [ps, pt]

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


def popupmsg(msg):
    def leave():
        popup.destroy()
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill='x', pady=10)
    b1 = ttk.Button(popup, text="Okay", command=leave)
    b1.pack()
    popup.mainloop()


class ReciclaUFU(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="a.ico")
        tk.Tk.wm_title(self, "Recicla UFU")

        container = tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, RegisterPage, Profile):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        load = Image.open('logo.png')
        render = ImageTk.PhotoImage(load)

        logo = ttk.Label(self, image=render)
        logo.image = render
        logo.pack()

        label = ttk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        username = tk.StringVar()
        password = tk.StringVar()
        self.username_entry = ttk.Entry(self, textvariable=username)
        self.password_entry = ttk.Entry(self, show='*', textvariable=password)
        self.username_entry.insert(0, "Usuário")
        self.password_entry.insert(0, "Senha")
        self.username_entry.pack()
        self.password_entry.pack()

        button1 = ttk.Button(self, text="Login",
                             command=lambda: self.check_user(username, password, controller))
        button1.pack()

        button2 = ttk.Button(self, text="Registrar",
                             command=lambda: controller.show_frame(RegisterPage))
        button2.pack()

    def check_user(self, username, password, controller):
        global current_user
        username = username.get()
        password = password.get()
        if username in user_list:
            if user_list[username][0] == password:
                current_user = username
                controller.frames[Profile].update_profile()
                controller.show_frame(Profile)
            else:
                popupmsg("Senha incorreta.")
        else:
            popupmsg("Usuário não encontrado.")


class RegisterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Criar conta", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        username = tk.StringVar()
        password = tk.StringVar()
        password_conf = tk.StringVar()

        self.username_entry = ttk.Entry(self, textvariable=username)
        self.password_entry = ttk.Entry(self, show='*', textvariable=password)
        self.password_conf_entry = ttk.Entry(self, show='*', textvariable=password_conf)

        self.username_entry.insert(0, "Usuário")
        self.password_entry.insert(0, "Senha")
        self.password_conf_entry.insert(0, "Confirmar senha")

        self.username_entry.pack()
        self.password_entry.pack()
        self.password_conf_entry.pack()

        button1 = ttk.Button(self, text="Registrar",
                             command=lambda: self.check_reg(username, password, password_conf, controller))
        button1.pack()

        button2 = ttk.Button(self, text="Voltar",
                             command=lambda: controller.show_frame(LoginPage))
        button2.pack()

    def check_reg(self, username, password, password_conf, controller):
        username = username.get()
        password = password.get()
        password_conf = password_conf.get()
        if username in user_list:
            popupmsg("Nome de usuário já cadastrado.")
        elif password_conf != password:
            popupmsg("Senhas não coincidem.")
        else:
            db.query("INSERT INTO contas (username, password, pontos) VALUES ('%s','%s','%s')" % (username, password, 0))
            controller.show_frame(LoginPage)

            user_list[username] = [password, '0']

            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.password_conf_entry.delete(0, 'end')

            self.username_entry.insert(0, "Usuário")
            self.password_entry.insert(0, "Senha")
            self.password_conf_entry.insert(0, "Confirmar senha")

            popupmsg("Usuário cadastrado com sucesso.")


class Profile(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.profile_name_text = tk.StringVar()
        self.profile_name_text.set(current_user)
        self.profile_name = tk.Label(self, textvariable=self.profile_name_text, font=LARGE_FONT)
        self.profile_name.pack(pady=10, padx=10)

        img = Image.open("./profile_pics/teste_1.png")
        render = ImageTk.PhotoImage(img)
        self.profile_pic = tk.Label(self, image=render)
        self.profile_pic.image = render

        self.profile_pic.pack()

        button1 = ttk.Button(self, text="Desconectar",
                             command=lambda: self.log_off(controller))
        button1.pack(side="bottom", pady=30)

    def update_profile(self):
        self.profile_name_text.set(current_user)

        new_path = "./profile_pics/%s.png" % current_user

        if not Path(new_path).exists():
            new_path = "./profile_pics/oi.png"

        new_pic = Image.open(new_path)
        pic = ImageTk.PhotoImage(new_pic)
        self.profile_pic.configure(image=pic)
        self.profile_pic.image = pic

    def log_off(self, controller):
        global current_user
        current_user = ""

        login_page = controller.frames[LoginPage]

        login_page.username_entry.delete(0, 'end')
        login_page.password_entry.delete(0, 'end')

        login_page.username_entry.insert(0, "Usuário")
        login_page.password_entry.insert(0, "Senha")

        controller.show_frame(LoginPage)

app = ReciclaUFU()
app.geometry("400x600")
app.mainloop()
