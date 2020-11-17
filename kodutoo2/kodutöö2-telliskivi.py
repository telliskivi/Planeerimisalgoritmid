#!/usr/bin/env python3
# vim: set fileencoding=utf8 :
# Näiteprogramm protsessoriaja planeerijate visualiseerimiseks
# algne autor Sten-Oliver Salumaa
# refaktoreerinud ja muidu muutnud Meelis Roos

from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox

def puhasta():
    tahvel.delete('all')

# joonistab tahvlile protsesse kujutavad ristkülikud numbrite ja protsesside nimedega
def joonista(jarjend, valjasta):
    protsessid = {"A" :"green", "B" : "red", "C" : "orange", "D" : "blue", "E" : "yellow", "F" : "purple", "G" : "lime", "H" : "pink", "I" : "cyan", "J" : "grey"}
    tähised = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    puhasta()
    x1 = 120
    y1 = 50
    kaugus = 0
    suurus = 15

    tahvel.create_text(25, 25, text="Etapp", font=("bold", 10))
    tahvel.create_text(80, 25, text="Lisatud", font=("bold", 10))
    tahvel.create_text(80, 40, text="protsess", font=("bold", 10))

    for i in range(len(valjasta)):
        texty = ((y1 + suurus * i) + (y1 + suurus * (i + 1))) / 2
        if i < len(jarjend):
            tahvel.create_text(25, texty, text=str(i))
            tahvel.create_text(80, texty, text=tähised[i] + ": " + str(jarjend[i][0]) + "," + str(jarjend[i][1]))
        else:
            tahvel.create_text(25, texty, text=str(i))
            tahvel.create_text(80, texty, text="-")

    for i in range(50):
        textx = ((x1 + suurus*i) + (x1 + suurus*(i+1)))/2
        texty = 40
        tahvel.create_text(textx, texty, text=str(i))

    for i in range(len(valjasta)):
        for j in range(len(valjasta[0])):
            x2 = x1 + suurus
            y2 = y1 + suurus
            if valjasta[i][j] != "-":
                kujund = tahvel.create_rectangle(x1, y1, x2, y2, fill=protsessid.get(valjasta[i][j]))
                keskpaikx = (x1 + x2)/2
                keskpaiky = (y1 + y2)/2
                tahvel.create_text(keskpaikx, keskpaiky, text=valjasta[i][j])
                x1 += suurus
            else:
                kujund = tahvel.create_rectangle(x1, y1, x2, y2, fill="white")
                keskpaikx = (x1 + x2) / 2
                keskpaiky = (y1 + y2) / 2
                tahvel.create_text(keskpaikx, keskpaiky, text="-")
                x1 += suurus
        x1 = 120
        y1 += suurus
        
def joonistaErind(tähis):
    tähised = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    x1 = 120
    y1 = 50
    suurus = 15
    for i in range(len(tähised)):
        if tähised[i] == tähis:
            tahvel.create_rectangle(x1, (y1 + suurus*i), (x1 + suurus*50), (y1 + suurus*(i + 1)), fill="black")
            tahvel.create_text((x1 + (x1 + suurus*50))/2, ((y1 + suurus*i) + (y1 + suurus*(i + 1)))/2, text="Protsess ei mahu mällu", fill="lightgrey")

# teeb järjendist kahetasemelise listi, mida on mugavam töödelda
def massiiviks(input_jarjend):
    valjund = []
    jupid = input_jarjend.split(";")
    for i in range(len(jupid)):
        hakkliha = jupid[i].split(",")
        saabumine = int(hakkliha[0])
        kestus = int(hakkliha[1])
        valjund.append([saabumine, kestus])
    return valjund

# otsustab, millist järjendit teha kahetasemeliseks massiiviks
def massiiviMeister():
    jarjend = []
    if var.get() == 1:
        return massiiviks(predef1)
    elif var.get() == 2:
        return massiiviks(predef2)
    elif var.get() == 3:
        return massiiviks(predef3)
    elif var.get() == 4:
        try:
            return massiiviks(kasutaja_jarjend.get())
        except:
            messagebox.showerror(title="Viga sisendis", message="Vigane kasutaja muster!")
            return massiiviks(predef1)
    else:
        return massiiviks(predef1)
    
def teeMaatriks(jarjend):
    massiiv = []
    for i in range(10):
        abi = []
        for j in range(50):
            abi.append("-")
        massiiv.append(abi)
    return massiiv

