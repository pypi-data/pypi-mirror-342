"""
**What Users Can Do**:
1. **Use for Personal and Non-Commercial Purposes:**  
   Users can download and use the Software for personal projects, non-commercial projects, or educational purposes, as long as it's not for profit or commercial gain.

2. **Incorporate into Larger Projects:**  
   Users can include the Software in larger projects, either public or private, but **with proper attribution** (e.g., crediting the original author, "ByteLightDev").

3. **Modify for Personal Use:**  
   Users can modify the Software for their own use within a larger project, as long as any modifications are clearly documented (e.g., note which parts were changed).

4. **Publicly Distribute:**  
   Users can distribute their projects that use the Software publicly, but **U must provide proper attribution** to the original author and include the required notice ("This project includes software developed by [ByteLightDev], © 2025...").

---

**What Users Can't Do:**
1. **Commercial Use Without Permission:**  
   Users cannot use the Software for commercial purposes (e.g., selling it, using it in a product sold for profit) without any **consent** from the Licensor.

2. **Resell or Sublicense the Software:**  
   Users cannot sell, lease, or sublicense the Software as a standalone product. The Software cannot be distributed as-is for a fee or bundled with another product for resale.

3. **Alter or Copy the Original Software (or parts of it) Without Permission:**  
   Users cannot modify the core form of the Software and then redistribute it as part of their project, unless U clearly state any changes made. Copying portions of the Software for redistribution or use in other projects **without the necessary modifications** is prohibited.

4. **Failing to Give Proper Attribution:**  
   If a user integrates the Software into any project that is shared or published, U must ensure the correct **attribution** notice is visible and readable, as specified in the agreement.

---

**How U Can Use the Software:**
**1. Permission for Commercial Use or Profit**  
If you want to use the Software for **commercial purposes** (e.g., selling a product that includes it or using it in a business), you **must get permission** from the Licensor.  

Alternatively, you can use the Software commercially **without prior permission** if you **credit "ByteLightDev" properly** by:  
- Displaying the **ByteLightDev logo** in your commercial content.  
- Ensuring the logo appears **clearly** in the video for **at least 3 seconds** in **HD quality** and is **easily visible** (not hidden or covered).  

© 2025 [ByteLightDev]
"""




from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import logging
import socket
import http
import json
import io
import shutil
import subprocess
import os
import time
import random
import uuid
import inspect
import smtplib
from email.message import EmailMessage
import threading
import sys
import requests
import datetime
import re
import pyperclip
import tkinter as tk
import numpy as np
import sounddevice as sd
import string
import hashlib
import ast
import heapq
from functools import lru_cache
from collections import defaultdict
from difflib import get_close_matches
import platform
import ctypes
from urllib.request import urlopen
from base64 import b64encode



def Easterbun():
    if check_internet_connection():
        def get_easter_date(year):
            a = year % 19
            b = year // 100
            c = year % 100
            d = b // 4
            e = b % 4
            f = (b + 8) // 25
            g = (b - f + 1) // 3
            h = (19 * a + b - d - g + 15) % 30
            i = c // 4
            k = c % 4
            l = (32 + 2 * e + 2 * i - h - k) % 7
            m = (a + 11 * h + 22 * l) // 451
            month = (h + l - 7 * m + 114) // 31
            day = ((h + l - 7 * m + 114) % 31) + 1
            return datetime.date(year, month, day)
        today = datetime.date.today()
        easter = get_easter_date(today.year)
        if today == easter:
            def get_screen_size():
                temp = tk.Tk()
                temp.withdraw()
                w, h = temp.winfo_screenwidth(), temp.winfo_screenheight()
                temp.destroy()
                return w, h
            screen_width, screen_height = get_screen_size()
            url = "https://raw.githubusercontent.com/GoodByeSyntax/GBSassets/main/Easter.png"
            with urlopen(url) as response:
                image_data = response.read()
            b64_data = b64encode(image_data)
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry(f"{screen_width}x{screen_height}+0+0")
            root.configure(bg='black')
            root.bind("<Escape>", lambda e: root.destroy())
            photo = tk.PhotoImage(data=b64_data)
            label = tk.Label(root, image=photo, bg='black')
            label.place(relx=0.5, rely=0.5, anchor='center')
            root.mainloop()
        else:print("Today is not Easter 🐰")
    else:print("No internet no bun!")
def Halloween():
    if check_internet_connection():
        today = datetime.date.today()
        if today.month == 10 and today.day == 31:
            def get_screen_size():
                temp = tk.Tk()
                temp.withdraw()
                w, h = temp.winfo_screenwidth(), temp.winfo_screenheight()
                temp.destroy()
                return w, h
            screen_width, screen_height = get_screen_size()
            url = "https://raw.githubusercontent.com/GoodByeSyntax/GBSassets/main/Halloween.png"
            with urlopen(url) as response:
                image_data = response.read()
            b64_data = b64encode(image_data)
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry(f"{screen_width}x{screen_height}+0+0")
            root.configure(bg='black')
            root.bind("<Escape>", lambda e: root.destroy())
            photo = tk.PhotoImage(data=b64_data)
            label = tk.Label(root, image=photo, bg='black')
            label.place(relx=0.5, rely=0.5, anchor='center')
            root.mainloop()
        else:print("It's not Halloween yet 🎃")
    else:print("No internet, no pumpkin! 👻")
