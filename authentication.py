from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror
import os
import file_manager


if os.path.isfile('./users.txt') == False:
    with open('users.txt', 'w+', encoding='utf-8') as file:
        file.close()

users = []

with open('users.txt', 'r', encoding='utf-8') as file:
    for n in file:
        users.append(n)
    file.close()

for i in range(len(users)):
    data = users[i].split(':')
    for j in range(2):
        print(data[j])

class Authentication(Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Authentication")
        self.geometry('250x225')
        self.configure(bg="#DC8F90")

        self.login = StringVar()
        self.passwd = StringVar()

        Label(self, text="Логин:", font=Font(size=9, weight="bold"), pady=10,background="#DC8F90", fg="#000000").pack(side=TOP)
        self.entry_name = Entry(self, textvariable=self.login).pack(side=TOP)

        Label(self, text="Пароль:", font=Font(size=9, weight="bold"), pady=10, background="#DC8F90", fg="#000000").pack(side=TOP)
        self.entry_passwd = Entry(self, show="*", textvariable=self.passwd).pack(side=TOP)
        register = Button(self, text='Регистрация', width=10)
        register.config(command=self.new_user, font=Font(size=9, weight="bold"), pady=10)
        register.pack(side=BOTTOM)
        login = Button(self, text='Войти', width=10)
        login.config(command=self.log_user, font=Font(size=9, weight="bold"), pady=10)
        login.pack(side=BOTTOM)
        self.protocol("WM_DELETE_WINDOW", lambda: exit())


    @staticmethod
    def get_empty(log, passwd):
        log.set('')
        passwd.set('')


    def log_user(self):
        name = self.login.get()
        passwd = self.passwd.get()
        flag = False
        Authentication.get_empty(self.login, self.passwd)
        if len(users) == 0:
            showerror('Ошибка', 'В системе еще нет зарегистрированных пользователей')
        else:
            for user in users:
                data = user.split(':')
                if name == data[0] and passwd == data[1]:
                    flag = True
            if flag == False:
                showerror('Ошибка', 'Вы ввели неправильный логин или пароль')
            else:
                self.begin(name, 'have')

    def new_user(self):
        name = self.login.get()
        passwd = self.passwd.get()
        flag = False
        Authentication.get_empty(self.login, self.passwd)
        if len(name) != 0 and len(passwd) != 0:
            if len(users) == 0:
                with open('users.txt', 'a', encoding='utf-8') as file:
                    file.write(fr'{name}:{passwd}')
                    file.close()
            else:
                for user in users:
                    data = user.split(':')
                    if name == data[0]:
                        flag = True
                        showerror('Ошибка', 'Уже есть такой пользователь')

                if flag == False:
                    with open('users.txt', 'a', encoding='utf-8') as file:
                        file.write(fr'{name}:{passwd}')
                        file.close()
                    self.begin(name, 'not have')


    def begin(self, name, condition):
        self.destroy()
        file_manager.authentication(name, condition)


Authentication().mainloop()