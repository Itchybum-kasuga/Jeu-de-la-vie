from tkinter import *
import csv
import datetime

# Variables globales pour suivre l'état du jeu
global jour
global saisie
global en_cour
global nbr_cell_jour
global date_jour
global liste_jours

# initialisation des variables globales
jour = 0
saisie = True
liste_jours = []
nbr_cell_jour = []
date_jour = []
en_cour = True

def dessin_grille() :
# dessin des lignes verticales
    x=100
    for i in range(21):
        y1=0
        y2=600
        Zone.create_line (x , y1 , x , y2 ,width=4,fill="blue")
        x=x+30
# dessin des lignes horizontales
    y = 0
    for i in range(21):
        x1=100
        x2=700
        Zone.create_line (x1 , y , x2 , y ,width=4,fill="blue")
        y= y + 30
    """J'ai pris la liberté de retirer la ligne qui redessinait constament la
    grille, cette dernière n'étant plus nécessaire avec mes points ne
    dépassant pas de leurs cases individuelles."""

#fonction appelée à chaque clic
def coordonnees(event) :
    global saisie

    col = (event.x-100) // 30
    li = event.y // 30
    #verification que le clic est dans la grille
    if col >= 0 and saisie == True :
        #dessine créature si il n'y en a pas
        if grille[li][col] == 0 :
            dessiner_creature(li, col, 1)
            grille[li][col] = 1
        #efface créature si il en a
        else :
            dessiner_creature(li, col, 0)
            grille[li][col] = 0
    #message d'erreur si hors de la grille
    else :
        print("Clic en dehors de la grille")

def validation_du_jeu() :
    global saisie
    #enregistre le jour 0 dans la liste des nombres des cellules par jour
    cellules = 0
    for x in range(20) :
        for y in range (20) :
            if grille[x][y] == 1 :
                cellules = cellules + 1
    nbr_cell_jour.append(cellules)
    print("Vous avez validé")
    #désactive la saisie des clics dans la grille
    saisie = False

