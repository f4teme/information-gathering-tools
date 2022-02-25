from tkinter import *
import tkinter.filedialog
import tkinter as tk
import socket as s
from tkinter.tix import IMAGE
import sys
import os
import tkinter as tk
from pathlib import Path
from glob import glob
from logging import exception
from textwrap import wrap
from tkinter import *
import requests
import urllib.request
import json
from tkinter.messagebox import showinfo
from bs4 import BeautifulSoup
import threading

#--------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Path to asset files for this GUI master.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# Required in order to add data files to masters executable
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

output_path = ""
def IP2LOCATION(domain):
    GEO_IP_API_URL  = 'http://ip-api.com/json/'
    DOMAIN    = domain 
    req             = urllib.request.Request(GEO_IP_API_URL + DOMAIN)
    response        = urllib.request.urlopen(req).read()
    json_response   = json.loads(response.decode('utf-8'))
    return (json_response)

def FIND_IP(domain):
    """
    Get host name and return Ip address of website
    """
    info = s.getaddrinfo(domain,80) 
    LIST_IP =[]
    for i in info:
        LIST_IP.append(i[4][0])
    return (LIST_IP)
  
PORTS =[]
def PORT_SCANER(port):
    so = s.socket(s.AF_INET, s.SOCK_STREAM)
    s.setdefaulttimeout(0.1)

    res = so.connect_ex((domain,port))
    if res ==0:
        try:
            server_name = s.getservbyport(port,'tcp')
        except:
            server_name = ''
   
        result = {
            'port':port,
            'state':'Open',
            'server name':server_name
        }   
    else:
        try:
            server_name = s.getservbyport(port,'tcp')
        except:
            server_name = ''
        result = {
            'port':port,
            'state':'Close',
            'server name':server_name
            }     
    so.close()
    PORTS.append(result)
    return result

def FIND_DIRECTORY(domain):
    url = f"http://www.{domain}"
    soup = BeautifulSoup(requests.get(url).text,"html.parser")

    hrefs = []
    for a in soup.find_all('a'):
        hrefs.append(a['href'])

    return hrefs

def CHECK_PORT():
    port = int(port_value.get())
    res = PORT_SCANER(port)
    showinfo(
        title='Port Information',
        message=F"Port{res['port']} is {res['state']}")

def select_path():
    global output_path

    output_path = tkinter.filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)

def select_path_SB():
    global output_path_SB

    output_path_SB = tkinter.filedialog.askdirectory()
    path_entry_SB.delete(0, tk.END)
    path_entry_SB.insert(0, output_path_SB)


def Download_directorys():
    path_to_save = path_entry.get()
    completeName = os.path.join(path_to_save, "Directorys.txt")
    Links = FIND_DIRECTORY(domain)
    with open(completeName, 'w') as f:
        for item in Links:
            f.write("%s\n" % item)
    tk.messagebox.showinfo(
        "Success!", f"All Directorys successfully downloaded at {path_to_save}.")

SUB_DOMAINS = []
def FIND_SUBDOMAINS(subdomain):

        s = requests.session()
        url = f'https://{subdomain}.{domain}'
        try:
            s.get(url ,timeout=1.5)
            #print(url)
            SUB_DOMAINS.append(url)
        except:
            pass


def Download_SubDomain():
    path_to_save = path_entry_SB.get()
    completeName= os.path.join(path_to_save, "SubDomains.txt") 
    threads = []
    file = open('Subdomain50.txt','r')
    Subs  = file.read()
    sub_domain = Subs.splitlines()

    for i in sub_domain:
        thread = threading.Thread(target=FIND_SUBDOMAINS ,args=[i])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    with open(completeName, 'w') as f:
        for item in SUB_DOMAINS:
            f.write("%s\n" % item)
    tk.messagebox.showinfo(
        "Success!", f"Subdomains successfully downloaded at {path_to_save}.")

