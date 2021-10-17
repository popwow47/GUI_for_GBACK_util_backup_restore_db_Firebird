###########################################IMPORT_MODULES###########################################################
import tkinter as tk  # импортирование модуля графики
from tkinter import filedialog  # импортирование из модуля графики  класс  "диалоговые окна"
import subprocess  # импортирование модуля подпроцессов для  выполнения "виндовых" программ
import os  # импортирование модуля для выполнения команд ОС
from datetime import datetime  # импортирование класса "даты и времени" из одноимённого модуля
import time  # импортирования модуля времени
from pathlib import Path  # импортирование класса "Путь" из модуля библиотек путей
import arrow

from tkinter import messagebox  # импортирование класса информационных окон из модуля графики

##################################################GLOBAL_VARIABLES###################################################
current_time = time.time()
now = datetime.now()
database_temp = " "
save_location_temp = " "
util_temp = ""
database_filename = " "
save_location_name = " "
util_name = ''
#####################################################FUNCTIONS#########################################################
# функция сообщения при возникновения ошибки
def error_message(m):
    messagebox.showerror("Произошла ошибка!", '''ВНИМАНИЕ!
Если Вы видите это сообщение то значит возможно
у Вас один или несколько из следующих пунктов :
1)Проверьте правильно ли Вы выбрали утилиту gbak.exe;
2)Проверьте правильно ли Вы выбрали Баузу Данных;
2)Проверьте корректны ли имя\пароль БД;
3)Проверьте включён ли сервер Firebird;
%s''' % m)



# функция сообщения с предупреждением
def warning_message():
    messagebox.showwarning("ПРЕДУПРЕЖДЕНИЕ!",
                           '''Пожалуйста выбирайте разные каталоги хранения для БД и Backup'ов во избежании удалениях их при начале копирования так как функция автоудаления настроена на  файлы старше 10 дней отроду ''')





# функция активации кнопок "копирования и резервирования" при определённом условии
def check_backup_restore_on_key(event):
    if len(password_db_input.get()) and len(username_db_input.get()) > 0:
        backup_button['state'] = 'normal'
        restore_button['state'] = 'normal'
    else:
        backup_button['state'] = 'disabled'
        restore_button['state'] = 'disabled'


# функция активации кнопки "для выбора файла"
def check_browse_util():
    global util_temp
    if util_temp == ['']:

        browse_database_button['state'] = 'disabled'
    else:
        browse_database_button['state'] = 'normal'



# функция активации кнопки "для выбора каталога"
def check_browse_database():
    global database_temp

    if database_temp  != ['']:

        save_backup_location_button['state'] = 'normal'
    else:
        save_backup_location_button['state'] = 'disabled'


# функция выбора файлов БД\Backup'ов
def database_browse_button():
    warning_message()

    global data_base_folder_path
    global database_filename
    global database_temp
    global tmp2
    database_filename = filedialog.askopenfilename(initialdir="/",
                                           title="Выберите файл",
                                           filetypes=(  ("firebird FDB files", "*.fdb*"),("firebird GBK files", "*.gbk*,*.fdb*"),
                                               ("all files",
                                                "*.*")))
    data_base_folder_path.set(database_filename)
    database_temp = database_filename.split("/")

    try:
        tmp = database_temp[-1].split(".")
        tmp2 = tmp[0] + "." + tmp[1]
    except Exception as e:
        error_message(e)
    check_browse_database()


# функция  выбора исполняемых файлов
def util_browse_button():
    global backup_util_folder_path3
    global util_name
    global util_temp
    util_name = filedialog.askopenfilename(initialdir="/",
                                           title="Выберите файл gbak.exe",
                                           filetypes=(("exe files",
                                                       "*.exe*"),
                                                      ))
    backup_util_folder_path3.set(util_name)
    util_temp = util_name.split("/")
    check_browse_util()



# функция удаления файлов по дате их создания
def del_files():
    filesPath = save_location_name

    criticalTime = arrow.now().shift(hours=+1).shift(days=-10)  # файлы старше 10 дней

    for item in Path(filesPath).glob('*'):
        if item.is_file():

            itemTime = arrow.get(item.stat().st_mtime)
            if itemTime < criticalTime:
                os.remove(item)


# функция  вызова утилиты восстановления  копии БД Firebird  с необходимыми флагами  и указанием источника и приёмника
def restore():
    try:
        subprocess.check_call(
            [util_name, "-c", garbage_checkbox_var.get(), full_log_checkbox_var.get(), disable_compression_at_backup_checkbox_var.get(), backup_format_checkbox_var.get(), write_only_metadata_checkbox_var.get(), ignore_stuck_2pc_transactions_checkbox_var.get(), "-user",
             str(username_db_input.get()), "-pas", str(password_db_input.get()), database_filename, save_location_name + "/" + tmp2])
    except Exception as e:
        error_message(e)



# функция  вызова утилиты  резервного копирования  БД Firebird  с необходимыми флагами  и указанием истоника и приёмника
def backup():
    try:
        #del_files()
        subprocess.check_call(
            [util_name, "-b", full_log_checkbox_var.get(), garbage_checkbox_var.get(), disable_compression_at_backup_checkbox_var.get(), backup_format_checkbox_var.get(), write_only_metadata_checkbox_var.get(), ignore_stuck_2pc_transactions_checkbox_var.get(), "-user",
             str(username_db_input.get()), "-pas", str(password_db_input.get()), database_filename,
             save_location_name + "/" + database_temp[-1] + "." + now.strftime("%d-%m-%Y")])


    except Exception as e:
        error_message(e)


