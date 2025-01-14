import tkinter as tk
import random

class Navire:
    def __init__(self, taille, nom):
        self.taille = taille
        self.nom = nom
        self.positions = []
        self.touchees = []

    def est_coule(self):
        return set(self.positions) == set(self.touchees)


class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = [[None for _ in range(taille)] for _ in range(taille)]
        self.navires = []

    def placer_navire(self, navire, x, y, orientation):
        positions = []
        for i in range(navire.taille):
            if orientation == "horizontal":
                if y + i >= self.taille or self.grille[x][y + i]:
                    return False
                positions.append((x, y + i))
            elif orientation == "vertical":
                if x + i >= self.taille or self.grille[x + i][y]:
                    return False
                positions.append((x + i, y))

        for pos in positions:
            self.grille[pos[0]][pos[1]] = navire
        
        navire.positions = positions
        self.navires.append(navire)
        return True

    def retirer_dernier_navire(self):
        if not self.navires:
            return False

        dernier_navire = self.navires.pop()
        for x, y in dernier_navire.positions:
            self.grille[x][y] = None

        return True

    def recevoir_tir(self, x, y):
        if self.grille[x][y] is None:
            return "manque"
        elif isinstance(self.grille[x][y], Navire):
            navire = self.grille[x][y]
            navire.touchees.append((x, y))
            return "touche" if not navire.est_coule() else "coule"


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()


class BatailleNavaleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")

        self.creer_interface()
        self.phase = "placement"
        self.navires_a_placer = [
            (5, "Porte-avions"),
            (4, "Croiseur"),
            (3, "Destroyer"),
            (3, "Destroyer"),
            (2, "Sous-marin"),
            (2, "Sous-marin")
        ]
        self.navire_actuel = 0
        self.orientation = "horizontal"

    def creer_interface(self):
        self.cadre_joueur = tk.Frame(self.root, padx=10, pady=10)
        self.cadre_joueur.pack(side=tk.LEFT, padx=20, pady=20)
        self.cadre_ordinateur = tk.Frame(self.root, padx=10, pady=10)
        self.cadre_ordinateur.pack(side=tk.RIGHT, padx=20, pady=20)

        self.boutons_joueur = []
        self.boutons_ordinateur = []

        self.label_joueur = tk.Label(self.cadre_joueur, text="Grille du Joueur", font=("Helvetica", 12))
        self.label_joueur.grid(row=0, columnspan=10)

        self.label_ordinateur = tk.Label(self.cadre_ordinateur, text="Grille de l'Ordinateur", font=("Helvetica", 12))
        self.label_ordinateur.grid(row=0, columnspan=10)

        for x in range(10):
            ligne_joueur = []
            ligne_ordinateur = []
            for y in range(10):
                bouton_joueur = tk.Button(self.cadre_joueur, width=4, height=2, command=lambda x=x, y=y: self.placer_navire(x, y))
                bouton_joueur.grid(row=x + 1, column=y, padx=5, pady=5, sticky="nsew")
                ligne_joueur.append(bouton_joueur)

                bouton_ordinateur = tk.Button(self.cadre_ordinateur, width=4, height=2, command=lambda x=x, y=y: self.tirer(x, y))
                bouton_ordinateur.grid(row=x + 1, column=y, padx=5, pady=5, sticky="nsew")
                ligne_ordinateur.append(bouton_ordinateur)

            self.boutons_joueur.append(ligne_joueur)
            self.boutons_ordinateur.append(ligne_ordinateur)

        for i in range(10):
            self.cadre_joueur.grid_columnconfigure(i, weight=1)
            self.cadre_joueur.grid_rowconfigure(i, weight=1)
            self.cadre_ordinateur.grid_columnconfigure(i, weight=1)
            self.cadre_ordinateur.grid_rowconfigure(i, weight=1)

        self.cadre_options = tk.Frame(self.root)
        self.cadre_options.pack(side=tk.BOTTOM, pady=10)

        self.bouton_horizontal = tk.Button(self.cadre_options, text="Horizontal", command=self.set_orientation_horizontal)
        self.bouton_horizontal.pack(side=tk.TOP, padx=5, pady=5)

        self.bouton_vertical = tk.Button(self.cadre_options, text="Vertical", command=self.set_orientation_vertical)
        self.bouton_vertical.pack(side=tk.TOP, padx=5, pady=5)

        self.bouton_annuler = tk.Button(self.cadre_options, text="Annuler dernier", command=self.annuler_dernier_navire)
        self.bouton_annuler.pack(side=tk.TOP, padx=5, pady=5)

        self.label_navire = tk.Label(self.cadre_options, text="Placez : Porte-avions (5 cases)")
        self.label_navire.pack(side=tk.LEFT, padx=10)

        self.label_resultat = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.label_resultat.pack(pady=10)

        self.bouton_nouvelle_partie = tk.Button(self.root, text="Nouvelle partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.pack(side=tk.BOTTOM, pady=20)

    def set_orientation_horizontal(self):
        self.orientation = "horizontal"

    def set_orientation_vertical(self):
        self.orientation = "vertical"

    def annuler_dernier_navire(self):
        if self.joueur.plateau.retirer_dernier_navire():
            self.navire_actuel -= 1
            taille, nom = self.navires_a_placer[self.navire_actuel]
            self.label_navire.config(text=f"Placez : {nom} ({taille} cases)")

            for ligne in self.boutons_joueur:
                for bouton in ligne:
                    bouton.configure(bg="SystemButtonFace", state="normal")

            for navire in self.joueur.plateau.navires:
                for pos in navire.positions:
                    self.boutons_joueur[pos[0]][pos[1]].configure(bg="gray")

            if self.navire_actuel < len(self.navires_a_placer):
                taille, nom = self.navires_a_placer[self.navire_actuel]
                self.label_navire.config(text=f"Placez : {nom} ({taille} cases)")

            elif self.navire_actuel == len(self.navires_a_placer):
                self.label_navire.config(text="Placement terminé !")
                self.phase = "jeu"
                self.placer_navires_ordinateur()

    def placer_navire(self, x, y):
        if self.phase != "placement":
            return

        if self.navire_actuel >= len(self.navires_a_placer):
            return

        taille, nom = self.navires_a_placer[self.navire_actuel]
        navire = Navire(taille, nom)
        if self.joueur.plateau.placer_navire(navire, x, y, self.orientation):
            for pos in navire.positions:
                self.boutons_joueur[pos[0]][pos[1]].configure(bg="gray")
            self.navire_actuel += 1

        if self.navire_actuel < len(self.navires_a_placer):
            taille, nom = self.navires_a_placer[self.navire_actuel]
            self.label_navire.config(text=f"Placez : {nom} ({taille} cases)")
        elif self.navire_actuel == len(self.navires_a_placer):
            self.label_navire.config(text="Placement terminé !")
            self.phase = "jeu"
            self.placer_navires_ordinateur()

    def placer_navires_ordinateur(self):
        for taille, nom in [(5, "Porte-avions"), (4, "Croiseur"), (3, "Destroyer"), (3, "Destroyer"), (2, "Sous-marin"), (2, "Sous-marin")]:
            place = False
            while not place:
                x, y = random.randint(0, 9), random.randint(0, 9)
                orientation = random.choice(["horizontal", "vertical"])
                navire = Navire(taille, nom)
                place = self.ordinateur.plateau.placer_navire(navire, x, y, orientation)

    def tirer(self, x, y):
        if self.phase != "jeu":
            return

        resultat = self.ordinateur.plateau.recevoir_tir(x, y)
        if resultat == "manque":
            self.boutons_ordinateur[x][y].configure(bg="blue")
        elif resultat == "touche":
            self.boutons_ordinateur[x][y].configure(bg="red")
        elif resultat == "coule":
            self.boutons_ordinateur[x][y].configure(bg="#8B0000")

        if resultat in ["touche", "coule", "manque"]:
            self.afficher_resultat(resultat)

        if all(navire.est_coule() for navire in self.ordinateur.plateau.navires):
            self.label_resultat.config(text="Vous avez gagné !")
            self.phase = "terminé"
        
        if self.phase != "terminé":
            self.tirer_ordinateur()

    def afficher_resultat(self, resultat):
        if resultat == "manque":
            self.label_resultat.config(text="Coup raté !")
        elif resultat == "touche":
            self.label_resultat.config(text="Touché !")
        elif resultat == "coule":
            self.label_resultat.config(text="Navire coulé !")

    def tirer_ordinateur(self):
        x, y = random.randint(0, 9), random.randint(0, 9)
        while self.boutons_joueur[x][y]['bg'] in ['blue', 'red', '#8B0000']:
            x, y = random.randint(0, 9), random.randint(0, 9)

        resultat = self.joueur.plateau.recevoir_tir(x, y)
        if resultat == "manque":
            self.boutons_joueur[x][y].configure(bg="blue")
        elif resultat == "touche":
            self.boutons_joueur[x][y].configure(bg="red")
        elif resultat == "coule":
            self.boutons_joueur[x][y].configure(bg="#8B0000")

        self.afficher_resultat(resultat)

        if all(navire.est_coule() for navire in self.joueur.plateau.navires):
            self.label_resultat.config(text="L'ordinateur a gagné !")
            self.phase = "terminé"

    def nouvelle_partie(self):
        self.phase = "placement"
        self.navire_actuel = 0
        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")
        self.creer_interface()

root = tk.Tk()
app = BatailleNavaleApp(root)
root.mainloop()