def btn_clicked():
    global domain
    domain = domain_entry.get()
    master.destroy()

    window = Tk()
    window.title("Information Gathering Tool")    
    window.geometry("862x519")
    window.configure(bg = "#e5ecf9")
    #------HEADER GUI---------
    canvas = Canvas(
        window,
        bg = "#e5ecf9",
        height = 519,
        width = 862,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)


    canvas.create_rectangle(
        35, 26, 35+200, 26+45,
        fill = "#6592fe",
        outline = "")


    canvas.create_rectangle(
        235, 26, 235+200, 26+45,
        fill = "#85a9ff",
        outline = "")


    canvas.create_rectangle(
        431, 26, 431+200, 26+45,
        fill = "#6592fe",
        outline = "")


    canvas.create_rectangle(
        631, 26, 631+200, 26+45,
        fill = "#85a9ff",
        outline = "")

    canvas.create_text(
        135.5, 50,
        text = "Domain Name",
        fill = "#FFFFFF",
        font = ("Rasa-Regular", int(18.0)))

    canvas.create_text(
        326.5, 50,
        text = "Country",
        fill = "#FFFFFF",
        font = ("Rasa-Regular", int(18.0)))

    canvas.create_text(
        720, 50,
        text = "ISP",
        fill = "#FFFFFF",
        font = ("Rasa-Regular", int(18.0)))

    canvas.create_text(
        520.5, 50,
        text = "City",
        fill = "#FFFFFF",
        font = ("Rasa-Regular", int(18.0)))


    canvas.create_rectangle(
        35, 71, 35+200, 71+45,
        fill = "#e5e5e5",
        outline = "")


    canvas.create_rectangle(
        235, 71, 235+200, 71+45,
        fill = "#dfdfdf",
        outline = "")


    canvas.create_rectangle(
        431, 71, 431+200, 71+45,
        fill = "#e5e5e5",
        outline = "")


    canvas.create_rectangle(
        631, 71, 631+200, 71+45,
        fill = "#dfdfdf",
        outline = "")