# функция обработчика кнопки "выбора каталога"
def backup_save_location_browse_button():
    global save_folder_path2
    global save_location_name
    global save_location_temp
    save_location_name = filedialog.askdirectory()
    save_folder_path2.set(save_location_name)
    save_location_temp = save_location_name.split("/")



################################################MAIN_WINDOW############################################################
win = tk.Tk()
win.title("GUI для утилиты резервного копирования и восстановления  БД Firebird gbak.exe")

garbage_checkbox_var = tk.StringVar()
full_log_checkbox_var = tk.StringVar()
full_log_checkbox_var.set("-v")
disable_compression_at_backup_checkbox_var = tk.StringVar()
backup_format_checkbox_var = tk.StringVar()
write_only_metadata_checkbox_var = tk.StringVar()
ignore_stuck_2pc_transactions_checkbox_var = tk.StringVar()

data_base_folder_path = tk.StringVar()
save_folder_path2 = tk.StringVar()
backup_util_folder_path3 = tk.StringVar()

##############################################LABELES#################################################################
name_util_label = tk.Label(win, text="1) Выбор утилиты", font=("Arial", 10, "bold"), anchor="center").grid(row=1, column=0, stick="w")

data_base_label = tk.Label(win, text="2) БД\Backup", font=("Arial", 10, "bold"), anchor="center").grid(row=2, column=0, stick="w")

save_db_label = tk.Label(win, text="3) Куда сохранить", font=("Arial", 10, "bold"), anchor="center").grid(row=3, column=0, stick="w")

username_db_label = tk.Label(win, text="4) имя пользователя БД", font=("Arial", 10, "bold"), anchor="center").grid(row=4, column=0, stick="w")

password_db_label = tk.Label(win, text="5) пароль БД", font=("Arial", 10, "bold"), anchor="center").grid(row=5, column=0, stick="w")

empty_down_label = tk.Label(text = "").grid(row = 7, column = 0)
empty_up_label = tk.Label(text = "Опции", font = ("bold")).grid(row = 0, column = 4)

backup_util_folder_path_label = tk.Label(master=win, textvariable=backup_util_folder_path3).grid(row=1, column=1)

data_base_folder_path_label = tk.Label(master=win, textvariable=data_base_folder_path).grid(row=2, column=1)


save_folder_path_label = tk.Label(master=win, textvariable=save_folder_path2).grid(row=3, column=1)



###############################################BUTTONS#################################################################
backup_button = tk.Button(win, text="Создание резервной копии", font=("bold"), command=backup, state="disabled")
backup_button.grid(row=8, column=1, stick="w")
restore_button = tk.Button(win, text="Восстановление из резервной копии", font=("bold"), command=restore, state="disabled")
restore_button.grid(row=8, column=4, stick="w")

browse_util_button = tk.Button(text="Выбрать№1", command=util_browse_button)

browse_util_button.grid(row=1, column=3)

browse_database_button = tk.Button(text="Выбрать№2", command=database_browse_button, state="disabled")
browse_database_button.grid(row=2, column=3)

save_backup_location_button = tk.Button(text="Выбрать№3", command=backup_save_location_browse_button, state="disabled")
save_backup_location_button.grid(row=3, column=3)

###########################################CHECKBOSES##################################################################
garbage_checkbox = tk.Checkbutton(win, text="отключить сборку мусора", variable=garbage_checkbox_var, onvalue="-g", offvalue="").grid(row=1, column=4, stick="w", padx = 10)

full_log_checkbox = tk.Checkbutton(win, text="вывод полного лога событий", variable=full_log_checkbox_var, onvalue="-v", offvalue="").grid(row=2, column=4, stick="w", padx = 10)

disable_compression_at_backup_checkbox = tk.Checkbutton(win, text="отключение сжатия при резервировании", variable=disable_compression_at_backup_checkbox_var, onvalue="-e", offvalue="").grid(row=3, column=4, stick="w", padx = 10)

backup_format_checkbox = tk.Checkbutton(win, text="формат резервной копии", variable=backup_format_checkbox_var, onvalue="-nt", offvalue="").grid(row=4, column=4, stick="w", padx = 10)

write_only_metadata_checkbox = tk.Checkbutton(win, text="запись только метаданных", variable=write_only_metadata_checkbox_var, onvalue="-m", offvalue="").grid(row=5, column=4, stick="w", padx = 10)

ignore_stuck_2pc_transactions_checkbox = tk.Checkbutton(win, text='''игнорировать изменения "застрявшие" транзакций 2PC ''', variable=ignore_stuck_2pc_transactions_checkbox_var,onvalue="-L", offvalue="").grid(row=6, column=4, stick="w", padx = 10)



#############################################INPUT_FIELDS###############################################################
username_db_input = tk.Entry(win)
username_db_input.bind('<KeyRelease>', check_backup_restore_on_key)
username_db_input.grid(row=4, column=1)
password_db_input = tk.Entry(win)
password_db_input.config(show="*")  # отображение звёздочек вместо пароля
password_db_input.bind('<KeyRelease>', check_backup_restore_on_key)
password_db_input.grid(row=5, column=1)



####################################################ENTRY_POINT########################################################
if __name__ == "__main__":
    #win.geometry("910x310+500+200")  # размеры активного окна
    win.mainloop()  # активация основного окна программы








