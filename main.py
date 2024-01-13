from tkinter import *
from model import *
from tkinter import ttk
import requests
import webbrowser
import yadisk
import datetime

globalId = -1
diskName = ''

API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()
url = 'https://www.googleapis.com/customsearch/v1'

with db:
    db.create_tables([
        Client, SuperUser, Requests
    ])


def backup_db():
    global diskName
    dt_now = datetime.datetime.now().strftime("%c")
    # Подключение к базе данных

    # Создание курсора
    cur = db.cursor()

    # Получение списка всех таблиц в базе данных
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()

    y = yadisk.YaDisk(token='y0_AgAAAABpucOuAAsP-gAAAAD2ON1e6MYSWtHLRZWtiRKBU-MW2ntmPm4')

    diskName = '/BD'
    diskName += dt_now
    y.mkdir(diskName)
    for table in tables:
        table_name = table[0]
        cur.copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER", open(f"{table_name}.csv", 'w'))
        y.upload(f"{table_name}.csv", f"{diskName}/{table_name}.csv")
    # Создание временной директории для резервной копии

    # Закрытие соединения с базой данных
    cur.close()


def enter_program(event):
    global globalId
    user = Client.select().where((Client.login == username_entry.get()) & (Client.password == password_entry.get()))
    admin = SuperUser.select().where(
        (SuperUser.username == username_entry.get()) & (SuperUser.password == password_entry.get()))
    if len(admin) == 0:
        if len(user) == 0:
            new_window = Toplevel(window)
            new_window.title("Ошибка")
            new_window.resizable(width=False, height=False)
            screen_width1 = window.winfo_screenwidth()
            screen_height1 = window.winfo_screenheight()
            x1 = (screen_width1 // 2) - (460 // 2)
            y1 = (screen_height1 // 2) - (70 // 2)
            new_window.geometry(f"{460}x{70}+{x1}+{y1}")
            new_window.configure(bg="black")
            new_window.grab_set()
            label = Label(new_window, text="Такого пользователя не существует!Зарегистрируйтесь", fg="red", bg="black",
                          font=("Times New Roman", 14))
            registration_button1 = Button(new_window, text="Ок", width=10)
            registration_button1.bind("<Button-1>", lambda event: new_window.destroy())
            label.grid(row=0, column=0, sticky="nsew", columnspan=2)  # установка параметра sticky
            registration_button1.grid(row=1, column=0, ipadx=20, columnspan=2)
        else:
            u = Client.get(Client.login == username_entry.get())
            globalId = u.client_id
            new_window = Toplevel(window)
            new_window.configure(bg="black")
            new_window.title("Идет загрузка")
            screen_width1 = window.winfo_screenwidth()
            screen_height1 = window.winfo_screenheight()

            # Вычислить координаты x и y для центрирования окна
            x1 = (screen_width1 // 2) - (500 // 2)
            y1 = (screen_height1 // 2) - (100 // 2)
            new_window.geometry(f"{500}x{100}+{x1}+{y1}")
            label = Label(new_window, text="Здравствуйте," + username_entry.get() + "!", font=("Times New Roman", 14),
                          bg="black", fg="orange")
            progress_bar = ttk.Progressbar(new_window, orient='horizontal', length=200, mode='determinate')
            label.pack()
            progress_bar.pack(pady=10)
            progress_bar.start(1000)
            progress_bar.step(94)

            new_window.after(5000, lambda: [new_window.destroy(), window.destroy(), User()])
    else:
        new_window = Toplevel(window)
        new_window.configure(bg="black")
        new_window.title("Идет загрузка")
        screen_width1 = window.winfo_screenwidth()
        screen_height1 = window.winfo_screenheight()

        # Вычислить координаты x и y для центрирования окна
        x1 = (screen_width1 // 2) - (500 // 2)
        y1 = (screen_height1 // 2) - (100 // 2)
        new_window.geometry(f"{500}x{100}+{x1}+{y1}")
        label = Label(new_window, text="Здравствуйте,Admin:" + username_entry.get() + "!", font=("Times New Roman", 14),
                      bg="black", fg="orange")
        progress_bar = ttk.Progressbar(new_window, orient='horizontal', length=200, mode='determinate')
        label.pack()
        progress_bar.pack(pady=10)
        progress_bar.start(1000)
        progress_bar.step(94)
        new_window.after(5000, lambda: [new_window.destroy(), window.destroy(), Admin()])


def enter_google(event, link):
    webbrowser.register('chrome', None,
                        webbrowser.BackgroundBrowser("C:/Program Files/Google/Chrome/Application/chrome.exe"))
    webbrowser.get('chrome').open(link)


def google_search(event, entry_pars, window1):
    new_req = Requests(username_id=globalId, name_request=entry_pars.get())
    new_req.save()
    query = entry_pars.get()
    param = {
        'q': query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID
    }
    response = requests.get(url, params=param)
    results = response.json()['items']
    links = []
    for item in results:
        links.append(item['link'])
    new_window = Toplevel(window1)
    new_window.resizable(width=False, height=False)
    screen_width1 = window1.winfo_screenwidth()
    screen_height1 = window1.winfo_screenheight()
    new_window.title("Ссылки на сайты с данными по запросу")
    new_window.configure(bg="black")
    x1 = (screen_width1 // 2) - (300 // 2)
    y1 = (screen_height1 // 2) - (300 // 2)
    new_window.geometry(f"{400}x{300}+{x1}+{y1}")
    count = 1
    j = 1
    for link in links:
        label = Label(new_window, text=f"{j})" + link, fg="orange", cursor="hand2", bg="black")
        label.grid(row=count, column=0, sticky="w")
        label.bind("<Button-1>", lambda event, link=link: enter_google(event, link))
        count += 1
        j += 1


def User():
    window1 = Tk()
    window1.resizable(width=False, height=False)
    screen_width1 = window1.winfo_screenwidth()
    screen_height1 = window1.winfo_screenheight()
    window1.title("User")

    x1 = (screen_width1 // 2) - (580 // 2)
    y1 = (screen_height1 // 2) - (50 // 2)
    window1.geometry(f"{580}x{50}+{x1}+{y1}")
    window1.configure(bg="black")
    label = Label(window1, text="Ввод", fg="orange", bg="black")
    button_pars = Button(window1, text="Parsing", bg="orange")

    entry_pars = Entry(window1, font=("Times New Roman", 12))
    entry_pars.configure(width=61)

    label.grid(row=1, column=0)  # Center label in window1
    entry_pars.grid(row=1, column=1, ipadx=20)
    button_pars.grid(row=2, column=0, columnspan=3)
    button_pars.bind("<Button-1>", lambda event: google_search(event, entry_pars, window1))
    window1.mainloop()


def del_user(event, login_, new_window, window1):
    query = Client.delete().where(Client.login == login_)
    query.execute()
    new_window.destroy()
    editor(event, window1)


def menu_editor(event, new_window, login_, window1):
    context_menu = Menu(new_window, tearoff=0)
    context_menu.add_command(label="Посмотреть данные")
    context_menu.add_command(label="Удалить пользователя", command=lambda: del_user(event, login_, new_window, window1))
    context_menu.post(event.x_root, event.y_root)


def editor(event, window1):
    all_user_names = Client.select(Client.login)
    new_window = Toplevel(window1)
    screen_width1 = window1.winfo_screenwidth()
    screen_height1 = window1.winfo_screenheight()
    new_window.title("Редактор")

    x1 = (screen_width1 // 2) - (1024 // 2)
    y1 = (screen_height1 // 2) - (512 // 2)
    new_window.geometry(f"{1024}x{512}+{x1}+{y1}")
    new_window.configure(bg="black")
    count = 1
    j = 1

    for widget in new_window.winfo_children():
        widget.destroy()

    for login_ in all_user_names:
        label = Label(new_window, text=f"{j})" + f"{login_.login}", fg="orange", cursor="hand2", bg="black",
                      font=("Times New Roman", 12))
        label.grid(row=count, column=0, sticky="w")
        count += 1
        j += 1
        label.bind("<Button-3>", lambda event, login=login_.login: menu_editor(event, new_window, login, window1))

    new_window.mainloop()


def Admin():
    window1 = Tk()
    window1.resizable(width=False, height=False)
    screen_width1 = window1.winfo_screenwidth()
    screen_height1 = window1.winfo_screenheight()
    window1.title("Admin")

    x1 = (screen_width1 // 2) - (1024 // 2)
    y1 = (screen_height1 // 2) - (512 // 2)
    window1.geometry(f"{1024}x{512}+{x1}+{y1}")
    window1.configure(bg="black")

    enter_button1 = Button(window1, text="Редактор", fg="orange", bg="black")
    registration_button1 = Button(window1, text="История запросов", fg="orange", bg="black")
    enter_button1.grid(row=0, column=0, ipadx=20)
    registration_button1.grid(row=0, column=1, ipadx=20)
    enter_button1.bind("<Button-1>", lambda event: editor(event, window1))
    window1.mainloop()


def registration(event, username_entry1, password_entry1, new_window):
    global diskName
    user = Client.select().where((Client.login == username_entry1.get()) & (Client.password == password_entry1.get()))
    if len(user) == 0 and len(username_entry1.get()) != 0 and len(password_entry1.get()) != 0:
        new_client = Client(login=username_entry1.get(), password=password_entry1.get())
        new_client.save()
        new_window.destroy()
    else:
        new_window1 = Toplevel(new_window)
        if len(username_entry1.get()) == 0 or len(password_entry1.get()) == 0:
            label = Label(new_window1, text="Поля не должны быть пустыми", fg="red")
        else:
            label = Label(new_window1, text="Такой пользователь существует", fg="red")
        label.pack()
    backup_db()


def enter_registration(event):
    new_window = Toplevel(window)
    new_window.configure(bg="black")
    new_window.resizable(width=False, height=False)
    x1 = (screen_width // 2) - (740 // 2)
    y1 = (screen_height // 2) - (100 // 2)
    new_window.geometry(f"{740}x{100}+{x1}+{y1}")
    new_window.grab_set()
    label1 = Label(new_window, text="Регистрация", width=100, bg="black", fg="orange")
    username_label1 = Label(new_window, text="Логин", bg="black", fg="orange")
    password_label1 = Label(new_window, text="Пароль", bg="black", fg="orange")
    registration_button1 = Button(new_window, text="Зарегистрироваться", bg="orange")
    username_entry1 = Entry(new_window, width=100)
    password_entry1 = Entry(new_window, width=100)
    label1.grid(row=0, column=1)
    username_label1.grid(row=1, column=0)
    username_entry1.grid(row=1, column=1)
    password_label1.grid(row=2, column=0)
    password_entry1.grid(row=2, column=1)
    registration_button1.grid(row=3, column=1, ipadx=20)
    registration_button1.bind("<Button-1>",
                              lambda event: registration(event, username_entry1, password_entry1, new_window))


if __name__ == "__main__":
    window = Tk()
    window.resizable(width=False, height=False)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.title("Вход в приложение")
    window.configure(bg="black")
    x = (screen_width // 2) - (220 // 2)
    y = (screen_height // 2) - (70 // 2)
    window.geometry(f"{220}x{70}+{x}+{y}")
    username_label = Label(window, text="Логин", fg="orange", bg="black")
    password_label = Label(window, text="Пароль", fg="orange", bg="black")
    username_entry = Entry(window)
    password_entry = Entry(window, show="*")
    enter_button = Button(window, text="Войти", bg="orange")
    registration_button = Button(window, text="Регистрация", bg="orange")
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    enter_button.grid(row=3, column=0, ipadx=20)
    registration_button.grid(row=3, column=1, ipadx=20)
    enter_button.bind("<Button-1>", enter_program)
    registration_button.bind("<Button-1>", enter_registration)
    window.mainloop()
