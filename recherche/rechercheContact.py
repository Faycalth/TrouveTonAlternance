#récupère adresse mail à partir d'une liste de nom d'entreprise 
#libraries
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import urllib.parse
import urllib.error
import csv
import time
import os
import re
from datetime import datetime

def contact(liste_ville):
    fichier_src = getNomFichier()
    nom_fichier = maj_csv(fichier_src)
    return nom_fichier

def getNomFichier():
    nom_fichier = "entreprises_informatiques.csv"
    try:
        if os.path.isfile(nom_fichier):
            return nom_fichier
        else:
            raise NameError("Erreur, le fichier n'est pas dans le dossier")
    except NameError:
        print("Le fichier 'entreprises_informatiques.csv' n'est pas dans le dossier")

def getNomEntreprise(source):
    liste_nom = []
    with open(source, "r") as fichier_src:
        reader = csv.DictReader(fichier_src)
        for row in reader:
            nom = row['Nom']
            liste_nom.append(nom.lower())
    return liste_nom

def get_url(nom):
    url = "https://www.google.com/search?q="+nom
    req = Request(url.replace(" ", "+"), headers={'User-Agent': 'Mozilla/5.0', 'cookie': '<my cookie>'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    url_site = ""

    #recherche dans la recherche
    try:
        page_recherche = soup.find("body")
        resultats = page_recherche.find_all("a")

        #liste de tous les liens
        liste_liens = []
        
        for r in resultats:
            x = nom.split(" ")
            if "www."+x[0] in r.get('href'):
                #extraction du nom de domaine
                liste_liens.append(r.get("href"))
                l2 = liste_liens[0].split("/")
                url_site = l2[3]
                break
    except:
        pass
            
    return url_site
  
def get_mail(url):           
    url_site = "https://www.google.com/search?q="+url+"+contact"
    req_site = Request(url_site, headers={'User-Agent': 'Mozilla/5.0', 'cookie': '<my cookie>'})
    page_site = urlopen(req_site).read()
    soup_site = BeautifulSoup(page_site, 'html.parser')
    

    #recherche dans la recherche
    try:
        page_contact = soup_site.find("body")
        resultats_contact = page_contact.find_all("div")

        liste = []
        for r in resultats_contact:
            liste.append(r.getText())
        
        #extraction mail
        liste_mail = []
        #regex = "\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b" #pattern mail
        for l in liste:
            if "@" in l:
                liste_mail_2 = extraireMail(l)
                for l2 in liste_mail_2:
                    if l2 not in liste_mail:
                        liste_mail.append(l2)

    except:
        pass
    
    return liste_mail 

def extraireMail(texte):
    pattern = "\S+@+\S+"
    liste = re.findall(pattern, texte)
    liste_mail = []
    for l in liste:
        pattern2 = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+", l)  
        for p in pattern2:
            if p not in liste_mail:
                liste_mail.append(p)

    return liste_mail 
                

def maj_csv(source):
    nom_fichier = "contact_entreprise.csv"

    with open(nom_fichier, "w", newline='') as maj_fichier, open(source, "r") as fichier_src:
        fieldnames = ["Nom","Code Postal","Ville","Activite principale","Site Web","Contact"]

        writer = csv.DictWriter(maj_fichier, fieldnames=fieldnames, restval="")
        writer.writeheader()

        reader = csv.DictReader(fichier_src)    

        liste_nom_ent = getNomEntreprise(source)
        i = 0
        j = len(getNomEntreprise(source))
        k = 0
        for row in reader:
            try:
                nom = row["Nom"].lower()
                if nom in liste_nom_ent:
                    site_web = get_url(nom)
                    if site_web:
                        contact = get_mail(site_web)
                        if contact:
                            k+=1
                    else:
                        contact = []
                    
                    writer.writerow({
                        'Nom': row["Nom"],
                        'Ville': row["Ville"], 
                        'Code Postal': row["Code Postal"],
                        'Activite principale': row["Activite principale"],
                        'Site Web': site_web,
                        'Contact': contact
                    })
                i+=1
                print(str(i), " lignes traitées sur", j, end="\r")
                time.sleep(0.05)
            except urllib.error.HTTPError as err: 
                if err.code == 429:
                    print("Erreur HTTP 429 ('Too many requests')")
                    print("Arrêt momentané du programme, reprise dans 10 minute ( heure actuelle :", str(datetime.now().time()), ")")
                    print(str(k), " adresses mails trouvées pour le moment") 
                    time.sleep(600) #erreur HTTP 429 "Too many requests" ou ConnectionResetError (problème de connexion)
                    continue
                else:
                    print(err.code)
                    print("Arrêt momentané du programme, reprise dans 1 minute (heure actuelle :", str(datetime.now().time()), ")")
                    print(str(k), " adresses mails trouvées pour le moment") 
                    time.sleep(60) #erreur HTTP 429 "Too many requests" ou ConnectionResetError (problème de connexion)
                    continue
                    
            except ConnectionResetError:
                print("Erreur ConnectionResetError")
                print("Arrêt momentané du programme, reprise dans 2 minutes ( heure actuelle :", str(datetime.now().time()), ")")
                print(str(k), " adresses mails trouvées pour le moment") 
                time.sleep(120) #erreur HTTP 429 "Too many requests" ou ConnectionResetError (problème de connexion)
                continue
            except PermissionError:
                print("Erreur de permission, veuillez fermer les fichiers que le programme utilise (Excel notamment)")
                print("Arrêt momentané du programme, reprise dans 30 secondes ( heure actuelle :", str(datetime.now().time()), ")")
                print(str(k), " adresses mails trouvées pour le moment") 
                time.sleep(30) 
                continue
            except:
                print("Erreur inconnue :", err.code)
                print("Arrêt momentané du programme, reprise dans 1 minute ( heure actuelle :", str(datetime.now().time()), ")")
                print(str(k), " adresses mails trouvées pour le moment") 
                time.sleep(60) #erreur HTTP 429 "Too many requests" ou ConnectionResetError (problème de connexion)
                continue
        try:
            print("Programme terminé | ", str(k), "listes d'adresses mails trouvées sur", str(j), "(", round(k/(j-1),2),"%)")
        except:
            print("Programme terminé | ", str(k), "listes d'adresses mails trouvées")
            return nom_fichier
                     
              
#Programme
#start_time = time.time()
#main()
#print("Temps d'execution = " + str(time.time() - start_time) + " secondes")
