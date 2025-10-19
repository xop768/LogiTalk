from customtkinter import *
from socket import *
from threading import Thread
from tkinter.messagebox import *

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x300')
        self.title('Онлайн-чат')
        
        #---Меню налаштувань---
        self.frame = CTkFrame(self, width=200,
                              height=self.winfo_height())
        self.frame.pack_propagate(False)
        self.frame.configure(width=0)
        self.is_show_menu = False
        self.frame_speed = 20
        self.frame_width = 0
        self.frame.place(x=0, y=0)
        
        self.btn = CTkButton(self, text='меню', width=30,
                             command=self.toggle_show_menu)
        self.btn.place(x=0, y=0)
        
        self.label = CTkLabel(self.frame, text='Налаштування')
        self.label.pack(pady=30)
        self.name_entry = CTkEntry(self.frame,
                        placeholder_text="Ім'я/нікнейм")
        self.name_entry.pack()
        self.signup_btn = CTkButton(self.frame,
                                    text='Зареєструватися',
                                    command=self.sign_up)
        self.signup_btn.pack()
        self.change_theme = CTkOptionMenu(
            self.frame,
            values=['Темна тема', 'Світла тема']
        )
        self.change_theme.pack(pady=10)
        
        #---Вікно чату---
        self.chat_text = CTkTextbox(self,
                                    state='disabled',
                                    wrap='word')
        self.chat_text.place(x=0, y=30)
        
        self.message = CTkEntry(
            self, placeholder_text='Введіть повідомлення',
            width=200
        )
        self.message.place(x=0, y=250)
        
        self.send_button = CTkButton(self, text='>>',
                                     width=40, height=30,
                                     command=self.send_message)
        self.send_button.place(x=200, y=250)
        
        self.adaptive_ui()
        
        self.username = ''
        
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
        except:
            pass
    
    #---Перемикання меню---    
    def toggle_show_menu(self):
        if self.is_show_menu == True:
            self.is_show_menu = False
            self.close_menu()
        else:
            self.is_show_menu = True
            self.show_menu()
    
    #---Показати меню---
    def show_menu(self):
        if self.frame_width <= 200:
            self.frame_width += self.frame_speed
            self.frame.configure(
                width=self.frame_width,
                height=self.winfo_height())
        if self.is_show_menu == True:
            self.after(20, self.show_menu)
    
    #---Приховати меню---
    def close_menu(self):
        if self.frame_width >= 0:
            self.frame_width -= self.frame_speed
            self.frame.configure(
                width=self.frame_width,
                height=self.winfo_height())
        if self.is_show_menu == False:
            self.after(20, self.close_menu)
    
    #---Адаптивний інтерфейс---
    def adaptive_ui(self):
        self.chat_text.configure(
            width=self.winfo_width()-self.frame.winfo_width(),
            height=self.winfo_height()-self.send_button.winfo_height()-30
        )
        self.chat_text.place(x=self.frame.winfo_width())
        
        self.message.configure(
            width=self.winfo_width()-self.frame.winfo_width()-self.send_button.winfo_width()
        )
        self.message.place(
            x=self.frame.winfo_width(),
            y=self.winfo_height()-self.message.winfo_height()
        )
        
        self.send_button.place(
            x=self.winfo_width()-self.send_button.winfo_width(),
            y=self.winfo_height()-self.send_button.winfo_height()
        )
        
        self.after(20, self.adaptive_ui)
    
    #---Реєстрація користувача---
    def sign_up(self):
        try:
            if self.name_entry.get() == '':
                showerror('ПОМИЛКА!', 'Поле імені порожнє!')
            else:
                self.username = self.name_entry.get()
                self.add_message(f'Ваш нікнейм: {self.username}')
                hello = f'{self.username} приєднується'
                self.client_socket.sendall(hello.encode())
                self.name_entry.configure(state='disabled')
                self.signup_btn.configure(state='disabled')
        except:
            pass
    
    #---Додавання повідомлення у своє вікно чату---
    def add_message(self, text):
        self.chat_text.configure(state='normal')
        self.chat_text.insert(END, text + '\n')
        self.chat_text.configure(state='disabled')
    
    def send_message(self):
        message = self.message.get()
        if message != '':
            self.add_message(f'{self.username}: {message}')
            data = f'{self.username}: {message}'
            try:
                self.client_socket.sendall(data.encode())
            except:
                pass
        self.message.delete(0, END)
    
    #---Отримати повідомлення--
    def recv_message(self):
        while True:
            try:
                message = self.client_socket.recv(4096).decode()
                if message != '':
                    self.add_message(message)
            except:
                break
    
HOST = '127.0.0.1'
PORT = 8080

window = MainWindow()
window.mainloop()