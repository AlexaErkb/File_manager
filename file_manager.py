import os
import shutil
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showerror
from tkinter import messagebox
from zipfile import ZipFile
from configs import path


class FileManager:

    def __init__(self, name, condition):
        self.name = name
        self.window = Tk()
        self.window["bg"] = "#DC8F90"
        self.text = StringVar()
        self.label = Label(width=100, textvariable=self.text)
        self.console = Entry(width=100)
        self.file_list = Listbox(width=100, height=20)
        self.commands = {
            "help": self.help,
            "create_dir": self.create_dir,
            "change_dir": self.change_dir,
            "remove_dir": self.remove_dir,
            "create_file": self.create_file,
            "change_file": self.change_file,
            "read": self.read,
            "exit_display": self.exit_display,
            "remove_file": self.remove_file,
            "copy": self.copy,
            "move": self.move,
            "rename": self.rename,
            "create_archive_dir": self.create_archive_dir,
            "create_archive_file": self.create_archive_file,
            "archive": self.archive
        }
        self.condition = condition
        if self.condition == 'not have':
            self.path = path
            self.create_dir(self.name)
        self.path = fr'{path}\{self.name}'
        self.configure_window()

    def configure_window(self):
        self.window.title("File manager")
        self.window.bind('<Return>', self.get_command)
        self.file_list.pack(side=BOTTOM, padx=10, pady=10)
        self.file_list.configure(font=Font(size=9, weight="bold"), bg="#FFFFFF", fg="#000000",
                                 selectbackground="#000000", selectforeground="#FFFFFF")
        self.label.pack(side=BOTTOM, padx=10)
        self.label.configure(font=Font(size=9, weight="bold"), bg="#FFFFFF", fg="#000000")
        self.console.pack(side=BOTTOM, padx=10, pady=2)
        self.console.configure(font=Font(size=9, weight="bold"), bg="#FFFFFF", fg="#000000")
        self.display_dir_content()
        self.display_path()
        self.window.mainloop()

    def display_dir_content(self):
        self.file_list.delete(0, END)
        for file in os.listdir(self.path):
            self.file_list.insert(END, file)

    def display_path(self):
        self.text.set(f'Рабочая директория: {self.path}')

    def display_content(self, content):
        self.file_list.delete(0, END)
        for line in content:
            self.file_list.insert(END, line)

    def exit_display(self):
        self.display_dir_content()

    def help(self):
        commands = '''create_dir *имя* - создать новую директорию
        change_dir *путь* - перейти в другую директорию
        remove_dir *имя* - удалить директорию со всем содержимым
        create_file *имя* - создание файла
        change_file *содержимое* *имя* - запись данных в файл
        read *имя* - режим чтения файла
        exit_display - выйти из режима чтения
        remove_file *имя* - удалить выбранный файл
        copy *имя* *путь* - копирует выбранный файл в другое место
        move *имя* *путь* - перемещает выбранный файл в другое место
        rename *старое имя* *новое имя* - переименовывает файл
        create_archive_dir *имя архива* *имя папки* - создает архив из папки
        create_archive_file *имя архива* *имя папки* - создает архив из файлов
        archive *имя* - распаковывает архив'''

        messagebox.showinfo('Доступные команды', commands)

    def get_command(self, func):
        line = self.console.get().split(" ")
        self.console.delete(0, END)
        if len(line) > 0:
            command, arguments = line[0], line[1:]
            if command in self.commands.keys():
                self.commands[command](*arguments)
            else:
                showerror("Ошибка", "Нет такой команды")
            self.display_path()

    def create_dir(self, *args):
        if len(args) > 1:
            showerror("Ошибка", "Слишком много аргументов")
        else:
            dirName = args[0]
            try:
                os.mkdir(self.path + os.sep + dirName)
                self.display_dir_content()
            except Exception as e:
                showerror("Warning", str(e))

    def change_dir(self, *args):
        if len(args) > 1:
            showerror("Ошибка", "Слишком много аргументов")
        else:
            try:
                if args[0] == '.':
                    os.chdir(path)
                    self.path = fr'{path}\{self.name}'
                    self.display_dir_content()
                else:
                    os.chdir(fr'{self.path}\{args[0]}')
                    self.path += fr'\{args[0]}'
                    self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def remove_dir(self, *args):
        if len(args) > 1:
            showerror("Ошибка", "Слишком много аргументов")
        else:
            dirName = args[0]
            try:
                shutil.rmtree(self.path + os.sep + dirName)
                self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def create_file(self, *args):
        try:
            for file_name in args:
                if ".txt" not in file_name:
                    file_name += ".txt"
                if file_name in os.listdir(self.path):
                    showerror("Ошибка", 'Уже есть такой файл')
                else:
                    open(fr"{self.path}\{file_name}", 'a').close()
            self.display_dir_content()
        except Exception as e:
            showerror("Ошибка", str(e))

    def change_file(self, *args):
        if len(args) < 2:
            showerror("Ошибка", "Недостаточно данных")
        else:
            try:
                file_name, data = args[-1], args[0:]
                if ".txt" not in file_name:
                    file_name += ".txt"
                with open(fr"{self.path}\{file_name}", 'a') as file:
                    file.write(" ".join(data) + "\n")
                self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def read(self, *args):
        if len(args) > 1:
            showerror("Ошибка", "Слишком много аргументов")
        else:
            try:
                file_name = args[0]
                if ".txt" not in file_name:
                    file_name += ".txt"
                with open(file_name, 'r') as file:
                    self.display_content(file)
            except Exception as e:
                showerror("Ошибка", str(e))

    def remove_file(self, *file_names):
        try:
            for file_name in file_names:
                if ".txt" not in file_name:
                    file_name += ".txt"
                os.remove(fr"{self.path}\{file_name}")
            self.display_dir_content()
        except Exception as e:
            showerror("Ошибка", str(e))

    def copy(self, *args):
        file_names = args[:-1]
        dirPath = fr'{self.path}\{args[-1]}'
        try:
            for file_name in file_names:
                if ".txt" not in file_name:
                    file_name += ".txt"
                shutil.copy(fr'{self.path}\{file_name}', dirPath)
            self.display_dir_content()
        except Exception as e:
            showerror("Ошибка", str(e))

    def move(self, *args):
        if len(args) > 2:
            showerror("Ошибка", "Слишком много данных")
        elif len(args) < 2:
            showerror("Ошибка", "Слишком мало данных")
        else:
            try:
                file_names = args[:-1]
                dirPath = fr'{self.path}\{args[-1]}'
                for file_name in file_names:
                    if ".txt" not in file_name:
                        file_name += ".txt"
                        shutil.move(fr'{self.path}\{file_name}', dirPath)
                self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def rename(self, *args):
        if len(args) > 2:
            showerror("Ошибка", "Слишком много данных")
        elif len(args) < 2:
            showerror("Ошибка", "Слишком мало данных")
        else:
            try:
                file_name = args[0]
                if ".txt" not in file_name:
                    file_name += ".txt"
                new_file_name = args[1]
                if ".txt" not in new_file_name:
                    new_file_name += ".txt"
                os.rename(fr'{self.path}\{file_name}', fr'{self.path}\{new_file_name}')
                self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def create_archive_dir(self, *args):
        if len(args) < 1:
            showerror("Ошибка", "Слишком мало аргументов")
        elif len(args) > 2:
            showerror("Ошибка", "Слишком много аргументов")
        else:
            try:
                shutil.make_archive(fr'{self.path}\{args[0]}', 'zip', fr'{self.path}\{args[1]}')
                self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def create_archive_file(self, *args):
        if len(args) < 1:
            showerror("Ошибка", "Слишком мало аргументов")
        else:
            try:
                with ZipFile(fr'{self.path}\{args[0].split(".")[0]}.zip', "w") as zip_file:
                    for file in args[1:]:
                        zip_file.write(fr'{self.path}\{file}', arcname=file)
                    self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

    def archive(self, *args):
        if len(args) < 1:
            showerror("Ошибка", "Слишком мало аргументов")
        else:
            try:
                for zip_file in args:
                    z = ZipFile(fr'{self.path}\{zip_file}')
                    z.extractall(fr'{self.path}\{zip_file[:-4]}')
                self.display_dir_content()
            except Exception as e:
                showerror("Ошибка", str(e))

def authentication(name, condition):
    FileManager(name, condition)