def Valentine():
    if check_internet_connection():
        today = datetime.date.today()
        if today.month == 2 and today.day == 14:
            def get_screen_size():
                temp = tk.Tk()
                temp.withdraw()
                w, h = temp.winfo_screenwidth(), temp.winfo_screenheight()
                temp.destroy()
                return w, h
            screen_width, screen_height = get_screen_size()
            url = "https://raw.githubusercontent.com/GoodByeSyntax/GBSassets/main/Valentines%20Day.png"
            with urlopen(url) as response:
                image_data = response.read()
            b64_data = b64encode(image_data)
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry(f"{screen_width}x{screen_height}+0+0")
            root.configure(bg='black')
            root.bind("<Escape>", lambda e: root.destroy())
            photo = tk.PhotoImage(data=b64_data)
            label = tk.Label(root, image=photo, bg='black')
            label.place(relx=0.5, rely=0.5, anchor='center')
            root.mainloop()
        else: print("It's not Valentine's Day yet 💘")
    else:print("No internet, no love! 💔")
def Christmas():
    if check_internet_connection():
        today = datetime.date.today()
        if today.month == 12 and today.day == 25:
            def get_screen_size():
                temp = tk.Tk()
                temp.withdraw()
                w, h = temp.winfo_screenwidth(), temp.winfo_screenheight()
                temp.destroy()
                return w, h
            screen_width, screen_height = get_screen_size()
            url = "https://raw.githubusercontent.com/GoodByeSyntax/GBSassets/main/Christmas.png"
            with urlopen(url) as response:image_data = response.read()
            b64_data = b64encode(image_data)
            root = tk.Tk()
            root.overrideredirect(True)
            root.geometry(f"{screen_width}x{screen_height}+0+0")
            root.configure(bg='black')
            root.bind("<Escape>", lambda e: root.destroy())
            photo = tk.PhotoImage(data=b64_data)
            label = tk.Label(root, image=photo, bg='black')
            label.place(relx=0.5, rely=0.5, anchor='center')
            root.mainloop()
        else:print("It's not Christmas yet 🎅")
    else:print("No internet, no ho-ho-ho! ❄️")

def wait(key="s", num=1):
    if key.lower() == "s":
        time.sleep(num)
    elif key.lower() == "m":
        time.sleep(num * 60)
    elif key.lower() == "h":
        time.sleep(num * 3600)
    else:
        print("Error: Use 's' for seconds, 'm' for minutes, or 'h' for hours.")

def ifnull(value, default):
    return default if value is None or value == "" else value

def switch_case(key, cases, default=None):
    result = cases.get(key, default)
    return result() if callable(result) else result

def timer_function(func, seconds):
    time.sleep(seconds)
    func()

def iftrue(var, function):
    if var:
        function()

def iffalse(var, function):
    if not var:
        function()
        
def isequal(text,atext):
    if text.lower() == atext:return True
    else:return False

def until(function, whattodo):
    function()
    while True:
        whattodo()
        if function():break

def repeat(function, times):
    for _ in range(times):
        function()

def oncondit(condition, function_true, function_false):
    if condition:
        function_true()
    else:
        function_false()

def repeat_forever(function):
    while True:
        function()