def fin_partie():
    global en_cour
    global jour
    #désactive le boutont "jour suivant"
    en_cour = False
    print("Les créature ont survécus", jour, "jours.")
    #combine les listes
    donnees_combinees = zip(liste_jours, nbr_cell_jour, date_jour)
    #enregistre la combinaison des listes dans le fichier "grille.csv"
    with open('grille.csv', 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        # Écriture de l'en-tête
        writer.writerow(['Jour', 'Cellules', 'Date'])
        # Écriture des données
        writer.writerows(donnees_combinees)

def jour_suivant():
   global saisie
   global jour
   #vérifie que la saisie des clics est désactivé est que le jeu n'est pas fini
   if saisie == False and en_cour == True :
       #crée des liste des nouvelles créatures et de celles qui vont mourrir afin d'appliquer leurs état une fois les vérification des créatures éxistante terminée
       nait = []
       morts = []
       #parcour la liste de la grille etièrement
       for x in range (20) :
            for y in range (20) :
                voisins = 0
                #vérifie les case adjacente si elles ne sont pas en dehors de la grille pour compter le nombre de voisins
                if x != 0 and y != 0 :
                    if grille[x-1][y-1] == 1 :
                        voisins = voisins + 1

                if y != 0 :
                    if grille[x][y-1] == 1 :
                        voisins = voisins + 1

                if y != 0 and x != 19:
                    if grille[x+1][y-1] == 1 :
                        voisins = voisins + 1

                if x != 0 :
                    if grille[x-1][y] == 1 :
                        voisins = voisins + 1

                if x != 19 :
                    if grille[x+1][y] == 1 :
                        voisins = voisins + 1

                if x != 0 and y != 19:
                    if grille[x-1][y+1] == 1 :
                        voisins = voisins + 1

                if y != 19 :
                    if grille[x][y+1] == 1 :
                        voisins = voisins + 1

                if x != 19 and y != 19 :
                    if grille[x+1][y+1] == 1 :
                        voisins = voisins + 1
                #si il y a une créature sur la case
                if grille[x][y] == 1 :
                    #tue la créature si elle n'a pas 2 ou 3 voisins
                    if voisins != 2 and voisins != 3 :
                        morts.append((x,y))
                        dessiner_creature(x,y,0)
                    #change la créature en jaune si elle a 2 ou 3 voisins
                    else :
                        dessiner_creature(x,y,1)
                #si il n'y a pas de créature sur la case
                else :
                    #crée une créature bleu si il y a 3 voisins
                    if voisins == 3 :
                        nait.append((x,y))
                        dessiner_creature(x,y,3)
       #termine la partie si il n'y a lus de changements
       if not morts and not nait :
            fin_partie()
       #applique les nouveaux états stocké dans les listes "morts" et "nait"
       for m in range(len(morts)):
            grille[morts[m][0]][morts[m][1]] = 0
       for n in range(len(nait)):
            grille[nait[n][0]][nait[n][1]] = 1
            
        

       #compte le nombre de cellules total
       cellules = 0
       for x in range(20) :
           for y in range (20) :
                if grille[x][y] == 1 :
                    cellules = cellules + 1
       #si il y a des cellules, incrémente le compteur de jours et ajoute les données aux listes respectives
       if cellules != 0 :
            jour = jour + 1
            liste_jours.append(jour)
            nbr_cell_jour.append(cellules)
            date_jour.append(datetime.datetime.now())
       #si il n'y a plus de créature appelle la fonction de fin de partie et ajoute les infos aux listes respectives
       else :
            liste_jours.append(jour + 1)
            nbr_cell_jour.append(cellules)
            date_jour.append(datetime.datetime.now())
            fin_partie()
       #vérifie toutes les créature vivante pour compter leurs nombres de voisins et les change en rouge si elles vont mourrir
       for x in range (20) :
            for y in range (20) :
                voisins = 0
                if grille[x][y] == 1 :

                    if x != 0 and y != 0 :
                        if grille[x-1][y-1] == 1 :
                            voisins = voisins + 1

                    if y != 0 :
                        if grille[x][y-1] == 1 :
                            voisins = voisins + 1

                    if y != 0 and x != 19:
                        if grille[x+1][y-1] == 1 :
                            voisins = voisins + 1

                    if x != 0 :
                        if grille[x-1][y] == 1 :
                            voisins = voisins + 1

                    if x != 19 :
                        if grille[x+1][y] == 1 :
                            voisins = voisins + 1

                    if x != 0 and y != 19:
                        if grille[x-1][y+1] == 1 :
                            voisins = voisins + 1

                    if y != 19 :
                        if grille[x][y+1] == 1 :
                            voisins = voisins + 1

                    if x != 19 and y != 19 :
                        if grille[x+1][y+1] == 1 :
                            voisins = voisins + 1

                    if voisins != 2 and voisins != 3 :
                        dessiner_creature(x,y,2)

       Zone.update ()
   #message d'erreur si la saisie est activé ou que la partie est finie
   else :
        print("état de jeu invalide.")

#dessine ou efface les créature en fonction de la colonne; ligne et de leur état (morte, vivante, naissante, mourante)
def dessiner_creature(li, col, état):
    if état == 0 :
        Zone.create_oval(col*30+102 , li*30 + 2 , col*30+100 +27 , li*30+27 ,width=2 ,outline="grey",fill="grey")
    if état == 1 :
        Zone.create_oval(col*30+102 , li*30 + 2 , col*30+100 +27 , li*30+27 ,width=2 ,outline="yellow",fill="yellow")
    if état == 2 :
        Zone.create_oval(col*30+102 , li*30 + 2 , col*30+100 +27 , li*30+27 ,width=2 ,outline="red",fill="red")
    if état == 3 :
        Zone.create_oval(col*30+102 , li*30 + 2 , col*30+100 +27 , li*30+27 ,width=2 ,outline="cyan",fill="cyan")
    Zone.update ()


"""PROGRAMME PRINCIPAL"""


# création de la fenêtre graphique
fen=Tk()
fen.geometry ("700x600") # dimensionnement de la fenêtre
fen.title ("Jeu de la vie")
# création d'un canvas
Zone=Canvas(fen,width=700,height=600,bg="grey")
Zone.place(x=0,y=0)

# création de la liste où sont stockés les infos de la grille
grille = [[0] * 20 for i in range(20)]

#appel de la fonction dessin grille
dessin_grille()
valider=Button(fen, text="Valider",command=validation_du_jeu)
valider.place(x=0, y=0)

suivant=Button(fen, text="jour suivant",command=jour_suivant)
suivant.place(x=0, y=200)

suivant=Button(fen, text="finir la partie",command=fin_partie)
suivant.place(x=0, y=400)

fen.bind('<Button-1>',coordonnees)

fen.mainloop()