def plokideLeidja(protsess, pikkus):
    plokid = []
    abi = []
    for i in range(len(protsess)):
        if protsess[i] == "-":
            abi.append(i)
        else:
            if len(abi) >= pikkus:
                plokid.append(copy.deepcopy(abi))
                abi.clear()
            else:
                abi.clear()
    if len(abi) >= pikkus and not plokid.__contains__(abi):
        plokid.append(abi)

    for plokk in plokid:
        if len(plokk) < pikkus:
            plokid.remove(plokk)
    return plokid
    
# näitab programmis käimasolevat protsessijada
def massiiviTeavitaja(massiiv):
    text.delete(1.0, END)
    for jupp in massiiv:
        text.insert(INSERT, str(jupp) + "\n")

def kasuvalija(jarjend, algoritm):
    if algoritm == "firstfit":
        return firstfit(jarjend)
    elif algoritm == "lastfit":
        return lastfit(jarjend)
    elif algoritm == "bestfit":
        return bestfit(jarjend)
    elif algoritm == "worstfit":
        return worstfit(jarjend)
    elif algoritm == "randomfit":
        return randomfit(jarjend)

def jooksuta_algoritmi(algoritm):
    jarjend = massiiviMeister()
    massiiviTeavitaja(jarjend)
    (valjund, ooteaeg) = kasuvalija(jarjend, algoritm)
    joonista(valjund)
    keskm_oot = tahvel.create_text(80, 40, text="Keskmine ooteaeg:  " + str(ooteaeg))

predef1 = "4,5;2,7;9,2;4,6;7,1;6,4;8,8;3,6;1,10;9,2"
predef2 = "1,10;6,6;3,9;2,4;1,6;5,2;1,4;5,2;2,1;2,7"
predef3 = "5,10;6,6;3,9;8,4;3,6;5,12;1,4;15,3;3,4;9,7"

# GUI
raam = Tk()
raam.title("Planeerimisalgoritmid")
raam.resizable(False, False)
raam.geometry("800x400")

var = IntVar()
var.set(1)
Radiobutton(raam, text="Esimene", variable=var, value=1).place(x=10,y=40)
Radiobutton(raam, text="Teine", variable=var, value=2).place(x=10,y=70)
Radiobutton(raam, text="Kolmas", variable=var, value=3).place(x=10,y=100)
Radiobutton(raam, text="Enda oma", variable=var, value=4).place(x=10,y=130)

silt_vali = ttk.Label(raam, text="Vali või sisesta järjend (kujul 1,10;4,2;12,3;13,2)")
silt_vali.place(x=10, y=10)

silt1 = ttk.Label(raam, text=predef1)
silt1.place(x=120, y=40)

silt2 = ttk.Label(raam, text=predef2)
silt2.place(x=120, y=70)

silt3 = ttk.Label(raam, text=predef3)
silt3.place(x=120, y=100)

silt_run = ttk.Label(raam, text="Algoritmi käivitamiseks klõpsa nupule")
silt_run.place(x=10, y=160)

silt_tahvel = ttk.Label(raam, text="Käsil olevad protsessid:")
silt_tahvel.place(x=450, y=10)

kasutaja_jarjend = ttk.Entry(raam)
kasutaja_jarjend.place(x=120, y=130, height=25, width=240)

tahvel = Canvas(raam, width=800, height=180, background="white")
tahvel.place(x=0, y=220)

LIFO_nupp = ttk.Button(raam, text="First-Fit", command = lambda : jooksuta_algoritmi("firstfit"))
LIFO_nupp.place(x=10, y=190,height=25, width=80)

SJF_nupp = ttk.Button(raam, text="Last-Fit", command = lambda : jooksuta_algoritmi("lastfit"))
SJF_nupp.place(x=100, y=190,height=25, width=80)

SJF_nupp = ttk.Button(raam, text="Best-Fit", command = lambda : jooksuta_algoritmi("bestfit"))
SJF_nupp.place(x=190, y=190,height=25, width=80)

RR_nupp = ttk.Button(raam, text="Worst-Fit", command = lambda : jooksuta_algoritmi("worstfit"))
RR_nupp.place(x=280, y=190,height=25, width=80)

ML_nupp = ttk.Button(raam, text="Random-Fit", command = lambda : jooksuta_algoritmi("randomfit"))
ML_nupp.place(x=370, y=190,height=25, width=80)

puhasta_nupp = ttk.Button(raam, text="Puhasta väljund", command = lambda : puhasta() )
puhasta_nupp.place(x=500, y=190,height=25, width=130)

text = Text(raam, width=25, height=9)
text.place(x=450, y=30)

raam.mainloop()