def safe_run(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(f"Error occurred in function {func.__name__}: {e}")
        return None

def start_timer(seconds, callback):
    time.sleep(seconds)
    callback()

def generate_random_string(length=15):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@/-*_'
    return ''.join(random.choices(characters, k=length))

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

def send_email(subject, body, to_email, mailname, mailpass):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = mailname
    msg["To"] = to_email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(mailname, mailpass)
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def generate_unique_id():
    return str(uuid.uuid4())

def start_background_task(backtask):
    thread = threading.Thread(target=backtask)
    thread.start()

def nocrash(func):
    def wrapper(*args, **kwargs):
        return safe_run(func, *args, **kwargs)
    return wrapper

def parallel(*functions):
    threads = []
    for func in functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def gs(func):
    return inspect.getsource(func)

def Jctb(input_string):
    def char_to_binary(c):
        if c == ' ':
            return '0000000001'
        elif c == '\n':
            return '0000000010'
        alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        if c in alphabet_upper:
            return format(alphabet_upper.index(c), '010b')
        elif c in alphabet_lower:
            return format(alphabet_lower.index(c) + 26, '010b')
        return None

    binary_string = ''.join(char_to_binary(char) for char in input_string if char_to_binary(char))
    return binary_string


def Jbtc(binary_input):
    def binary_to_char(binary_vector):
        if binary_vector == '0000000001':
            return ' '
        elif binary_vector == '0000000010':
            return '\n'
        alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        num = int(binary_vector, 2)
        if 0 <= num <= 25:
            return alphabet_upper[num]
        elif 26 <= num <= 51:
            return alphabet_lower[num - 26]
        return None

    char_list = [binary_to_char(binary_input[i:i+10]) for i in range(0, len(binary_input), 10)]
    return ''.join(char_list)

class Jwin:
    def __init__(self, layout, widgets_config, user_callbacks=None):
        self.root = tk.Tk()
        self.root.title("Dynamic Window")
        self.widgets = {}
        self.user_callbacks = user_callbacks or {}
        self.layout_lines = [line.strip() for line in layout.strip().split("\n") if line.strip()]
        self.num_rows = len(self.layout_lines)
        self.num_cols = max(len(line) for line in self.layout_lines)
        for r in range(self.num_rows):
            self.root.grid_rowconfigure(r, weight=1)
        for c in range(self.num_cols):
            self.root.grid_columnconfigure(c, weight=1)
        self._create_widgets(widgets_config)
        self._create_layout()

    def _create_widgets(self, widgets_config):
        for widget_config in widgets_config:
            row, col = widget_config['position']
            widget_type = widget_config['type']
            options = widget_config.get('options', {})
            widget = self._create_widget(widget_type, options)
            if widget:
                widget.grid(row=row, column=col, padx=5, pady=5)
                widget_id = options.get("id")
                if widget_id:
                    self.widgets[widget_id] = widget

    def _create_widget(self, widget_type, options):
        if widget_type == "button":
            return tk.Button(self.root, text=options.get("text", "Button"),
                             command=lambda: self._execute_callback(options.get("id")))
        elif widget_type == "label":
            return tk.Label(self.root, text=options.get("text", "Label"))
        elif widget_type == "input":
            return tk.Entry(self.root)
        elif widget_type == "password":
            return tk.Entry(self.root, show="*")
        elif widget_type == "checkbox":
            return tk.Checkbutton(self.root, text=options.get("text", "Checkbox"))
        elif widget_type == "textarea":
            return tk.Text(self.root, height=5, width=20)
        else:
            return tk.Label(self.root, text=f"Unsupported: {widget_type}")

    def _create_layout(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.layout_lines[r][c] == " ":
                    continue

    def _execute_callback(self, widget_id):
        if widget_id and widget_id in self.user_callbacks:
            callback = self.user_callbacks[widget_id]
            if callable(callback):
                callback()

    def run(self):
        self.root.mainloop()


    def show_error_messagebox(message):
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("Error", message)

def encode_base64(data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    binary_data = ''.join([f"{ord(c):08b}" for c in data])
    padding = len(binary_data) % 6
    if padding != 0:
        binary_data += '0' * (6 - padding)
    encoded = ''.join([base64_chars[int(binary_data[i:i+6], 2)] for i in range(0, len(binary_data), 6)])
    encoded += "=" * ((4 - len(encoded) % 4) % 4)
    return encoded

def decode_base64(encoded_data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encoded_data = encoded_data.rstrip("=")
    binary_data = ''.join([f"{base64_chars.index(c):06b}" for c in encoded_data])
    decoded = ''.join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])
    return decoded

def reverse_string(string):
    return string[::-1]

def calculate_factorial(number):
    if number == 0:
        return 1
    return number * calculate_factorial(number - 1)

def generate_random_string(length=15):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@/-*_'
    random_string = ''
    for _ in range(length):
        random_string += charset[calculate_factorial(len(charset)) % len(charset)]
    return random_string

def swap_values(a, b):
    return b, a

def replace(string,replacement,replacment):return string.replace(replacement,replacment)

def find_maximum(numbers):
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def find_minimum(numbers):
    min_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val

def sum_list(lst):
    total = 0
    for num in lst:
        total += num
    return total

def reverse_list(lst):
    return lst[::-1]

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def split_into_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def unique_elements(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum_list(numbers) / len(numbers)

def calculate_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    return sorted_numbers[mid]

def count_words(text):
    return len(text.split())

def count_sentences(text):
    sentences = text.split('.')
    return len([s for s in sentences if s.strip()])

def add_commas(input_string):
    return ','.join(input_string)

def remove_spaces(text):
    return ''.join([char for char in text if char != ' '])

def calculate_square_root(number):
    if number < 0:
        return None
    guess = number / 2.0
    for _ in range(20):
        guess = (guess + number / guess) / 2.0
    return guess

def find_files_by_extension(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def get_curr_dir():
    return os.getcwd()

def check_if_file_exists(file_path):
    return os.path.exists(file_path)

def monitor_new_files(directory, callback):
    known_files = set(os.listdir(directory))
    while True:
        current_files = set(os.listdir(directory))
        new_files = current_files - known_files
        if new_files:
            callback(new_files)
        known_files = current_files
        time.sleep(1)


def monitor_file_changes(file_path, callback):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            last_modified = current_modified
            callback()
        time.sleep(1)

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def parse_json(json_string):
    return json.loads(json_string)

def create_file_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('')

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_zip_file(source_dir, output_zip):
    shutil.make_archive(output_zip, 'zip', source_dir)

def extract_zip_file(zip_file, extract_dir):
    shutil.unpack_archive(zip_file, extract_dir)

def move_file(source, destination):
    shutil.move(source, destination)

def copy_file(source, destination):
    shutil.copy(source, destination)

def show_file_properties(file_path):
    stats = os.stat(file_path)
    return f"Size: {stats.st_size} bytes, Last Modified: {time.ctime(stats.st_mtime)}"


def start_http_server(ip="0.0.0.0", port=8000):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server started on {ip}:{port}")
    httpd.serve_forever()

def stop_http_server():
    print("Stopping server...")
    exit(0)

def get_server_status(url="http://localhost:8000"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Server is up and running.")
        else:
            print(f"Server is down. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")

def set_server_timeout(timeout=10):
    socket.setdefaulttimeout(timeout)
    print(f"Server connection timeout set to {timeout} seconds.")

def upload_file_to_server(file_path, url="http://localhost:8000/upload"):
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
        if response.status_code == 200:
            print(f"File successfully uploaded: {file_path}")
        else:
            print(f"File upload failed. Status Code: {response.status_code}")

def download_file_from_server(file_url, save_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded: {save_path}")
    else:
        print(f"File download failed. Status Code: {response.status_code}")

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Welcome! Server is running.")
        elif self.path == "/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "online"}')
        else:
            self.send_response(404)
            self.end_headers()

def start_custom_http_server(ip="0.0.0.0", port=8000):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Custom server started on {ip}:{port}")
    httpd.serve_forever()

def set_server_access_logs(log_file="server_access.log"):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    print(f"Access logs are being saved to {log_file}")

def get_server_logs(log_file="server_access.log"):
    try:
        with open(log_file, 'r') as log:
            logs = log.readlines()
            print("".join(logs))
    except FileNotFoundError:
        print(f"{log_file} not found.")

def restart_http_server():
    print("Restarting server...")
    os.execv(sys.executable, ['python'] + sys.argv)

def check_internet_connection():
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        subprocess.run(["ping", param, "1", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def create_web_server(directory, port=8000):
    os.chdir(directory)
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving {directory} at http://localhost:{port}")
        httpd.serve_forever()

def create_custom_web_server(html, port=8000):
    html_content = html

    class CustomHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Serving custom HTML page at http://0.0.0.0:{port}")
        print("Anyone on the same network can access this. (if not work use this http://127.0.0.1:8000)")
        httpd.serve_forever()
def JynParser(rep):
    inj= """
    global main
    main = rep
    """
    exec()

def contains(input, str):
    return str in input

def Jusbcam(Device_Name):
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_PnPEntity', 'where', 'DeviceID like "USB%"', 'get', 'Name'],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        if result.stdout:
            output = result.stdout.strip().split("\n")[1:]
            devices = [line.strip() for line in output if line.strip()]
            return contains(devices,Device_Name)
        else:
            return []
    except Exception as e:
        print(f"Error detecting devices: {e}")
        return []

def defseprator(option_count, *options):
    if len(options) != option_count:
        raise ValueError(f"Expected {option_count} options, but got {len(options)}.")
    result = [1 if option else 0 for option in options]
    return ",".join(map(str, result))


def claw(html_option, html, ip, port, subdomain_option, subdomain_count, subdomains, return_server_logs_option):
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        MAIN_HTML = "<h1>Default Page</h1>"
        SUBDOMAINS = {}
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.MAIN_HTML.encode("utf-8"))
            elif self.path in self.SUBDOMAINS:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.SUBDOMAINS[self.path].encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")
            if self.server.log_requests:logging.info(f"Request: {self.command} {self.path} from {self.client_address}")
    if return_server_logs_option:logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    if html_option:CustomHandler.MAIN_HTML = html
    if subdomain_option:
        for i in range(1, subdomain_count + 1):
            sub_path = f"/sub{i}"
            CustomHandler.SUBDOMAINS[sub_path] = subdomains.get(sub_path, f"<h1>Subdomain {i}</h1>")
    server = socketserver.TCPServer((ip, port), CustomHandler)
    server.log_requests = return_server_logs_option
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"Server started at http://{ip}:{port}")
    return server

class ConsoleCam:
    def __init__(self):
        self._original_stdout = sys.stdout
        self._buffer = io.StringIO()
        sys.stdout = self._buffer
    @classmethod
    def start(cls):
        instance = cls()
        instance._buffer.truncate(0)
        instance._buffer.seek(0)
        return instance
    def get_new(self):return self._buffer.getvalue()
    def stop(self):sys.stdout = self._original_stdout

def prn(str):print(str)

def copy_to_clipboard(text):
    pyperclip.copy(text)

class Key:
    def __init__(self, key):
        VK_CODE = {
            **{chr(i): i - 32 for i in range(ord('a'), ord('z') + 1)},
            **{str(i): 0x30 + i for i in range(10)},
            **{f'f{i}': 0x6F + i for i in range(1, 13)},
            'left': 0x25, 'up': 0x26, 'right': 0x27, 'down': 0x28,
            'home': 0x24, 'end': 0x23, 'insert': 0x2D, 'delete': 0x2E,
            'pageup': 0x21, 'pagedown': 0x22,
            'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
            'tab': 0x09, 'capslock': 0x14, 'enter': 0x0D,
            'space': 0x20, 'backspace': 0x08, 'esc': 0x1B,
            ';': 0xBA, '=': 0xBB, ',': 0xBC, '-': 0xBD,
            '.': 0xBE, '/': 0xBF, '`': 0xC0,
            '[': 0xDB, '\\': 0xDC, ']': 0xDD, "'": 0xDE,
            'num0': 0x60, 'num1': 0x61, 'num2': 0x62, 'num3': 0x63,
            'num4': 0x64, 'num5': 0x65, 'num6': 0x66,
            'num7': 0x67, 'num8': 0x68, 'num9': 0x69,
            'multiply': 0x6A, 'add': 0x6B, 'separator': 0x6C,
            'subtract': 0x6D, 'decimal': 0x6E, 'divide': 0x6F,
        }
        self.key = key.lower()
        self.vk = VK_CODE.get(self.key)

    def press(self):
        if self.vk is not None:
            ctypes.windll.user32.keybd_event(self.vk, 0, 0, 0)

    def release(self):
        KEYEVENTF_KEYUP = 0x0002
        if self.vk is not None:
            ctypes.windll.user32.keybd_event(self.vk, 0, KEYEVENTF_KEYUP, 0)

    def tap(self, delay=0.05):
        self.press()
        time.sleep(delay)
        self.release()
    
    def type_text(text):
        def press_combo(*keys, delay=0.05):
            key_objs = [Key(k) for k in keys]
            for k in key_objs:
                k.press()
                time.sleep(delay)
            for k in reversed(key_objs):
                k.release()
                time.sleep(delay)
        for char in text:
            if char.isupper():
                press_combo('shift', char.lower())
            else:
                Key(char).tap()

    def press_combo(*keys, delay=0.05):
        key_objs = [Key(k) for k in keys]
        for k in key_objs:
            k.press()
            time.sleep(delay)
        for k in reversed(key_objs):
            k.release()
            time.sleep(delay)

def count_occurrences(lst, element):return lst.count(element)

def get_curr_time():now = datetime.datetime.now();return now.strftime("%Y-%m-%d %H:%M:%S")

def is_palindrome(s):return s == s[::-1]

def get_min_max(list):return min(list),max(list)

def is_digits(input):return input.isdigit()

def create_dict(keys, values):return dict(zip(keys, values))

def square_number(input):return input ** 2

def get_file_size(file_path):return os.path.getsize(file_path)

def find_duplicates(lst):
    seen = set()
    duplicates = []
    for item in lst:
        if item in seen:duplicates.append(item)
        else:seen.add(item)
    return duplicates

def get_average(list):
    if not list:return 0
    return sum(list) / len(list)

def divide(a, b):
    if b == 0:return None
    return a / b

def extract_numbers(s):return [int(x) for x in re.findall(r'\d+', s)]

class BinTrig:
    @classmethod
    def exit(cls, winroot, trig):
        def close_and_destroy():
            trig()
            winroot.destroy()
        winroot.protocol("WM_DELETE_WINDOW", close_and_destroy)

    def mouse_in(self, winroot, trig):
        winroot.bind("<Enter>", trig)

    def mouse_out(self, winroot, trig):
        winroot.bind("<Leave>", trig)

    def fullscreen(self, winroot, trig):
        def check_fullscreen(event=None):
            screen_width = winroot.winfo_screenwidth()
            screen_height = winroot.winfo_screenheight()
            window_width = winroot.winfo_width()
            window_height = winroot.winfo_height()
            if window_width == screen_width and window_height == screen_height:
                trig(event)
        winroot.bind("<Configure>", check_fullscreen)

    def minimized(self, winroot, trig):
        def check_minimized(event=None):
            if winroot.state() in ['iconic', 'withdrawn']:
                trig(event)
        winroot.bind("<Visibility>", check_minimized)

    def width_height(self, winroot, widmin, heimin, trig):
        def check_size(event=None):
            width = winroot.winfo_width()
            height = winroot.winfo_height()
            if width > widmin or height > heimin:
                trig(event)
        winroot.bind("<Configure>", check_size)

    def key_press(self, winroot, key, trig):
        winroot.bind(f"<KeyPress-{key}>", trig)

    def focus_gain(self, winroot, trig):
        winroot.bind("<FocusIn>", trig)

    def focus_loss(self, winroot, trig):
        winroot.bind("<FocusOut>", trig)

    def window_move(self, winroot, trig):
        winroot.bind("<Configure>", trig)

    def resize(self, winroot, trig):
        winroot.bind("<Configure>", trig)

    def close_shortcut(self, winroot, trig):
        winroot.bind("<Alt-F4>", trig)

    def mouse_button_press(self, winroot, button, trig):
        winroot.bind(f"<Button-{button}>", trig)

    def mouse_button_release(self, winroot, button, trig):
        winroot.bind(f"<ButtonRelease-{button}>", trig)

    def double_click(self, winroot, trig):
        winroot.bind("<Double-1>", trig)

    def mouse_motion(self, winroot, trig):
        winroot.bind("<Motion>", trig)

    def window_minimized(self, winroot, trig):
        def check_minimized(event=None):
            if winroot.state() == 'iconic':
                trig(event)
        winroot.bind("<Unmap>", check_minimized)

    def window_maximized(self, winroot, trig):
        def check_maximized(event=None):
            winroot.update_idletasks()
            if winroot.state() == 'zoomed':
                trig(event)
        winroot.bind("<Map>", check_maximized)
        winroot.bind("<Configure>", check_maximized)

    def window_restored(self, winroot, trig):
        def check_restored(event=None):
            if winroot.state() == 'normal':
                trig(event)
        winroot.bind("<Configure>", check_restored)

    def mouse_wheel_scroll(self, winroot, trig):
        winroot.bind("<MouseWheel>", trig)

    def text_change(self, widget, trig):
        widget.bind("<KeyRelease>", trig)

    def focus_on_widget(self, widget, trig):
        widget.bind("<FocusIn>", trig)

    def focus_off_widget(self, widget, trig):
        widget.bind("<FocusOut>", trig)

class ByteJar:
    def __init__(self, host="127.0.0.1", port=8090):
        self.host = host
        self.port = port
        self.client_socket = None

    def start(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            response = self.client_socket.recv(1024).decode().strip()
            print(f"DEBUG: Server response: {response}")  
            return response
        except Exception as e:
            return f"Error connecting to server: {e}"

    def stop(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            return "Connection closed."
        return "No active connection."

    def send_command(self, command):
        if not self.client_socket:
            return "Error: No active connection. Please start the connection first."

        try:
            self.client_socket.sendall(command.encode())
            response = self.client_socket.recv(1024).decode().strip()
            print(f"DEBUG: Server response: {response}")  
            return response
        except Exception as e:
            return f"Error while sending command: {e}"

def letterglue(str="", *substr, str2=""):return str + ''.join(substr) + str2

def letterglue_creator(word):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    original_vars = [(alphabet[i % 26] * ((i // 26) + 1), letter) for i, letter in enumerate(word)]
    shuffled_vars = original_vars[:]
    random.shuffle(shuffled_vars)
    defs_line = "; ".join([f'{var}="{ch}"' for var, ch in shuffled_vars]) + ";"
    glue_order = ", ".join([var for var, _ in original_vars])
    code = defs_line + "\n"
    code += "result = letterglue(" + glue_order + ")\n"
    code += "print(result)"
    return code

def Baudio(filename="audio_data", mode="Write", duration=5, Warn=True):
    def BprecAU(fname, Warn=Warn):
        if Warn:
            print("Playing audio...")
        samplerate = 44100
        with open(letterglue(fname, ".Bau"), 'rb') as f:
            audio_data = f.read()
        audio_data_np = np.frombuffer(audio_data, dtype='float32')
        sd.play(audio_data_np, samplerate=samplerate)
        sd.wait()
        if Warn:
            print(f"Audio playback from {fname}.Bau finished.")

    host = "127.0.0.1"
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    client_socket.sendall("record".encode())
    client_socket.sendall(duration.to_bytes(4, 'big'))
    
    audio_length = int.from_bytes(client_socket.recv(4), 'big')
    audio_data = b""
    while len(audio_data) < audio_length:
        audio_data += client_socket.recv(1024)
    
    client_socket.close()
    
    if mode.lower() == "write":
        with open(letterglue(filename, ".Bau"), 'wb') as f:
            f.write(audio_data)
        if Warn:
            print(f"Audio recorded and saved to {filename}.Bau.")
            
    elif mode.lower() == "return":
        audio_np = np.frombuffer(audio_data, dtype='float32')
        if Warn:
            print("Audio recorded and returned as a numpy array.")
        return audio_np
    elif mode.lower() == "play":
        BprecAU(filename)
    else:
        raise ValueError("Invalid mode. Please use 'Write', 'Return' or 'Play'.")

class Btuple:
    @classmethod
    def count(cls, *words):
        return len(words)
    @classmethod
    def get(cls, index, *words):
        if 0 <= index < len(words):
            return words[index-1]
        return "Error: Please choose a number within range."
    @classmethod
    def exists(cls, item, *words):
        return item in words

    @classmethod
    def first(cls, *words):
        return words[0] if words else "Error: Tuple is empty."

    @classmethod
    def last(cls, *words):
        return words[-1] if words else "Error: Tuple is empty."

def isgreater(*nums):
    tc = Btuple.count(*nums)
    t1 = Btuple.get(*nums, 1)
    t2 = Btuple.get(*nums, 2)
    if tc != 2:
        print("There should be 2 numbers inputted!")
        return False
    elif tc == 0:
        print("Input can't be empty!")
        return False
    elif t1 > t2:return True
    else:return False

def runwfallback(func, fallback_func):
    try:return func()
    except Exception as e:return fallback_func()

def retry(func, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print("All attempts failed.")
    return None

def fftime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

def paste_from_clipboard():return pyperclip.paste()

def watch_file(filepath, callback):
    last_modified = os.path.getmtime(filepath)
    while True:
        time.sleep(1)
        if os.path.getmtime(filepath) != last_modified:
            last_modified = os.path.getmtime(filepath)
            callback(filepath)

def is_website_online(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:return False

def shorten_url(long_url):
    response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
    return response.text

def celsius_to_fahrenheit(c):return (c * 9/5) + 32

def fahrenheit_to_celsius(f):return (f - 32) * 5/9

def efv(code: str):
    fc = code.replace(",", ";")
    local_vars = {}
    exec(fc, {}, local_vars)
    return local_vars

def Hpass(limit=30):
    def e(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    def d(word1, word2):
        current_time = str(int(time.time()))
        mixed = ''.join(random.sample(word1 + word2 + current_time, len(word1 + word2 + current_time)))
        return mixed
    def c(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    def a(hash_value):
        result = []
        for char in hash_value:
            byte_val = (ord(char) * 10) % 256
            result.append(chr(byte_val))
        return ''.join(result)
    lc=limit
    def b(word1, word2):
        mixed1 = d(word1, word2)
        hashed1 = c(mixed1)
        jcbt1 = a(hashed1)
        mixed2 = d(word1, word2 + jcbt1)
        hashed2 = c(mixed2)
        final_jcbt = a(hashed2)
        return final_jcbt
    def o(word1, word2):
        result1 = b(word1, word2)
        result2 = b(word1, word2)
        current_time = str(int(time.time()))
        final_result = result1 + result2 + current_time
        return final_result
    def c2n(input_string):
        result = []
        for char in input_string:result.append(str(ord(char)))
        return ''.join(result)
    def n2c(number):
        number_str = str(number)
        result = []
        for digit in number_str:
            char = chr(96 + int(digit))
            if random.choice([True, False]):char = char.upper()
            result.append(char)
        return ''.join(result)
    def ltc(imp,cc):return imp[:cc]
    word1 = e();word2 = e()
    N="w"; P="r"; H="o"; C="="; D=" "; F="("; A="o"; R="2"; L=","; K="1"; E="o"; Q="d"; M=" "; B="o"; S=")"; O="o"; I="r"; J="d"; G="w"
    result = letterglue(A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S)
    context = {'word1': word1, 'word2': word2, 'o': o}
    exec(result, globals(), context)
    crs=c2n(context.get("oo"))
    nms=n2c(crs)
    return ltc(replace(nms,"`",""),lc)

def l(input):return list(input)

def dl(input):return ''.join(input)

def mix(input):shuffled = l(input);random.shuffle(shuffled);return dl(shuffled)

def sugar(input):
    rn = random.randint(1, len(input))
    random_number_string = ''.join(random.choices("01243213132112576635439769813224562133489", k=5))
    length = len(input) - 1
    a = list(add_commas(input))
    random.shuffle(a)
    b = generate_random_string(length)
    c = letterglue(''.join(a), b)
    c_list = list(c)
    random.shuffle(c_list)
    c_shuffled = ''.join(c_list)
    d = c_shuffled.replace(",", "")
    d_list = list(d)
    random.shuffle(d_list)
    d_shuffled = ''.join(d_list)
    rn_str = add_commas(str(rn))
    rn_list = list(rn_str)
    random.shuffle(rn_list)
    rn_shuffled = ''.join(rn_list)
    combined = letterglue(random_number_string, rn_shuffled + d_shuffled)
    combined_list = list(combined)
    random.shuffle(combined_list)
    f1 = ''.join(combined_list)
    return replace(mix(f1), ",", "")

def get_type(value):return f"{type(value).__name__} - {repr(value)}"

class Cache:
    def __init__(self):self.cached = {}
    def add(self, key, value):self.cached[key] = value
    def get(self, key):return self.cached.get(key, None)


def cantint(egl="Equal,Greater,Lower", ftw="From/To What", tw="Tuple of ints"):
    if egl == "e":
        if ftw in tw:tw.clear()
    elif egl == "g":
        if any(ftw > item for item in tw):tw.clear()
    elif egl == "l":
        if any(ftw < item for item in tw):tw.clear()
    else:return

def flatten(obj):
    if isinstance(obj, list):
        for item in obj:
            yield from flatten(item)
    else:
        yield obj

def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def chunk(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result

def deep_equal(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return False
        return all(deep_equal(a[k], b[k]) for k in a)
    elif isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(deep_equal(i, j) for i, j in zip(a, b))
    return a == b

def split_by(text, size):
    return [text[i:i + size] for i in range(0, len(text), size)]

class GoodBye2Spy:
    class Passworded:
        @classmethod
        def create(cls, data, key, seed=42):
            def distribute_key_into_string(data, key, seed=42):
                data_list = list(data)
                key_index = 0
                random.seed(seed)
                for i in range(len(data_list)):
                    if random.choice([True, False]):
                        data_list[i] = key[key_index % len(key)]
                        key_index += 1
                mixed_data = ''.join(data_list)
                return mixed_data
            mixed_data = distribute_key_into_string(data, key, seed)
            hashed_value = hashlib.sha256(mixed_data.encode()).hexdigest()
            return hashed_value
        
        @classmethod
        def verify(cls, data, key, given_hash, seed=42):
            generated_hash = cls.create(data, key, seed)
            return generated_hash == given_hash

    class Shifting:
        @classmethod
        def SBH(cls, data):
            hash_value = 0
            data = data.encode()
            for byte in data:
                hash_value ^= byte
                hash_value = (hash_value << 30) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            sugar(str(hash_value))
            return hash_value
    
    class Oneway:
        @classmethod
        def OW(cls, data="Input a string", strength=5):
            class Passworded:
                @classmethod
                def create(cls, data, key, seed=42):
                    def distribute_key_into_string(data, key, seed=42):
                        data_list = list(data)
                        key_index = 0
                        random.seed(seed)
                        for i in range(len(data_list)):
                            if random.choice([True, False]):
                                data_list[i] = key[key_index % len(key)]
                                key_index += 1
                        mixed_data = ''.join(data_list)
                        return mixed_data
                    mixed_data = distribute_key_into_string(data, key, seed)
                    hashed_value = hashlib.sha256(mixed_data.encode()).hexdigest()
                    return hashed_value
                
                @classmethod
                def verify(cls, data, key, given_hash, seed=42):
                    generated_hash = cls.create(data, key, seed)
                    return generated_hash == given_hash

            class Shifting:
                @classmethod
                def SBH(cls, data):
                    hash_value = 0
                    data = data.encode()
                    for byte in data:
                        hash_value ^= byte
                        hash_value = (hash_value << 30) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                    sugar(str(hash_value))
                    return hash_value
            key = generate_random_string(strength+15)
            return Shifting.SBH(Passworded.create(data, key))

def slc(code: str) -> str:
    try:
        tree = ast.parse(code)
        return ";".join(c.strip() for c in code.splitlines() if c.strip())
    except SyntaxError:return "Invalid Python code"

class Ai:
    @classmethod
    def GAI(context, questions=None, summarize_text=False, summary_length=3):

        def tokenize(text):
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            return text.split()
        def detect_question_type(question):
            q = question.lower()
            if 'how old' in q:
                return 'age'
            if 'when' in q:
                return 'date'
            if 'where' in q:
                return 'location'
            if 'who' in q:
                return 'person'
            if 'what' in q:
                return 'thing'
            return 'unknown'
        @lru_cache(maxsize=256)
        def cached_answer(question, context):
            return extract_answer(question, context)
        def extract_answer(question, context):
            q_type = detect_question_type(question)
            q_lower = question.lower()
            sentences = re.split(r'(?<=[.?!])\s+', context)
            if q_type == 'age':
                m = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})\b", context)
                if m:
                    day, month, year = m.group(1), m.group(2), int(m.group(3))
                    try:
                        dt = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
                    except ValueError:
                        return 'Answer not found.'
                    today = datetime.today()
                    age = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
                    return str(age)
            for s in sentences:
                s = s.strip().rstrip('.')
                if q_type == 'date':
                    m = re.search(r"\b(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4})\b", s)
                    if m:
                        return m.group(1)
                    m = re.search(r"\b(19|20)\d{2}\b", s)
                    if m:
                        return m.group(0)
                elif q_type == 'location':
                    m = re.search(r"\blived in\s+([A-Z][a-z]+),\s*which\s+is\s+in\s+([A-Z][a-z]+)\b", s)
                    if m:
                        return f"{m.group(1)} is in {m.group(2)}"
                    m = re.search(r"\b(?:in|at|on)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", s)
                    if m:
                        return m.group(1)
                elif q_type == 'person':
                    m = re.search(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", s)
                    if m:
                        return m.group(1)
                elif q_type == 'thing':
                    if 'company' in q_lower or 'work for' in q_lower:
                        m = re.search(r"\b([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*)\s+(Inc\.?|Ltd\.?|Corporation|LLC)\b", s)
                        if m:
                            return f"{m.group(1)} {m.group(2).rstrip('.')}"
                    if 'email' in q_lower:
                        m = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b", s)
                        if m:
                            return m.group(0)
                    if 'phone' in q_lower or 'number' in q_lower:
                        m = re.search(r"\+?\d[\d\-\s\(\)]{7,}\d", s)
                        if m:
                            return m.group(0)
                    if 'event' in q_lower or 'attend' in q_lower:
                        m = re.search(
                            r"\b(?:the\s+)?([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*)\s+"
                            r"(festival|conference|summit|meeting)\b",
                            s,
                            re.IGNORECASE
                        )
                        if m:
                            return f"{m.group(1).title()} {m.group(2).title()}"
                    if 'time' in q_lower:
                        m = re.search(r"\b(morning|afternoon|evening)\b", s, re.IGNORECASE)
                        if m:
                            return m.group(1).lower()
                        m = re.search(r"\b(\d{1,2}\s?(?:AM|PM))\b", s, re.IGNORECASE)
                        if m:
                            return m.group(1)
                    if 'percent' in q_lower or 'score' in q_lower:
                        m = re.search(r"\b\d+%|\d+\s+percent\b", s, re.IGNORECASE)
                        if m:
                            return m.group(0)
                    if 'currency' in q_lower or '$' in s or '€' in s:
                        m = re.search(r"\$\s?\d+(?:\.\d+)?|€\s?\d+", s)
                        if m:
                            return m.group(0)
            cm = get_close_matches(question.lower(), sentences, n=1)
            if cm:
                fallback = cm[0].rstrip('.')
                if q_type == 'thing' and ('event' in q_lower or 'attend' in q_lower):
                    m = re.search(
                        r"\b([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*)\s+"
                        r"(festival|conference|summit|meeting)\b",
                        fallback, re.IGNORECASE
                    )
                    if m:
                        return f"{m.group(1).title()} {m.group(2).title()}"
                return fallback

            return 'Answer not found.'
        def summarize(text, num_sentences=3):
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            if len(sentences) <= num_sentences:
                return text.strip()
            words = tokenize(text)
            stopwords = {
                'the','and','is','in','to','of','a','that','it','on','for','with','as','was','he','she','they','at','by','an'
            }
            freq = defaultdict(int)
            for w in words:
                if w in stopwords:
                    continue
                freq[w] += 1
            scores = {}
            for s in sentences:
                score = 0
                for w in tokenize(s):
                    score += freq.get(w, 0)
                scores[s] = score
            best = heapq.nlargest(num_sentences, scores, key=scores.get)
            summary = [s for s in sentences if s in best]
            return ' '.join(summary)
        if summarize_text:
            return summarize(context, num_sentences=summary_length)
        if questions:
            return [cached_answer(q, context) for q in questions]
        return 'No questions provided.'
    
    
    
    @classmethod
    def GQA(context, question):
        def preprocess(text):
            text = text.lower()
            text = re.sub(r'[^a-z\s.]', '', text)
            return text
        context = preprocess(context)
        question = preprocess(question)
        question_tokens = set(question.split())
        context_tokens = context.split()
        common_tokens = question_tokens.intersection(context_tokens)
        if not common_tokens:
            return "Sorry, I couldn't find an answer."
        sentences = context.split('.')
        sentence_scores = []
        for sentence in sentences:
            sentence_tokens = set(sentence.split())
            common_words_in_sentence = question_tokens.intersection(sentence_tokens)
            score = len(common_words_in_sentence)
            sentence_scores.append((score, sentence))
        sentence_scores.sort(reverse=True, key=lambda x: x[0])
        if sentence_scores:
            best_sentence = sentence_scores[0][1]
            best_sentence = best_sentence.capitalize().strip() + '.'
            return best_sentence
        return "Sorry, I couldn't find an answer."

def requireADMIN():
    if platform.system() != "Windows":
        tk.messagebox.showerror("Unsupported OS", "This script only supports Windows.")
        sys.exit(1)
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if not is_admin():
        tk.messagebox.showerror("Permission required", "Administrator privileges are required to run this program")
        sys.exit(1)

def get_raw_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {e}"
