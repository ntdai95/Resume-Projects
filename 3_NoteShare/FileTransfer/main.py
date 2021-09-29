import os
import random
import re
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import END
from PIL import Image, ImageTk
from client import Client
from models import Message


USER = ""
NOTES = []


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/background.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0,y=0)

        title = tk.Label(self, text="Welcome to NoteShare!", bg="magenta", font=("Arial Bold", 30))
        title.place(x=280, y=40)
        
        border = tk.LabelFrame(self, text='Login', bg='ivory', bd=10, font=("Arial", 40))
        border.pack(fill="both", expand="yes", padx = 150, pady=150)
        
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
            login_message = Client().send_action_message(Message(action="login", username=T1.get(),
                                                               password=T2.get()).to_json())
            if login_message["success"]:
                global USER
                USER = T1.get()
                controller.show_frame(UploadDownloadPage)
            else:
                messagebox.showinfo("Error", login_message["message"])
         
        B1 = tk.Button(border, text="Sign in", font=("Arial", 20),
                       command=lambda: [signing_in(), clear_entries()])
        B1.place(x=420, y=160)
        
        def register():
            window = tk.Tk()
            window.resizable(0,0)
            window.configure(bg="deep sky blue")
            window.title("Register")

            l1 = tk.Label(window, text="Account Setup", font=("Arial", 30), bg="deep sky blue")
            l1.place(x=280, y=40)

            l2 = tk.Label(window, text="Username:", font=("Arial", 30), bg="deep sky blue")
            l2.place(x=40, y=140)
            t2 = tk.Entry(window, font=("Arial", 20))
            t2.place(x = 400, y=140, width=300, height=50)

            l3 = tk.Label(window, text="Email Address:", font=("Arial", 30), bg="deep sky blue")
            l3.place(x=40, y=200)
            t3 = tk.Entry(window, font=("Arial", 20))
            t3.place(x = 400, y=200, width=300, height=50)
            
            l4 = tk.Label(window, text="Password:", font=("Arial", 30), bg="deep sky blue")
            l4.place(x=40, y=260)
            t4 = tk.Entry(window, show='*', font=("Arial", 20))
            t4.place(x = 400, y=260, width=300, height=50)
            
            l5 = tk.Label(window, text="Confirm Password:", font=("Arial", 30), bg="deep sky blue")
            l5.place(x=40, y=320)
            t5 = tk.Entry(window, show='*', font=("Arial", 20))
            t5.place(x = 400, y=320, width=300, height=50)
            
            def create_account():
                if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', t3.get()):
                    messagebox.showinfo("Error", "Please, enter a valid email address!")
                elif t4.get() == t5.get():
                    register_message = Client().send_action_message(Message(action="register", username=t2.get(), 
                                                                            password=t4.get(), email=t3.get()).to_json())
                    if register_message["success"]:
                        messagebox.showinfo("Success", register_message["message"])
                        window.destroy()
                    else:
                        messagebox.showinfo("Error", register_message["message"])
                else:
                    messagebox.showinfo("Error", "Passwords mismatched! Please, enter the same password for confirmation!")
                    
            b1 = tk.Button(window, text="Create Account", font=("Arial",30),
                           bg="#ffc22a", command=lambda: [create_account(), clear_entries()])
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
                password_email_message = Client().send_action_message(Message(action="password email", email=T3.get(), 
                                                                              password=new_password).to_json())
                if password_email_message["success"]:
                    messagebox.showinfo("Success", password_email_message["message"])
                else:
                    messagebox.showinfo("Error", password_email_message["message"])

        L3 = tk.Label(self, text="Type your email below, if you forgot your login credentials:",
                      font=("Arial Bold", 16), bg='ivory')
        L3.place(x=180, y=470)
        T3 = tk.Entry(self, font=("Arial Bold", 20))
        T3.place(x=200, y=520, width=440, height=50)
        B3 = tk.Button(self, text="Send!", bg="light green", font=("Arial", 20),
                       command=lambda: [change_password_email(), T3.delete(0, END)])
        B3.place(x=660, y=520)
        

class UploadDownloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/background.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0,y=0)

        title = tk.Label(self, text="Important instructions before uploading\nor after downloading your file!",
                         bg="red", font=("Arial Bold", 30))
        title.place(x=120, y=40)
        
        L1 = tk.Label(self, text="Uploading: Before uploading your .txt file, you need to\n"
                                 "compress it to a .code file. To do that, you need to open\n"
                                 "command prompt on Windows or terminal on Mac OS, navigate to\n"
                                 "the current directory, and then type the following command:\n"
                                 "java Huffman/Encode.java <filename without extensions>", 
                      bg = "light blue", font=("Arial Bold", 20))
        L1.place(x=40, y=220)

        L2 = tk.Label(self, text="Downloading: After downloading your .code file, you need to\n"
                                 "decompress it to a .txt file. To do that, you need to open\n"
                                 "command prompt on Windows or terminal on Mac OS, navigate to\n"
                                 "the current directory, and then type the following command:\n"
                                 "java Huffman/Decode.java <filename without extensions>", 
                      bg = "light green", font=("Arial Bold", 20))
        L2.place(x=40, y=440)

        def change_password():
            window = tk.Tk()
            window.resizable(0,0)
            window.configure(bg="deep sky blue")
            window.title("Changing Password!")

            l1 = tk.Label(window, text="Enter your new password below:",
                          font=("Arial Bold", 30), bg="deep sky blue")
            l1.place(x=80, y=40)

            l2 = tk.Label(window, text="Password:", font=("Arial", 30), bg="deep sky blue")
            l2.place(x=40, y=200)
            t2 = tk.Entry(window, show='*', font=("Arial", 20))
            t2.place(x = 400, y=200, width=300, height=50)
            
            l3 = tk.Label(window, text="Confirm Password:", font=("Arial", 30), bg="deep sky blue")
            l3.place(x=40, y=260)
            t3 = tk.Entry(window, show='*', font=("Arial", 20))
            t3.place(x = 400, y=260, width=300, height=50)

            def change_password_username():
                if t2.get() == t3.get():
                    password_username_message = Client().send_action_message(Message(action="password username", username=USER, 
                                                                                   password=t2.get()).to_json())
                    if password_username_message["success"]:
                        messagebox.showinfo("Success", password_username_message["message"])
                    else:
                        messagebox.showinfo("Error", password_username_message["message"])
                    window.destroy()
                else:
                    messagebox.showinfo("Error", "Passwords mismatched! Please, enter the same password for confirmation!")
                    
            b1 = tk.Button(window, text="Change Password!", font=("Arial", 30),
                           bg="#ffc22a", command=change_password_username)
            b1.place(x=200, y=400)
            
            window.geometry("760x500")
            window.mainloop()

        B1 = tk.Button(self, text="Change Password!", bg="purple",
                       font=("Arial", 20), command=change_password)
        B1.place(x=360, y=680)

        def get_all_filenames():
            get_all_files_message = Client().send_action_message(Message(action="get all files").to_json())
            if get_all_files_message["success"]:
                global NOTES
                NOTES = get_all_files_message["message"]
            else:
                messagebox.showinfo("Error", get_all_files_message["message"])
        
        B2 = tk.Button(self, text="Upload", font=("Arial", 20), 
                       command=lambda: controller.show_frame(UploadPage))
        B2.place(x=720, y=680)
        
        B3 = tk.Button(self, text="Download", font=("Arial", 20), 
                       command=lambda: [controller.show_frame(DownloadPage), get_all_filenames()])
        B3.place(x=120, y=680)
        

