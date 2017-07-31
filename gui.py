import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import _mysql as sql
from pathlib import Path
import time


db = sql.connect('localhost', 'root', '7621', 'recicla_ufu_contas')

current_user = ""

baterias_ref = {
    1: range(4),
    2: range(4, 6),
    3: range(6, 11),
    4: range(11, 15),
    5: range(15, 21)
}

papel_ref = {
    1: range(301),
    2: range(301, 601),
    3: range(601, 1001),
    4: range(1001, 1501),
    5: range(1501, 3001)
}

latinhas_ref = {
    1: range(11),
    2: range(11, 21),
    3: range(21, 36),
    4: range(36, 51),
    5: range(51, 101)
}

pontuacao_ref = {
    'baterias': 50,
    'papel': 3,
    'latinhas': 5
}

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

        for F in (LoginPage, RegisterPage, Profile, PointCreditPage):

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
        logo.pack(pady=10)

        label = ttk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        username = tk.StringVar()
        password = tk.StringVar()
        self.username_entry = ttk.Entry(self, textvariable=username)
        self.password_entry = ttk.Entry(self, show='*', textvariable=password)
        self.username_entry.insert(0, "Usuário")
        self.password_entry.insert(0, "Senha")
        self.username_entry.pack(pady=10)
        self.password_entry.pack()

        button1 = ttk.Button(self, text="Login",
                             command=lambda: self.check_user(username, password, controller))
        button1.pack(pady=10)

        button2 = ttk.Button(self, text="Registrar",
                             command=lambda: controller.show_frame(RegisterPage))
        button2.pack(pady=30)

    def check_user(self, username, password, controller):
        global current_user
        username = username.get()
        password = password.get()
        if username == 'admin' and password == 'admin':
            current_user = username
            controller.show_frame(PointCreditPage)
        else:
            db.query("SELECT password FROM contas WHERE username = '%s'" % username)
            result = db.store_result()

            if result.num_rows() != 0:
                result = str(result.fetch_row()[0][0], 'utf-8')
                if result == password:
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
        self.password_conf_entry.insert(0, "Senha")

        self.username_entry.pack()
        self.password_entry.pack(pady=10)
        self.password_conf_entry.pack()

        button1 = ttk.Button(self, text="Registrar",
                             command=lambda: self.check_reg(username, password, password_conf, controller))
        button1.pack(pady=10)

        button2 = ttk.Button(self, text="Voltar",
                             command=lambda: controller.show_frame(LoginPage))
        button2.pack()

    def check_reg(self, username, password, password_conf, controller):
        username = username.get()
        password = password.get()
        password_conf = password_conf.get()

        db.query("SELECT password FROM contas WHERE username = '%s'" % username)
        result = db.store_result()

        if result.num_rows() != 0:
            popupmsg("Nome de usuário já cadastrado.")
        elif password_conf != password:
            popupmsg("Senhas não coincidem.")
        else:
            db.query("INSERT INTO contas (username, password, pontos) VALUES ('%s','%s','%s')"
                     % (username, password, 0))
            db.query("INSERT INTO achievements (user) VALUES ('%s')" % username)
            controller.show_frame(LoginPage)

            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.password_conf_entry.delete(0, 'end')

            self.username_entry.insert(0, "Usuário")
            self.password_entry.insert(0, "Senha")
            self.password_conf_entry.insert(0, "Senha")

            popupmsg("Usuário cadastrado com sucesso.")


