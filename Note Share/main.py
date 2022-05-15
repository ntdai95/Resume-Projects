import os
import random
import re
import pygame as pg
import tkinter as tk
from tkinter import messagebox, ttk, Listbox
from tkinter.constants import END, CENTER, YES
from PIL import Image, ImageTk
from gtts import gTTS
from client import Client
from models import Message
import subprocess


USER = ""
NOTES = []
SHOW_NOTES = []


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("images/background.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        title = tk.Label(self, text="Welcome to NoteShare!", bg="magenta", font=("Arial Bold", 30))
        title.place(x=280, y=40)

        border = tk.LabelFrame(self, text='Login', bg='ivory', bd=10, font=("Arial", 40))
        border.pack(fill="both", expand="yes", padx=150, pady=150)

        L1 = tk.Label(border, text="Username:", font=("Arial Bold", 20), bg='ivory')
        L1.place(x=40, y=20)
        T1 = tk.Entry(self, font=("Arial Bold", 20))
        T1.place(x=380, y=230, width=380, height=50)

        L2 = tk.Label(border, text="Password:", font=("Arial Bold", 20), bg='ivory')
        L2.place(x=40, y=80)
        T2 = tk.Entry(self, width=30, show='*', font=("Arial Bold", 20))
        T2.place(x=380, y=290, width=380, height=50)

        def clear_entries():
            T1.delete(0, END)
            T2.delete(0, END)

        def signing_in():
            if T2.get():
                login_message = Client().send_action_message(Message(action="login",
                                                                     username=T1.get(),
                                                                     password=T2.get()).to_json())
                if login_message["success"]:
                    global USER
                    USER = T1.get()
                    controller.show_frame(MainPage)
                else:
                    messagebox.showinfo("Error", login_message["message"])
            else:
                messagebox.showinfo("Error", "Please, enter a password!")

        B1 = tk.Button(border, text="Sign in", font=("Arial", 20),
                       command=lambda: [signing_in(), clear_entries()])
        B1.place(x=420, y=160)

        def register():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Register")

            l1 = tk.Label(window, text="Account Setup", font=("Arial", 30), bg="deep sky blue")
            l1.place(x=280, y=40)

            l2 = tk.Label(window, text="Username:", font=("Arial", 30), bg="deep sky blue")
            l2.place(x=40, y=140)
            t2 = tk.Entry(window, font=("Arial", 20))
            t2.place(x=400, y=140, width=300, height=50)

            l3 = tk.Label(window, text="Email Address:", font=("Arial", 30), bg="deep sky blue")
            l3.place(x=40, y=200)
            t3 = tk.Entry(window, font=("Arial", 20))
            t3.place(x=400, y=200, width=300, height=50)

            l4 = tk.Label(window, text="Password:", font=("Arial", 30), bg="deep sky blue")
            l4.place(x=40, y=260)
            t4 = tk.Entry(window, show='*', font=("Arial", 20))
            t4.place(x=400, y=260, width=300, height=50)

            l5 = tk.Label(window, text="Confirm Password:", font=("Arial", 30), bg="deep sky blue")
            l5.place(x=40, y=320)
            t5 = tk.Entry(window, show='*', font=("Arial", 20))
            t5.place(x=400, y=320, width=300, height=50)

            def create_account():
                if not t2.get():
                    messagebox.showinfo("Error",
                                        "Username missing! Please, enter "
                                        "a username in the asked field!")
                elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', t3.get()):
                    messagebox.showinfo("Error", "Please, enter a valid email address!")
                elif not t4.get() and not t5.get():
                    messagebox.showinfo("Error",
                                        "Passwords missing! Please, enter the "
                                        "same password in the asked fields!")
                elif t4.get() == t5.get():
                    register_message = Client().send_action_message(Message(action="register",
                                                                            username=t2.get(),
                                                                            password=t4.get(),
                                                                            email=t3.get()).to_json())
                    if register_message["success"]:
                        messagebox.showinfo("Success", register_message["message"])
                        window.destroy()
                    else:
                        messagebox.showinfo("Error", register_message["message"])
                else:
                    messagebox.showinfo("Error",
                                        "Passwords mismatched! Please, enter "
                                        "the same password for confirmation!")

            b1 = tk.Button(window, text="Create Account", font=("Arial", 30), bg="#ffc22a",
                           command=lambda: [create_account(), clear_entries()])
            b1.place(x=250, y=400)

            window.geometry("760x500")
            window.mainloop()

        B2 = tk.Button(self, text="Register", bg="dark orange", font=("Arial", 20), command=register)
        B2.place(x=240, y=370)

        def change_password_email():
            if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', T3.get()):
                messagebox.showinfo("Error", "Please, enter a valid email address!")
            else:
                new_password = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(12)])
                password_email_message = Client().send_action_message(Message(action="password email",
                                                                              email=T3.get(),
                                                                              password=new_password).to_json())
                if password_email_message["success"]:
                    messagebox.showinfo("Success", password_email_message["message"])
                else:
                    messagebox.showinfo("Error", password_email_message["message"])

        L3 = tk.Label(self, text="Type your email below, if you forgot your login credentials:", font=("Arial Bold", 16), bg='ivory')
        L3.place(x=180, y=470)
        T3 = tk.Entry(self, font=("Arial Bold", 20))
        T3.place(x=200, y=520, width=440, height=50)
        B3 = tk.Button(self, text="Send!", bg="light green", font=("Arial", 20),
                       command=lambda: [change_password_email(), T3.delete(0, END)])
        B3.place(x=660, y=520)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("images/background.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        title = tk.Label(self, text="Please, select one of the options below!", bg="light blue", font=("Arial Bold", 30))
        title.place(x=120, y=60)

        def change_password():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Changing Password")

            l1 = tk.Label(window, text="Enter your new password below:", font=("Arial Bold", 30), bg="deep sky blue")
            l1.place(x=80, y=40)

            l2 = tk.Label(window, text="Password:", font=("Arial", 30), bg="deep sky blue")
            l2.place(x=40, y=200)
            t2 = tk.Entry(window, show='*', font=("Arial", 20))
            t2.place(x=400, y=200, width=300, height=50)

            l3 = tk.Label(window, text="Confirm Password:", font=("Arial", 30), bg="deep sky blue")
            l3.place(x=40, y=260)
            t3 = tk.Entry(window, show='*', font=("Arial", 20))
            t3.place(x=400, y=260, width=300, height=50)

            def change_password_username():
                if not t2.get() and not t3.get():
                    messagebox.showinfo("Error",
                                        "Passwords missing! Please, enter the "
                                        "same password in the asked fields!")
                elif t2.get() == t3.get():
                    password_username_message = Client().send_action_message(Message(action="password username",
                                                                                     username=USER,
                                                                                     password=t2.get()).to_json())
                    if password_username_message["success"]:
                        messagebox.showinfo("Success", password_username_message["message"])
                        window.destroy()
                    else:
                        messagebox.showinfo("Error", password_username_message["message"])
                else:
                    messagebox.showinfo("Error",
                                        "Passwords mismatched! Please, enter "
                                        "the same password for confirmation!")

            b1 = tk.Button(window, text="Change Password", font=("Arial", 30), bg="#ffc22a", command=change_password_username)
            b1.place(x=200, y=400)

            window.geometry("760x500")
            window.mainloop()

        B1 = tk.Button(self, text="Change Password", bg="brown", font=("Arial", 20), command=change_password)
        B1.place(x=340, y=260)

        def send_email():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Sending Email")

            l1 = tk.Label(window, text="Sending Email Message!", font=("Arial Bold", 30), bg="deep sky blue")
            l1.place(x=160, y=40)

            l2 = tk.Label(window, text="User:", font=("Arial", 30), bg="deep sky blue")
            l2.place(x=40, y=160)
            t2 = tk.Entry(window, font=("Arial", 20))
            t2.place(x=250, y=160, width=450, height=50)

            l3 = tk.Label(window, text="Message:", font=("Arial", 30), bg="deep sky blue")
            l3.place(x=40, y=220)
            t3 = tk.Entry(window, font=("Arial", 20))
            t3.place(x=250, y=220, width=450, height=140)

            def sending_email_message():
                password_username_message = Client().send_action_message(Message(action="send email",
                                                                                 username=USER,
                                                                                 receiving_username=t2.get(),
                                                                                 email_message=t3.get()).to_json())
                if password_username_message["success"]:
                    messagebox.showinfo("Success", password_username_message["message"])
                    window.destroy()
                else:
                    messagebox.showinfo("Error", password_username_message["message"])

            b1 = tk.Button(window, text="Send Email", font=("Arial", 30), bg="#ffc22a", command=sending_email_message)
            b1.place(x=260, y=400)

            window.geometry("760x500")
            window.mainloop()

        B2 = tk.Button(self, text="Send Email", bg="#ffc22a", font=("Arial", 20), command=send_email)
        B2.place(x=380, y=380)

        B3 = tk.Button(self, text="View Requests", bg="magenta", font=("Arial", 20),
                       command=lambda: controller.show_frame(RequestsPage))
        B3.place(x=360, y=500)

        def get_all_filenames():
            get_all_files_message = Client().send_action_message(Message(action="get all files").to_json())
            if get_all_files_message["success"]:
                global NOTES
                NOTES = get_all_files_message["message"]
            else:
                messagebox.showinfo("Error", get_all_files_message["message"])

        B4 = tk.Button(self, text="Upload File", font=("Arial", 20), command=lambda: controller.show_frame(UploadPage))
        B4.place(x=100, y=680)

        def delete_user():
            global USER
            USER = ""

        B5 = tk.Button(self, text="Logout", font=("Arial", 20),
                       command=lambda: [controller.show_frame(LoginPage), delete_user()])
        B5.place(x=410, y=680)

        B6 = tk.Button(self, text="Download File", font=("Arial", 20),
                       command=lambda: [controller.show_frame(DownloadPage), get_all_filenames()])
        B6.place(x=680, y=680)


class RequestsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='orange')

        Label = tk.Label(self, text="Current Requests", bg="green", font=("Arial Bold", 30))
        Label.place(x=300, y=60)

        def show_requests(requests):
            win = tk.Tk()
            win.configure(bg="deep sky blue")
            win.title("Requests")

            tree = ttk.Treeview(win, column=("TOPIC:", "USERNAME:", "CREATED:"), show='headings', height=20)
            tree.column("#1", anchor=CENTER)
            tree.heading("#1", text="TOPIC:")
            tree.column("#2", anchor=CENTER)
            tree.heading("#2", text="USERNAME:")
            tree.column("#3", anchor=CENTER)
            tree.heading("#3", text="CREATED:")

            for row in requests:
                tree.insert('', 'end', text="1", values=(row[0], row[1], row[2]))

            tree.grid(row=0, column=0, sticky='nsew')
            scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')
            win.geometry("622x430")
            win.mainloop()

        def view_request():
            get_all_requests_message = Client().send_action_message(Message(action="get all requests").to_json())
            if get_all_requests_message["success"]:
                requests = get_all_requests_message["message"]
                show_requests(requests)
            else:
                messagebox.showinfo("Error", get_all_requests_message["message"])

        L1 = tk.Label(self, text="Type the topic of the request that you want to add:", font=("Arial Bold", 20), bg='ivory')
        L1.place(x=40, y=320)
        T1 = tk.Entry(self, font=("Arial Bold", 20))
        T1.place(x=40, y=380, width=770, height=60)

        def add_request():
            add_request_message = Client().send_action_message(Message(action="add request",
                                                                       username=USER,
                                                                       topic=T1.get()).to_json())
            if add_request_message["success"]:
                messagebox.showinfo("Success", add_request_message["message"])
                T1.delete(0, END)
            else:
                messagebox.showinfo("Error", add_request_message["message"])

        L2 = tk.Label(self, text="Type the topic of the request that you want to delete:", font=("Arial Bold", 20), bg='ivory')
        L2.place(x=40, y=480)
        T2 = tk.Entry(self, width=30, font=("Arial Bold", 20))
        T2.place(x=40, y=540, width=740, height=60)

        def delete_request():
            delete_request_message = Client().send_action_message(Message(action="remove request",
                                                                          username=USER,
                                                                          topic=T2.get()).to_json())
            if delete_request_message["success"]:
                messagebox.showinfo("Success", delete_request_message["message"])
                T2.delete(0, END)
            else:
                messagebox.showinfo("Error", delete_request_message["message"])

        B1 = tk.Button(self, text="View Requests", font=("Arial", 20), bg="light blue", command=view_request)
        B1.place(x=360, y=200)

        B2 = tk.Button(self, text="Add", font=("Arial", 20), bg="light green", command=add_request)
        B2.place(x=840, y=380)

        B3 = tk.Button(self, text="Delete", font=("Arial", 20), bg="light green", command=delete_request)
        B3.place(x=810, y=540)

        B4 = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(MainPage))
        B4.place(x=140, y=680)

        def delete_user():
            global USER
            USER = ""

        B5 = tk.Button(self, text="Logout", font=("Arial", 20),
                       command=lambda: [controller.show_frame(LoginPage), delete_user()])
        B5.place(x=720, y=680)


