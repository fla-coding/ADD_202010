import os, json, requests
from datetime import datetime
from datetime import timedelta
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from functools import partial
from pathlib import Path

def validateLogin(tkWindow, prenom, nom, date_naissance, lieu_naissance, adresse, cp, ville, travail, sante, famille, handicap, convocation, missions, transits, animaux, dh_options):
    prenom = prenom.get()
    nom = nom.get()
    date_naissance = date_naissance.get()
    lieu_naissance = lieu_naissance.get()
    adresse = adresse.get()
    cp = cp.get()
    ville = ville.get()
    travail = travail.get()
    sante = sante.get()
    famille = famille.get()
    handicap = handicap.get()
    convocation = convocation.get()
    missions = missions.get()
    transits = transits.get()
    animaux = animaux.get()
    dh_options = dh_options.get()
    liste_motifs = []
    if travail == 1:
        liste_motifs.append("travail")
    if sante == 1:
        liste_motifs.append("sante")
    if famille == 1:
        liste_motifs.append("famille")
    if handicap == 1:
        liste_motifs.append("handicap")
    if convocation == 1:
        liste_motifs.append("convocation")
    if missions == 1:
        liste_motifs.append("missions")
    if transits == 1:
        liste_motifs.append("transits") 
    if animaux == 1:
        liste_motifs.append("animaux") 
    try:
        if dh_options == "Personnalisées":
            date = simpledialog.askstring('Date', 'Veuillez entrer la date (JJ/MM/AAAA).')
            heure = simpledialog.askstring('Heure', 'Veuillez entrer l\'heure (HH:MM).')
        elif dh_options == "Ajouter un délai":
            delai = simpledialog.askstring('Délai', 'Veuillez entrer le délai, en minutes.')
            date_et_heure = datetime.today() + timedelta(minutes=int(delai))
            date = f"{date_et_heure.day}/{date_et_heure.month}/{date_et_heure.year}"
            heure = f"{date_et_heure.hour}:{date_et_heure.minute}"
        else:
            date = f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}"
            heure = f"{datetime.today().hour}:{datetime.today().minute}"
        url = 'https://fla-coding.freeboxos.fr:36500/generate'
        content = {"prenom": prenom, "nom": nom, "date_naissance": date_naissance, "lieu_naissance": lieu_naissance, "adresse": adresse, "ville": ville, "cp": cp, "date_sortie": date, "heure_sortie": heure, "motifs": liste_motifs}
        headers = {"Content-Type": "application/json"}
        content = json.dumps(content)
        x = requests.get(url, data=content, headers=headers)
        home = os.getenv('HOME')
        open(f"{home}/Desktop/attestation_{datetime.today().hour}h{datetime.today().minute}.pdf", 'wb').write(x.content)
        messagebox.showinfo("Sauvegardé", f"L'attestation a bien été sauvegardée sur votre bureau sous le nom « attestation_{datetime.today().hour}h{datetime.today().minute}.pdf ».")
        try:
            elements = {'prenom': prenom, 'nom': nom, 'date_naissance': date_naissance, 'lieu_naissance': lieu_naissance, 'adresse': adresse, 'cp': cp, 'ville': ville}
            elements = json.dumps(elements)
            with open(f"{home}/Library/Preferences/add_202010/preremplissage.json", "w") as preremplissage:
                preremplissage.write(elements)
        except:
            pass
        tkWindow.destroy()
    except:
        messagebox.showerror("Erreur", "Une erreur est survenue.")
        tkWindow.destroy()


#Tentative de préremplissage
home = os.getenv('HOME')
cache_dir = Path(f"{home}/Library/Preferences/add_202010")
if cache_dir.is_dir() == True:
    try:
        with open(f"{home}/Library/Preferences/add_202010/preremplissage.json", "r") as preremplissage:
            elements = preremplissage.read()
        elements = json.loads(elements)
        prenom1 = elements['prenom']
        nom1 = elements['nom']
        date_naissance1 = elements['date_naissance']
        lieu_naissance1 = elements['lieu_naissance']
        adresse1 = elements['adresse']
        cp1 = elements['cp']
        ville1 = elements['ville']
    except:
        prenom1 = ''
        nom1 = ''
        date_naissance1 = ''
        lieu_naissance1 = ''
        adresse1 = ''
        cp1 = ''
        ville1 = ''
else:
    os.system(f"mkdir {home}/Library/Preferences/add_202010")
    prenom1 = ''
    nom1 = ''
    date_naissance1 = ''
    lieu_naissance1 = ''
    adresse1 = ''
    cp1 = ''
    ville1 = ''

#window
tkWindow = Tk()  
tkWindow.geometry('810x570')  
tkWindow.resizable(width=True, height=True)
tkWindow.title('Générateur d\'attestation de déplacement dérogatoire')

#prenom label and text entry box
prenomLabel = Label(tkWindow, text="Prénom :", wraplength=600).grid(sticky='e', row=0, column=0)
prenom = StringVar(value=prenom1)
prenomEntry = Entry(tkWindow, textvariable=prenom).grid(row=0, column=1)  

#nom label and password entry box
nomLabel = Label(tkWindow, text="Nom :", wraplength=600).grid(sticky='e', row=1, column=0)
nom = StringVar(value=nom1)
nomEntry = Entry(tkWindow, textvariable=nom).grid(row=1, column=1)  