class Profile(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.profile_name_text = tk.StringVar()
        self.profile_name_text.set(current_user)
        self.profile_name = ttk.Label(self, textvariable=self.profile_name_text, font=LARGE_FONT)
        self.profile_name.pack(pady=10, padx=10)

        img = Image.open("./profile_pics/teste_1.png")
        render = ImageTk.PhotoImage(img)
        self.profile_pic = ttk.Label(self, image=render)
        self.profile_pic.image = render
        self.profile_pic.pack()

        self.pont = tk.StringVar()
        self.pont_label = ttk.Label(self, textvariable=self.pont, font=LARGE_FONT)
        self.pont_label.pack()

        self.baterias_text = tk.StringVar()
        self.baterias_label = ttk.Label(self, textvariable=self.baterias_text, font=NORM_FONT)
        self.baterias_label.pack(pady=20)
        prg_bar = ImageTk.PhotoImage(Image.open("./progress_bar/progress_bar_0.png"))
        self.progress_bar_bat = ttk.Label(self, image=prg_bar)
        self.progress_bar_bat.image = prg_bar
        self.progress_bar_bat.pack()

        self.baterias_num_text = tk.StringVar()
        self.baterias_num = ttk.Label(self, textvariable=self.baterias_num_text, font=SMALL_FONT)
        self.baterias_num.pack()

        self.papel_text = tk.StringVar()
        self.papel_label = ttk.Label(self, textvariable=self.papel_text, font=NORM_FONT)
        self.papel_label.pack(pady=20)
        prg_bar = ImageTk.PhotoImage(Image.open("./progress_bar/progress_bar_0.png"))
        self.progress_bar_pap = ttk.Label(self, image=prg_bar)
        self.progress_bar_pap.image = prg_bar
        self.progress_bar_pap.pack()

        self.papel_num_text = tk.StringVar()
        self.papel_num = ttk.Label(self, textvariable=self.papel_num_text, font=SMALL_FONT)
        self.papel_num.pack()

        self.latinhas_text = tk.StringVar()
        self.latinhas_label = ttk.Label(self, textvariable=self.latinhas_text, font=NORM_FONT)
        self.latinhas_label.pack(pady=20)
        prg_bar = ImageTk.PhotoImage(Image.open("./progress_bar/progress_bar_0.png"))
        self.progress_bar_lat = ttk.Label(self, image=prg_bar)
        self.progress_bar_lat.image = prg_bar
        self.progress_bar_lat.pack()

        self.latinhas_num_text = tk.StringVar()
        self.latinhas_num = ttk.Label(self, textvariable=self.latinhas_num_text, font=SMALL_FONT)
        self.latinhas_num.pack()

        button1 = ttk.Button(self, text="Desconectar",
                             command=lambda: self.log_off(controller))
        button1.pack(side="bottom", pady=5)

        button2 = ttk.Button(self, text="Atualizar",
                             command=self.update_profile)
        button2.pack(side="bottom", pady=5)

    def update_profile(self):
        self.profile_name_text.set(current_user)

        new_path = "./profile_pics/%s.png" % current_user
        if not Path(new_path).exists():
            new_path = "./profile_pics/oi.png"
        new_pic = Image.open(new_path)
        pic = ImageTk.PhotoImage(new_pic)
        self.profile_pic.configure(image=pic)
        self.profile_pic.image = pic

        db.query("SELECT pontos FROM contas WHERE username = '%s'" % current_user)
        result = db.store_result()
        result = result.fetch_row()
        pontos = 'Pontos: ' + str(int(result[0][0]))
        self.pont.set(pontos)

        db.query("SELECT * FROM achievements WHERE user = '%s'" % current_user)
        result = db.store_result()
        result = result.fetch_row()
        bat_num = int(result[0][1])
        pap_num = int(result[0][2])
        lat_num = int(result[0][3])

        f1 = 0
        f2 = 0
        f3 = 0

        for i in range(1, 6):
            if bat_num in baterias_ref[i]:
                self.baterias_text.set("Baterias #%d" % i)
                txt = str(bat_num) + '/' + str(max(baterias_ref[i]))
                self.baterias_num_text.set(txt)
                bat_num = round(float(bat_num) / max(baterias_ref[i])*100)
                f1 = 1
            if pap_num in papel_ref[i]:
                self.papel_text.set("Papel #%d" % i)
                txt = str(pap_num) + '/' + str(max(papel_ref[i])) + ' gramas'
                self.papel_num_text.set(txt)
                pap_num = round(float(pap_num) / max(papel_ref[i]) * 100)
                f2 = 1
            if lat_num in latinhas_ref[i]:
                self.latinhas_text.set("Latinhas #%d" % i)
                txt = str(lat_num) + '/' + str(max(latinhas_ref[i]))
                self.latinhas_num_text.set(txt)
                lat_num = round(float(lat_num) / max(latinhas_ref[i]) * 100)
                f3 = 1

        if not f1:
            self.baterias_text.set("Baterias #5")
            txt = str(bat_num) + '/' + str(max(baterias_ref[5]))
            self.baterias_num_text.set(txt)
            bat_num = 100
        if not f2:
            self.papel_text.set("Papel #5")
            txt = str(pap_num) + '/' + str(max(papel_ref[5])) + ' gramas'
            self.papel_num_text.set(txt)
            pap_num = 100
        if not f3:
            self.latinhas_text.set("Latinhas #5")
            txt = str(lat_num) + '/' + str(max(latinhas_ref[5]))
            self.latinhas_num_text.set(txt)
            lat_num = 100

        new_path = "./progress_bar/progress_bar_%d.png" % bat_num
        new_pgbr = ImageTk.PhotoImage(Image.open(new_path))
        self.progress_bar_bat.configure(image=new_pgbr)
        self.progress_bar_bat.image = new_pgbr

        new_path = "./progress_bar/progress_bar_%d.png" % pap_num
        new_pgbr = ImageTk.PhotoImage(Image.open(new_path))
        self.progress_bar_pap.configure(image=new_pgbr)
        self.progress_bar_pap.image = new_pgbr

        new_path = "./progress_bar/progress_bar_%d.png" % lat_num
        new_pgbr = ImageTk.PhotoImage(Image.open(new_path))
        self.progress_bar_lat.configure(image=new_pgbr)
        self.progress_bar_lat.image = new_pgbr

    def log_off(self, controller):
        global current_user
        current_user = ""

        login_page = controller.frames[LoginPage]

        login_page.username_entry.delete(0, 'end')
        login_page.password_entry.delete(0, 'end')

        login_page.username_entry.insert(0, "Usuário")
        login_page.password_entry.insert(0, "Senha")

        controller.show_frame(LoginPage)


class PointCreditPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text='Crédito de pontos', font=LARGE_FONT)
        label.pack(pady=20)

        self.credit_user = tk.StringVar()
        self.credit_user_entry = ttk.Entry(self, textvariable=self.credit_user)
        self.credit_user_entry.pack(pady=10)
        self.credit_user.set("Usuário")

        ttk.Label(self, text="Baterias").pack(pady=10)
        self.slider_baterias = tk.Scale(self, orient='horizontal', from_=0, to=20, length=300,
                                        tickinterval=2, sliderlength=10)
        self.slider_baterias.pack(pady=10)

        ttk.Label(self, text="Papel").pack(pady=10)
        self.slider_papel = tk.Scale(self, orient='horizontal', from_=0, to=3000, length=300,
                                     tickinterval=500, sliderlength=10)
        self.slider_papel.pack(pady=10)

        ttk.Label(self, text="Latinhas").pack(pady=10)
        self.slider_latinhas = tk.Scale(self, orient='horizontal', from_=0, to=20, length=300,
                                        tickinterval=2, sliderlength=10)
        self.slider_latinhas.pack(pady=10)

        button1 = ttk.Button(self, text="Desconectar",
                             command=lambda: controller.frames[Profile].log_off(controller))
        button1.pack(side="bottom", pady=20)

        button2 = ttk.Button(self, text="Creditar",
                             command=lambda: self.check_user(self.credit_user))
        button2.pack(pady=20)

    def check_user(self, credit_user):

        credit_user = credit_user.get()
        db.query("SELECT last_credit FROM contas WHERE username = '%s'" % credit_user)
        result = db.store_result()

        if result.num_rows() == 0 or credit_user == 'admin':
            popupmsg("Usuário inválido")

        elif time.time() - int(result.fetch_row()[0][0]) < 8:
            popupmsg("Aguarde para realizar novo crédito.")

        else:
            baterias_num = self.slider_baterias.get()
            papel_num = self.slider_papel.get()
            latinhas_num = self.slider_latinhas.get()

            if not baterias_num and not papel_num and not latinhas_num:
                popupmsg("Selecione ao menos um valor.")
            else:
                credit_points = baterias_num*pontuacao_ref['baterias'] + papel_num*pontuacao_ref['papel'] + latinhas_num*pontuacao_ref['latinhas']

                db.query("UPDATE contas SET pontos = pontos + %d, last_credit = %d WHERE username = '%s'" % (credit_points, time.time(), credit_user))
                db.commit()

                db.query("UPDATE achievements SET baterias = baterias + %d, papel = papel + %d, latinhas = latinhas + %d WHERE user = '%s'" % (baterias_num, papel_num, latinhas_num, credit_user))
                db.commit()

                self.slider_baterias.set(0)
                self.slider_papel.set(0)
                self.slider_latinhas.set(0)

                popupmsg("%d pontos creditados com sucesso para o usuário %s." % (credit_points, credit_user))

app = ReciclaUFU()
app.geometry("400x600")
app.mainloop()