#------------Call IP2LOCATION-----------

    location = IP2LOCATION(domain)

    #DOMAIN_NAME TEXT
    canvas.create_text(
        120, 90.0,
        text = domain,
        fill = "#000000",
        font = ("Comic Sans MS", int(12.0)))
    #COUNTRY TEXT
    canvas.create_text(
        328.5, 90.0,
        text = location['country'],
        fill = "#000000",
        font = ("Comic Sans MS", int(12.0)))
    #CITY TEXT
    canvas.create_text(
        508.0, 90,
        text = location['city'],
        fill = "#000000",
        font = ("Comic Sans MS", int(12.0)))
    #ISP TEXT
    canvas.create_text(
        721.5, 90,
        text = location['isp'],
        fill = "#000000",
        font = ("Comic Sans MS", int(12.0)))
    #----------IP ADDRESS GUI-----------------

    ip_bg = PhotoImage(file=ASSETS_PATH / "ip_bg.png")
    LIST_IP_ADDRESESS = FIND_IP(domain)

    for i in range(0,len(LIST_IP_ADDRESESS)):
        x = 135 + (i*200)
        y = 150 
        ip1 = canvas.create_image(x, y, image=ip_bg)

        canvas.create_text(
        x , y,
        text = LIST_IP_ADDRESESS[i],
        fill = "#000000",
        font = ("Comic Sans MS", int(12.0)))
        if (i==3):
            break

    #------OPEN PORT GUI----------
    canvas.create_rectangle(
        35, 196, 35+80, 196+30,
        fill = "#6592fe",
        outline = "")


    canvas.create_rectangle(
        115, 196, 115+70, 196+30,
        fill = "#85a9ff",
        outline = "")


    canvas.create_rectangle(
        185, 196, 185+85, 196+30,
        fill = "#b1c7fe",
        outline = "")

    canvas.create_text(
        72.5, 210.0,
        text = "Port",
        fill = "#FFFFFF",
        font = ("Comic Sans MS", int(18.0)))

    canvas.create_text(
        148.0, 211.0,
        text = "State",
        fill = "#FFFFFF",
        font = ("Comic Sans MS", int(18.0)))

    canvas.create_text(
        225.0, 210.0,
        text = "Service Name",
        fill = "#FFFFFF",
        font = ("Comic Sans MS", int(10.0)))


    canvas.create_rectangle(
        35, 226, 35+235, 226+255,
        fill = "#e5e5e5",
        outline = "")

    loading_png = tk.PhotoImage(file=ASSETS_PATH / "loading.png")
    loading_img = canvas.create_image(149.5, 350, image=loading_png)
    #call port scanner:

    def find():   
        canvas.delete(loading_img)  
        ports = [21,22,23,53,80,443,194]

        threads = []
        for i in ports:
            thread = threading.Thread(target=PORT_SCANER ,args=[i])

            thread.start()
            threads.append(thread)


        for thread in threads:
            thread.join()
        for i in range(0,len(PORTS)):

            y = 250 +(i*20)

            canvas.create_text(
            73, y,
            text =PORTS[i]['port'],
            fill = "#000000",
            font = ("Comic Sans MS", int(10.0)))
            canvas.create_text(
            149, y,
            text =PORTS[i]['state'],
            fill = "#000000",
            font = ("Comic Sans MS", int(10.0)))

            canvas.create_text(
            226, y,
            text =PORTS[i]['server name'],
            fill = "#000000",
            font = ("Comic Sans MS", int(10.0)))        
            if y >= 400:
                break
    global port_value    
    port_value = tk.Spinbox(window,from_=1 , to=65535,width=10,textvariable=IntVar())
    port_value.place(x=100 , y=420)

    canvas.create_text(
            150, 450,
            text ='must be between 1 and 65535',
            fill = "#000000",
            font = ("Comic Sans MS", int(8.0)))

    search_btn_img = tk.PhotoImage(file=ASSETS_PATH / "seach_btn.png")
    search_btn = tk.Button(
        image=search_btn_img, borderwidth=0, highlightthickness=0,
        command=CHECK_PORT, relief="flat")
    search_btn.place(x=180, y=415, width=25, height=25)
    #---------SUB DOMAIN--------

    canvas.create_rectangle(
        591, 226, 591+240, 226+255,
        fill = "#e5e5e5",
        outline = "")

    canvas.create_rectangle(
        315, 196, 315+240, 196+30,
        fill = "#85a9ff",
        outline = "")

    canvas.create_text(
        435.0, 210.0,
        text = "Sub Domains",
        fill = "#FFFFFF",
        font = ("Comic Sans MS", int(14.0)))

    canvas.create_rectangle(
        315, 222, 315+240, 222+255,
        fill = "#b1c7fe",
        outline = "")
    loading_png1 = tk.PhotoImage(file=ASSETS_PATH / "loading.png")
    loading_img1 = canvas.create_image(430, 350, image=loading_png1)
    #SubDomain:
    def SUB ():
        canvas.delete(loading_img1)
        threads = []
        sub_domain = ['www','mail','store','news','admin','m','email','1']
        for i in sub_domain:
            thread = threading.Thread(target=FIND_SUBDOMAINS ,args=[i])
            thread.start()
            threads.append(thread)


        for thread in threads:
            thread.join()

        for i in range(0,len(SUB_DOMAINS)):

            y = 250 +(i*20)

            canvas.create_text(
            430, y,
            text =SUB_DOMAINS[i],
            fill = "#000000",
            font = ("Comic Sans MS", int(10.0)))
        
            if y >= 400:
                break
    #---------Download All Subdomains----:
    global path_entry_SB
    path_entry_SB = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    path_entry_SB.place(x=325.0, y=435, width=150.0, height=20)
    path_picker_img1 = tk.PhotoImage(file = ASSETS_PATH / "path_picker.png")
    path_picker_button = tk.Button(
        image = path_picker_img1,
        text = '',
        compound = 'center',
        fg = 'white',
        borderwidth = 0,
        highlightthickness = 0,
        command = select_path_SB,
        relief = 'flat')
    path_picker_button.place(
        x = 458, y = 435,
        width = 24,
        height = 22)
    download_btn_img1 = tk.PhotoImage(file=ASSETS_PATH / "download_btn.png")
    download_btn = tk.Button(
        image=download_btn_img1, borderwidth=0, highlightthickness=0,
        command=Download_SubDomain, relief="flat")
    download_btn.place(x=490, y=432, width=25, height=25)


    #-----DIRECTORYS GUI------:
    canvas.create_rectangle(
        591, 196, 591+240, 196+30,
        fill = "#85a9ff",
        outline = "")



    #Directory:
    canvas.create_text(
        695.0, 210.0,
        text = "Directorys",
        fill = "#FFFFFF",
        font = ("Comic Sans MS", int(14.0)))

    Links = FIND_DIRECTORY(domain)

    for i in range(0,len(Links)):

        y = 250 +(i*20)

        if len(Links[i])>40:
            text = Links[i][0:35] + '...'
        else:
            text = Links[i]
        canvas.create_text(
            710, y,
            justify='right',
            text ='[+]'+text,
            fill = "#000000",
            font = ("Comic Sans MS", int(8.0)))
        if y >= 400:
            break
    #------------Download Directory Button-----------:
    global path_entry
    path_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    path_entry.place(x=600.0, y=435, width=150.0, height=20)
    path_picker_img = tk.PhotoImage(file = ASSETS_PATH / "path_picker.png")
    path_picker_button = tk.Button(
        image = path_picker_img,
        text = '',
        compound = 'center',
        fg = 'white',
        borderwidth = 0,
        highlightthickness = 0,
        command = select_path,
        relief = 'flat')
    path_picker_button.place(
        x = 745, y = 435,
        width = 24,
        height = 22)
    download_btn_img = tk.PhotoImage(file=ASSETS_PATH / "download_btn.png")
    generate_btn = tk.Button(
        image=download_btn_img, borderwidth=0, highlightthickness=0,
        command=Download_directorys, relief="flat")
    generate_btn.place(x=780, y=435, width=25, height=25)


    window.after(3000,find)
    window.after(500,SUB)
    window.resizable(False, False)
    window.mainloop()


