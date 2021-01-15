import recherche.rechercheEntreprise as ent
import recherche.rechercheContact as c
import recherche.envoiMail as mail
import csv
import re

"""
def envoiMail(fichier_mail):
    fichier_bilan = "bilan_mail.csv"
    with open(fichier_mail, "r") as fichier, open(fichier_bilan, "w", newline="") as bilan:
        fieldnames = ["Nom","Ville","Site Web","Activite principale","Adresse mail","Email"]

        writer = csv.DictWriter(bilan, fieldnames=fieldnames, restval="")
        writer.writeheader()

        reader = csv.DictReader(fichier) 

        for r in reader:
            try:
                if r["Contact"]:
                    nom_entreprise = r["Nom"]
                    domaine_entreprise = r["Activite principale"]
                    liste_mail = r["Contact"]
                    ville = r["Ville"]
                    site_web = r["Site Web"]

                    liste = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+", liste_mail)

                    for l in liste:
                        print(l)
                        try:
                            texte_mail = mail.envoyer_mail(nom_entreprise, domaine_entreprise, l)
                            writer.writerow({
                                'Nom': nom_entreprise,
                                'Ville': ville,
                                'Site Web': site_web,
                                'Activite principale': domaine_entreprise,
                                'Adresse mail': l, 
                                'Email': texte_mail
                            })
                        except:
                            print("raté")
                    
                else:
                    print("Pas de mail")
            except:
                continue

"""
liste_ville = ent.entreprise()
fichier_mail = c.contact(liste_ville)
"""
fichierMail = "contact_entreprise.csv"
envoiMail(fichierMail) 
"""