#date_naissance label and url entry box
date_naissanceLabel = Label(tkWindow, text="Date de naissance (JJ/MM/AAAA) :", wraplength=600).grid(sticky='e', row=2, column=0)  
date_naissance = StringVar(value=date_naissance1)
date_naissanceEntry = Entry(tkWindow, textvariable=date_naissance).grid(row=2, column=1)  

#lieu_naissance label and url entry box
lieu_naissanceLabel = Label(tkWindow, text="Lieu de naissance :", wraplength=600).grid(sticky='e', row=3, column=0)  
lieu_naissance = StringVar(value=lieu_naissance1)
lieu_naissanceEntry = Entry(tkWindow, textvariable=lieu_naissance).grid(row=3, column=1)  

#adresse label and url entry box
adresseLabel = Label(tkWindow, text="Adresse (n° et rue) :", wraplength=600).grid(sticky='e', row=4, column=0)  
adresse = StringVar(value=adresse1)
adresseEntry = Entry(tkWindow, textvariable=adresse).grid(row=4, column=1)

#cp label and url entry box
cpLabel = Label(tkWindow, text="Code postal :", wraplength=600).grid(sticky='e', row=5, column=0)  
cp = StringVar(value=cp1)
cpEntry = Entry(tkWindow, textvariable=cp).grid(row=5, column=1)

#ville label and url entry box
villeLabel = Label(tkWindow, text="Ville :", wraplength=600).grid(sticky='e', row=6, column=0)
ville = StringVar(value=ville1)
villeEntry = Entry(tkWindow, textvariable=ville).grid(row=6, column=1) 

#travail tick
travailLabel = Label(tkWindow, text="Déplacements entre le domicile et le lieu d'exercice de l'activité professionnelle ou le lieu d'enseignement et de formation, déplacements professionnels ne pouvant être différés", wraplength=600).grid(sticky='e', row=7, column=0) 
travail = IntVar()
Checkbutton(tkWindow, variable=travail).grid(row=7, column=1)

#sante tick
santeLabel = Label(tkWindow, text="Déplacements pour des consultations et soins ne pouvant être assurés à distance et ne pouvant être différés ou pour l'achat de produits de santé", wraplength=600).grid(sticky='e', row=8, column=0) 
sante = IntVar()
Checkbutton(tkWindow, variable=sante).grid(row=8, column=1)

#famille tick
familleLabel = Label(tkWindow, text="Déplacements pour motif familial impérieux, pour l'assistance aux personnes vulnérables ou précaires ou pour la garde d'enfants", wraplength=600).grid(sticky='e', row=9, column=0) 
famille = IntVar()
Checkbutton(tkWindow, variable=famille).grid(row=9, column=1)

#handicap tick
handicapLabel = Label(tkWindow, text="Déplacements des personnes en situation de handicap et de leur accompagnant", wraplength=600).grid(sticky='e', row=10, column=0) 
handicap = IntVar()
Checkbutton(tkWindow, variable=handicap).grid(row=10, column=1)

#convocation tick
convocationLabel = Label(tkWindow, text="Déplacements pour répondre à une convocation judiciaire ou administrative", wraplength=600).grid(sticky='e', row=11, column=0) 
convocation = IntVar()
Checkbutton(tkWindow, variable=convocation).grid(row=11, column=1)

#missions tick
missionsLabel = Label(tkWindow, text="Déplacements pour participer à des missions d'intérêt général sur demande de l'autorité administrative", wraplength=600).grid(sticky='e', row=12, column=0) 
missions = IntVar()
Checkbutton(tkWindow, variable=missions).grid(row=12, column=1)

#transits tick
transitsLabel = Label(tkWindow, text="Déplacements liés à des transits ferroviaires ou aériens pour des déplacements de longues distances", wraplength=600).grid(sticky='e', row=13, column=0) 
transits = IntVar()
Checkbutton(tkWindow, variable=transits).grid(row=13, column=1)

#animaux tick
animauxLabel = Label(tkWindow, text="Déplacements brefs, dans un rayon maximal d'un kilomètre autour du domicile pour les besoins des animaux de compagnie", wraplength=600).grid(sticky='e', row=14, column=0) 
animaux = IntVar()
Checkbutton(tkWindow, variable=animaux).grid(row=14, column=1)

#Date & heure de sortie
dh_optionsLabel = Label(tkWindow, text="Date et heure de sortie :", wraplength=600).grid(sticky='e', row=15, column=0)  
listeOptions=["Actuelles", "Personnalisées", "Ajouter un délai"]
dh_options = ttk.Combobox(tkWindow, values=listeOptions, state="readonly")
dh_options.grid(row=15, column=1)
dh_options.current(0)

#blank space
blankLabel = Label(tkWindow, text="").grid(row=16, column=0)

validateLogin = partial(validateLogin, tkWindow, prenom, nom, date_naissance, lieu_naissance, adresse, cp, ville, travail, sante, famille, handicap, convocation, missions, transits, animaux, dh_options)

#login button
loginButton = Button(tkWindow, text="Générer", command=validateLogin).grid(sticky='e', row=17, column=0)   

tkWindow.mainloop()