class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='light blue')

        Label = tk.Label(self, text="Select your file!", bg="orange", font=("Arial Bold", 30))
        Label.place(x=330, y=60)

        def read_file():
            filepath = os.path.join(os.path.dirname(__file__), "{}.txt".format(T1.get()))
            if os.path.exists(filepath):
                if not os.path.exists(os.path.join(os.path.dirname(__file__), "audio")):
                    os.makedirs(os.path.join(os.path.dirname(__file__), "audio"))

                speechpath = os.path.join(os.path.join(os.path.dirname(__file__), "audio", "{}.mp3".format(T1.get())))
                if not os.path.exists(speechpath):
                    with open(filepath, "r") as file_object:
                        lines = file_object.readlines()
                        for line in lines:
                            line = line.rstrip()
                            if line.replace(" ", "") != "":
                                break
                        speech = gTTS(text=str(line), lang="en", slow=False)
                        speech.save(speechpath)
                pg.mixer.init()
                pg.mixer.music.load(speechpath)
                pg.mixer.music.set_volume(0.2)
                pg.mixer.music.play()
                T1.delete(0, END)
            else:
                messagebox.showinfo("Error", "File not found. Note that only .txt files can be read!\n"
                                             "Please, enter a valid filename without the .txt extension!")

        L1 = tk.Label(self, text="Type your filename without the .txt extension to read the first line:", font=("Arial Bold", 20), bg='ivory')
        L1.place(x=40, y=180)
        T1 = tk.Entry(self, width=30, font=("Arial Bold", 20))
        T1.place(x=40, y=240, width=795, height=40)
        B1 = tk.Button(self, text="Read", font=("Arial", 16), bg="#ffc22a", command=read_file)
        B1.place(x=850, y=240)

        def clear_entries():
            T2.delete(0, END)
            T3.delete(0, END)

        def upload_filename():
            filepath = os.path.join(os.path.dirname(__file__), T2.get())
            if os.path.exists(filepath):
                subprocess.call(f"EncodeFile.sh {T2.get()}", shell=True)
                upload_message = Client().send_action_message(Message(action="upload",
                                                                      username=USER,
                                                                      filename=T2.get(),
                                                                      tag=T3.get()).to_json())
                subprocess.call(f"del {T2.get()}.code", shell=True)
                if upload_message["success"]:
                    messagebox.showinfo("Success", upload_message["message"])
                    clear_entries()
                else:
                    messagebox.showinfo("Error", upload_message["message"])
            else:
                messagebox.showinfo("Error", "File not found! Please, enter a valid filename with the file extension!")

        L2 = tk.Label(self, text="Type your filename with the file extension:", font=("Arial Bold", 20), bg='ivory')
        L2.place(x=40, y=340)
        T2 = tk.Entry(self, font=("Arial Bold", 20))
        T2.place(x=40, y=400, width=875, height=40)

        L3 = tk.Label(self, text="Type a tag that you want to associate with your file:", font=("Arial Bold", 20), bg='ivory')
        L3.place(x=40, y=500)
        T3 = tk.Entry(self, width=30, font=("Arial Bold", 20))
        T3.place(x=40, y=560, width=875, height=40)

        B2 = tk.Button(self, text="Upload", font=("Arial", 20), bg="#ffc22a", command=upload_filename)
        B2.place(x=420, y=680)

        B3 = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(MainPage))
        B3.place(x=140, y=680)

        def delete_user():
            global USER
            USER = ""

        B4 = tk.Button(self, text="Logout", font=("Arial", 20),
                       command=lambda: [controller.show_frame(LoginPage), delete_user()])
        B4.place(x=720, y=680)


class DownloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='light green')

        Label = tk.Label(self, text="Available Notes:", bg="orange", font=("Arial Bold", 30))
        Label.place(x=320, y=60)

        def read_file():
            filepath = os.path.join(os.path.dirname(__file__), "{}.txt".format(T1.get()))
            if os.path.exists(filepath):
                if not os.path.exists(os.path.join(os.path.dirname(__file__), "audio")):
                    os.makedirs(os.path.join(os.path.dirname(__file__), "audio"))

                speechpath = os.path.join(os.path.join(os.path.dirname(__file__), "audio", "{}.mp3".format(T1.get())))
                if not os.path.exists(speechpath):
                    with open(filepath, "r") as file_object:
                        lines = file_object.readlines()
                        for line in lines:
                            line = line.rstrip()
                            if line.replace(" ", "") != "":
                                break
                        speech = gTTS(text=str(line), lang="en", slow=False)
                        speech.save(speechpath)
                pg.mixer.init()
                pg.mixer.music.load(speechpath)
                pg.mixer.music.set_volume(0.2)
                pg.mixer.music.play()
                T1.delete(0, END)
            else:
                messagebox.showinfo("Error", "File not found. Note that only .txt files can be read!\n"
                                             "Please, enter a valid filename without the .txt extension!")

        L1 = tk.Label(self, text="Type your filename without the .txt extension to read the first line:", font=("Arial Bold", 20), bg='ivory')
        L1.place(x=35, y=180)
        T1 = tk.Entry(self, width=30, font=("Arial Bold", 20))
        T1.place(x=35, y=240, width=798, height=40)
        B1 = tk.Button(self, text="Read", font=("Arial", 16), command=read_file)
        B1.place(x=848, y=240)

        def show_notes():
            win = tk.Tk()
            win.configure(bg="deep sky blue")
            win.title("Files")

            tree = ttk.Treeview(win, column=("FILENAME:", "USERNAME:", "TAG:", "CREATED:"), show='headings', height=20)
            tree.column("#1", anchor=CENTER)
            tree.heading("#1", text="FILENAME:")
            tree.column("#2", anchor=CENTER)
            tree.heading("#2", text="USERNAME:")
            tree.column("#3", anchor=CENTER)
            tree.heading("#3", text="TAG:")
            tree.column("#4", anchor=CENTER)
            tree.heading("#4", text="CREATED:")

            for row in SHOW_NOTES:
                tree.insert('', 'end', text="1", values=(row[0], row[1], row[2], row[3]))

            tree.grid(row=0, column=0, sticky='nsew')
            scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.grid(row=0, column=1, sticky='ns')
            win.geometry("822x430")
            win.mainloop()

        def search_filename():
            if NOTES == []:
                messagebox.showinfo("Error", "There is no note file currently on the server!")
            else:
                def binary_search(array, low, high, filename):
                    if high >= low:
                        middle = (high + low) // 2
                        if array[middle][0] == filename:
                            return middle
                        elif array[middle][0] > filename:
                            return binary_search(array, low,
                                                 middle - 1, filename)
                        else:
                            return binary_search(array, middle + 1,
                                                 high, filename)
                    else:
                        return -1
                result = binary_search(NOTES, 0, len(NOTES) - 1, T2.get())
                T2.delete(0, END)

                global SHOW_NOTES
                SHOW_NOTES = []
                if result != -1:
                    SHOW_NOTES.append(NOTES[result])
                show_notes()

        L2 = tk.Label(self, text="Search filename:", font=("Arial Bold", 20), bg='ivory')
        L2.place(x=40, y=510)
        T2 = tk.Entry(self, font=("Arial Bold", 20))
        T2.place(x=280, y=510, width=530, height=40)
        B2 = tk.Button(self, text="Search", font=("Arial", 16), command=search_filename)
        B2.place(x=825, y=510)

        def show_files(category_choice, order_choice):
            if NOTES == []:
                messagebox.showinfo("Error", "There is no note file currently on the server!")
            elif category_choice == ():
                messagebox.showinfo("Error", "Please, select a category to sort the notes by!")
            elif order_choice == ():
                messagebox.showinfo("Error", "Please, select an order to sort the notes by!")
            else:
                def mergeSort(array, category_choice, order_choice):
                    if len(array) > 1:
                        mid = len(array) // 2
                        L = array[:mid]
                        R = array[mid:]

                        mergeSort(array=L, category_choice=category_choice,
                                  order_choice=order_choice)
                        mergeSort(array=R, category_choice=category_choice,
                                  order_choice=order_choice)

                        i = j = k = 0
                        while i < len(L) and j < len(R):
                            if (L[i][category_choice] < R[j][category_choice] and order_choice == 0) or \
                               (L[i][category_choice] > R[j][category_choice] and order_choice == 1):
                                array[k] = L[i]
                                i += 1
                            else:
                                array[k] = R[j]
                                j += 1
                            k += 1

                        while i < len(L):
                            array[k] = L[i]
                            i += 1
                            k += 1

                        while j < len(R):
                            array[k] = R[j]
                            j += 1
                            k += 1

                global SHOW_NOTES
                SHOW_NOTES = []
                for row in NOTES:
                    SHOW_NOTES.append(row)

                if category_choice[0] != 0 and len(SHOW_NOTES) > 1:
                    mergeSort(array=SHOW_NOTES,
                              category_choice=category_choice[0],
                              order_choice=order_choice[0])
                elif category_choice[0] == 0 and order_choice[0] == 1:
                    SHOW_NOTES.reverse()
                show_notes()

        S1 = tk.Label(self, text="Sort Categories:", bg="orange", font=("Arial Bold", 20))
        S1.place(x=90, y=320)
        s1 = Listbox(self, selectmode="SINGLE", exportselection=0, font=16)
        s1.pack(expand=YES, fill="both")
        s1.place(x=140, y=370, width=120, height=100)
        category_choices = ["FILENAME", "USERNAME", "TAG", "CREATED"]
        for each_item in range(len(category_choices)):
            s1.insert(END, category_choices[each_item])
            s1.itemconfig(each_item, bg="yellow" if each_item % 2 == 0 else "cyan")

        S2 = tk.Label(self, text="Sort Orders:", bg="orange", font=("Arial Bold", 20))
        S2.place(x=420, y=350)
        s2 = Listbox(self, selectmode="SINGLE", exportselection=0, font=16)
        s2.pack(expand=YES, fill="both")
        s2.place(x=430, y=400, width=140, height=50)
        sort_choices = ["ASCENDING", "DESCENDING"]
        for each_item in range(len(sort_choices)):
            s2.insert(END, sort_choices[each_item])
            s2.itemconfig(each_item, bg="yellow" if each_item % 2 == 0 else "cyan")

        B3 = tk.Button(self, text="Show Notes", bg="dark orange", font=("Arial", 20),
                       command=lambda: show_files(s1.curselection(), s2.curselection()))
        B3.place(x=692, y=370)

        def download_filename():
            if NOTES == []:
                messagebox.showinfo("Error", "There is no note file currently on the server!")
                T4.delete(0, END)
            elif T4.get() in [row[0] for row in NOTES]:
                download_message = Client().send_action_message(Message(action="download", filename=T4.get()).to_json())
                subprocess.call(f"DecodeFile.sh {T4.get()}", shell=True)
                subprocess.call(f"del {T4.get()}.code", shell=True)
                messagebox.showinfo("Success", download_message["message"])
                T4.delete(0, END)
            else:
                messagebox.showinfo("Error",
                                    "The requested filename does not exist. "
                                    "Please, enter an existing filename "
                                    "with the file extension!")

        L4 = tk.Label(self, text="File to download:", font=("Arial Bold", 20), bg='ivory')
        L4.place(x=40, y=590)
        T4 = tk.Entry(self, width=30, font=("Arial Bold", 20))
        T4.place(x=290, y=590, width=495, height=40)
        B4 = tk.Button(self, text="Download", font=("Arial", 16), command=download_filename)
        B4.place(x=800, y=590)

        B5 = tk.Button(self, text="Back", font=("Arial", 20), command=lambda: controller.show_frame(MainPage))
        B5.place(x=140, y=680)

        def delete_user():
            global USER
            USER = ""

        B6 = tk.Button(self, text="Logout", font=("Arial", 20),
                       command=lambda: [controller.show_frame(LoginPage), delete_user()])
        B6.place(x=720, y=680)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        window.pack()
        window.grid_columnconfigure(0, minsize=960)
        window.grid_rowconfigure(0, minsize=780)

        self.frames = {}
        for F in (LoginPage, MainPage, RequestsPage, UploadPage, DownloadPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("NoteShare")


if __name__ == "__main__":
    app = Application()
    app.maxsize(1000, 800)
    app.mainloop()