class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg='light blue')
        
        Label = tk.Label(self, text="Select your file!", bg="orange", font=("Arial Bold", 30))
        Label.place(x=330, y=60)

        L1 = tk.Label(self, text="Type your filename without the .code extension:",
                      font=("Arial Bold", 25), bg='ivory')
        L1.place(x=40, y=200)
        T1 = tk.Entry(self, font=("Arial Bold", 30))
        T1.place(x=40, y=260, width=860, height=60)
        
        L2 = tk.Label(self, text="Type a tag that you want to associate with your file:",
                      font=("Arial Bold", 25), bg='ivory')
        L2.place(x=40, y=360)
        T2 = tk.Entry(self, width = 30, font=("Arial Bold", 30))
        T2.place(x=40, y=420, width=860, height=60)

        def upload_filename():
            if os.path.exists("{}.code".format(T1.get())):
                upload_message = Client().send_action_message(Message(action="upload", username=USER,
                                                                      filename=T1.get(), tag=T2.get()).to_json())
                if upload_message["success"]:
                    messagebox.showinfo("Success", upload_message["message"])
                else:
                    messagebox.showinfo("Error", upload_message["message"])
            else:
                messagebox.showinfo("Error", "File not found! Please, enter a valid filename without the .code extension!")

        B1 = tk.Button(self, text="Upload!", font=("Arial", 30), bg="#ffc22a", command=upload_filename)
        B1.place(x=380, y=520)

        def delete_user():
            global USER
            USER = ""

        B2 = tk.Button(self, text="Logout", font=("Arial", 20), 
                       command=lambda: [controller.show_frame(LoginPage), delete_user()])
        B2.place(x=720, y=680)
        
        B3 = tk.Button(self, text="Back", font=("Arial", 20), 
                       command=lambda: controller.show_frame(UploadDownloadPage))
        B3.place(x=140, y=680)


class DownloadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='light green')
        
        Label = tk.Label(self, text="Available Notes:", bg="orange", font=("Arial Bold", 30))
        Label.place(x=320, y=60)

        L1 = tk.Label(self, text="Search filename:", font=("Arial Bold", 20), bg='ivory')
        L1.place(x=40, y=200)
        T1 = tk.Entry(self, font=("Arial Bold", 20))
        T1.place(x=280, y=200, width=520, height=40)

        def search_filename():
            if NOTES == []:
                messagebox.showinfo("Error", "There is no note file currently on the server!")
            else:
                # Implement binary search
                print(NOTES)
                pass

        B1 = tk.Button(self, text="Search", font=("Arial", 16), command=search_filename)
        B1.place(x=820, y=200)

        def show_files():
            if NOTES == []:
                messagebox.showinfo("Error", "There is no note file currently on the server!")
            else:
                # Implement mergesort by tag if selected
                print(NOTES)
                pass
        
        B3 = tk.Button(self, text="Show Notes", bg="dark orange", font=("Arial", 20), command=show_files)
        B3.place(x=300, y=360)

        sort_by_tag = tk.IntVar()
        sort_by_tag.set(0)
        B2 = tk.Checkbutton(self, text="Sort\nby tag", variable=sort_by_tag,
                            offvalue = 0, onvalue = 1, font=("Arial", 20), height=50, width=50)
        B2.place(x=540, y=350, width= 110, height=70)
        
        L2 = tk.Label(self, text="File to download:", font=("Arial Bold", 20), bg='ivory')
        L2.place(x=40, y=540)
        T2 = tk.Entry(self, width=30, font=("Arial Bold", 20))
        T2.place(x=290, y=540, width=490, height=40)

        def download_filename():
            if NOTES == []:
                messagebox.showinfo("Error", "There is no note file currently on the server!")
            elif T2.get() in [row[0] for row in NOTES]:
                download_message = Client().send_action_message(Message(action="download", filename=T2.get()).to_json())
                messagebox.showinfo("Success", download_message["message"])
            else:
                messagebox.showinfo("Error", "The requested filename does not exist. Please, enter" 
                                             "an existing filename without the .code extension!")

        B4 = tk.Button(self, text="Download", font=("Arial", 16), command=download_filename)
        B4.place(x=800, y=540)

        def delete_user():
            global USER
            USER = ""
        
        B5 = tk.Button(self, text="Logout", font=("Arial", 20), 
                       command=lambda: [controller.show_frame(LoginPage), delete_user()])
        B5.place(x=720, y=680)
        
        B6 = tk.Button(self, text="Back", font=("Arial", 20), 
                       command=lambda: controller.show_frame(UploadDownloadPage))
        B6.place(x=140, y=680)
        
        
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        window = tk.Frame(self)
        window.pack()
        window.grid_columnconfigure(0, minsize = 960)
        window.grid_rowconfigure(0, minsize = 780)
        
        self.frames = {}
        for F in (LoginPage, UploadDownloadPage, UploadPage, DownloadPage):
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
    app.maxsize(1000,800)
    app.mainloop()
