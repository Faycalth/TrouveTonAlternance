#https://docs.python.org/fr/3/library/csv.html
import csv,os

dict_act = {'61.10Z': 'Telecommunications filaires', '61.20Z': 'Telecommunications sans fil', '61.30Z': 'Télécommunications par satellite','61.90Z': 'Autres activités de télécommunication','62.01Z': 'Programmation informatique','62.02A': 'Conseil en systèmes et logiciels informatiques','62.02B': 'Tierce maintenance de systèmes et d applications informatiques','62.03Z': 'Gestion d installations informatiques','62.09Z': 'Autres activités informatiques','63.11Z': 'Traitement de données, hébergement et activités connexes','63.12Z': 'Portails Internet'}

def entreprise():
    #création dictionnaire clé valeur
    key_list = list(dict_act.keys())
    value_list = list(dict_act.values())

    liste_ville = recherche(get_nom_fichier(),get_ville(),get_activite(key_list, value_list))
    print("Votre fichier se trouve dans : ", os.getcwd())
    return liste_ville

def get_nom_fichier():
    nom_fichier = "liste_entreprise.csv"
    if os.path.isfile(nom_fichier):
        return nom_fichier
    else:
        print("Erreur, le fichier n'est pas dans le dossier")

def get_ville():
    liste_ville = []
    liste_ville_fichier = getVilleFichier()
    print("Précisez les différents arrondissements de Lyon telles que : LYON 1ER, LYON 2EME, etc")
    print("Précisez les différents arrondissements de Paris telles que : PARIS 1, PARIS 2, etc")
    print("X pour arrêter d'entrer des villes")

    i = True
    while(i):
        inp_ville = str(input("Entrez les villes des entreprises : "))
        if (inp_ville=="X" or inp_ville=="x"):
            i=False
        elif (inp_ville.upper() not in liste_ville_fichier):
            print("Réessayez, la ville n'est pas connue")
        else: 
            liste_ville.append(inp_ville.upper()) 
            
    return liste_ville

def getVilleFichier():
    ville_fichier = []
    with open(get_nom_fichier(), "r") as fichier_src:          
        reader = csv.DictReader(fichier_src)
        for row in reader:
            ville = row['libelleCommuneEtablissement']
            ville_fichier.append(ville)
    
    return ville_fichier



def get_activite(key_list, value_list):
    i = True
    liste_activite = []
    print("X pour arrêter d'entrer les activités")

    while(i):
        affichage_activite(value_list)
        try:
            inp_activite = input("\nEntrez le numero de l'activite de l'entreprise : ")
            if( inp_activite=="X" or inp_activite=="x" ):
                i=False   
            else:  
                liste_activite.append(key_list.pop(int(inp_activite)))
                value_list.pop(int(inp_activite)) 
        except:
            i = False
    
    return liste_activite

def affichage_activite(value_list):
    nb = 0
    for value in value_list:
        print(nb,":",value)
        nb = nb + 1

def recherche(nom_fichier_src, liste_ville, liste_activite):
    #variables
    nom_fichier_sortie = "entreprises_informatiques.csv"
    count = 0
    fieldnames = ['Nom', 'Code Postal', 'Ville', 'Activite principale']

    #Algorithme de recherche
    with open(nom_fichier_src, "r") as fichier_src, open(nom_fichier_sortie, "w", newline="") as fichier_sortie:  #Ouverture des fichiers
        writer = csv.DictWriter(fichier_sortie, fieldnames=fieldnames, restval="")
        writer.writeheader()
        
        reader = csv.DictReader(fichier_src)
        for row in reader:
            if(row['libelleCommuneEtablissement'] in liste_ville and row['categorieJuridiqueUniteLegale']!="1000"):
                if(row['activitePrincipaleUniteLegale'] in liste_activite):
                    writer.writerow({
                        'Nom':row['denominationUniteLegale']+" "+row['sigleUniteLegale'],
                        'Ville':row['libelleCommuneEtablissement'], 
                        'Code Postal':row['codePostalEtablissement'],
                        'Activite principale': dict_act[row['activitePrincipaleUniteLegale']]
                    })
                    count = count + 1
    print("\nNombre d'entreprises trouvées : ", count)

    return liste_ville


#Programme
#entreprise()