def main():
    global master
    master = tk.Tk()
    master.geometry("862x519")
    logo = tk.PhotoImage(file=ASSETS_PATH / "gathering.jpg")
    master.call('wm', 'iconphoto', master._w, logo)
    master.title("Information Gathering Tool")
    master.configure(bg="#3A7FF6")
    canvas = tk.Canvas(
        master, bg="#3A7FF6", height=519, width=862,
        bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
    canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")
    #INFORMATION GATHERING TOOL:
    canvas.create_text(
        370, 60,
        text = "INFOR",
        fill = "#ffffff",
        font = ("graceful", int(30)))

    canvas.create_text(
        506, 60,
        text = "MATION",
        fill = "BLUE",
        font = ("RibeyeMarrow-Regular", int(30.0)))


    canvas.create_text(
        375, 100,
        text = "GATH",
        fill = "#ffffff",
        font = ("RibeyeMarrow-Regular", int(30.0)))

    canvas.create_text(
        497, 100,
        text = "ERING",
        fill = "BLUE",
        font = ("RibeyeMarrow-Regular", int(30.0)))

    canvas.create_text(
        402.5, 135.5,
        text = "TO",
        fill = "#ffffff",
        font = ("RibeyeMarrow-Regular", int(30.0)))

    canvas.create_text(
        455, 135.5,
        text = "OL",
        fill = "BLUE",
        font = ("RibeyeMarrow-Regular", int(30.0)))
    #-----
    text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
    token_entry_img = canvas.create_image(650.5, 200.5, image=text_box_bg)

    #ENTRY: Get domain name:
    canvas.create_text(
        490.0, 180.0, text="Domain Name:", fill="#515486",
        font=("Arial-BoldMT", int(13.0)), anchor="w")
    global domain_entry
    domain_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    domain_entry.place(x=490.0, y=200, width=321.0, height=35)
    domain_entry.focus()



    title = tk.Label(
        text="Welcome to Information Gathering", bg="#3A7FF6",
        fg="white", font=("Arial-BoldMT", int(18.0)))
    title.place(x=20.0, y=160.0)


    info_text = tk.Label(
        text="Information Gathering Tool uses the Sockets\n"
        "to analyse a Website:\n"
        "▫Find Ip Address\n"
        "▫Find Open Ports\n"
        "▫Find Subdomains\n" 
        "▫Find Directory\n" 


        ,bg="#3A7FF6", fg="white", justify="left",
        font=("Georgia", int(14.0)))

    info_text.place(x=27.0, y=200.0)

    name_text = tk.Label(
        text="✍(✿◠‿◠) Fatemeh Homayouni | UMZ " 
        ,bg="#3A7FF6", fg="white", justify="left",
        font=("Georgia", int(10.0)))

    name_text.place(x=27.0, y=450.0)    
    #---Host Information: --
    location_bg = tk.PhotoImage(file=ASSETS_PATH / "location.png")
    location_img = canvas.create_image(500.5, 270.5, image=location_bg)
    my_hostname = s.gethostname()
    my_hostip = s.gethostbyname(my_hostname)

    title = tk.Label(
        text=f"Your IP address is : {my_hostip}",bg='white',
        fg="black", font=("Arial-BoldMT", int(10.0)))
    title.place(x=510.5, y=260.5)



    generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
    generate_btn = tk.Button(
        image=generate_btn_img, borderwidth=0, highlightthickness=0,
        command=btn_clicked, relief="flat")
    generate_btn.place(x=557, y=350, width=180, height=55)

    master.mainloop()


main()