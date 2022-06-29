from json import loads
from csv import reader


def generate_insertion(table_name, attributes, values):
    attrs = "(" + ", ".join(attributes) + ")"
    vals = "(" + ", ".join([f"'{v}'" for v in values]) + ")"
    query = f"Insert into {table_name} {attrs} values {vals};\n"
    return query


def insert_joueurs_jouerA_postes():
    global w, clubs
    w.write("\n\n/*  Joueurs  */\n")
    id_joueur = 1
    postes = []
    poste_queries = []
    jouerA_queries = []
    id_poste = 1
    for club in clubs:
        for joueur in club["joueurs"]:
            nom_complet = joueur["nom"].replace("'", "").split(" ")
            nom = nom_complet[0]
            prenom = " ".join(nom_complet[1:])
            q_joueur = generate_insertion(
                "Joueur", ["IdJoueur", "NomJoueur", "PrenomJoueur"], [id_joueur, nom, prenom]
            )
            if joueur["poste"] not in postes:
                postes.append(joueur["poste"])
                q_poste = generate_insertion(
                    "Poste", ["IdPoste", "DescriptionPoste"], [id_poste, joueur["poste"]]
                )
                poste_queries.append(q_poste)
                id_poste += 1

            q_jouerA = generate_insertion(
                "JouerA",
                ["IdJoueur", "IdPoste", "Sigle"],
                [id_joueur, postes.index(joueur["poste"]) + 1, club["equipe"]],
            )
            jouerA_queries.append(q_jouerA)
            w.write(q_joueur)
            id_joueur += 1

    w.write("\n\n/*  Postes  */\n")
    for q in poste_queries:
        w.write(q)

    w.write("\n\n/*  JouerA  */\n")
    for q in jouerA_queries:
        w.write(q)


def insert_wilayas():
    global w
    w.write("\n\n/*  Wilayas  */\n")
    q = generate_insertion("Wilaya", ["IdWilaya", "NomWilaya"], ["1", "Alger"])
    w.write(q)


def insert_divisions():
    global w
    w.write("\n\n/*  Divisions  */\n")
    q = generate_insertion("Division", ["IdDivision", "NomDivision"], ["1", "Honneur"])
    w.write(q)


def insert_stades():
    global w, clubs
    w.write("\n\n/*  Stades  */\n")
    id = 1
    for club in clubs:
        q = generate_insertion(
            "Stade", ["IdStade", "NomStade", "IdWilaya"], [id, club["Stade"], "1"]
        )
        w.write(q)
        id += 1


def insert_groupes():
    global w
    w.write("\n\n/*  Groupes  */\n")
    for i in range(1, 4):
        q = generate_insertion("Groupe", ["IdDivision", "NumGroupe"], ["1", str(i)])
        w.write(q)


def insert_equipes():
    global w, clubs
    w.write("\n\n/*  Equipes  */\n")

    attrs = (
        "("
        + ", ".join(
            [
                "Sigle",
                "NomEqu",
                "Date_Fondation",
                "IdWilaya",
                "IdDivision",
                "NumGroupe",
                "IdStade",
            ]
        )
        + ")"
    )
    for club in clubs:
        values = [
            f'\'{club["equipe"]}\'',
            f'\'{club["Nom_complet"]}\'',
            f'\'{club["Fondation"]}-01-01\'',
            "'1'",
            "'1'",
            "'1'",
        ]

        vals = f'SELECT {", ".join([v for v in values])}, Case when exists(select * from Stade where NomStade=\'{club["Stade"]}\') then IdStade else NULL end from Stade  limit 1'
        q = f"Insert into Equipe {attrs} {vals};\n"
        w.write(q)


def insert_saisons():
    global w
    w.write("\n\n/*  Saison  */\n")
    q = generate_insertion(
        "Saison", ["Saison", "DateDebut", "DateFin"], ["1", "2021-11-30", "2022-05-29"]
    )
    w.write(q)


def insert_journees():
    global w
    w.write("\n\n/*  Journees  */\n")
    for i in range(1, 27):
        q = generate_insertion("Journee", ["Saison", "NumJournee"], ["1", str(i)])
        w.write(q)


def insert_rencontres_Joue_marquer():
    global w, rencontres
    w.write("\n\n/*  Rencontres  */\n")
    id_rencontre = 1
    Joue_queries = []
    marquer_queries = []
    for journee in rencontres["journees"]:
        for rencontre in journee["rencontres"]:
            # rencontre
            attrs = (
                "("
                + ", ".join(["IdRencontre", "Saison", "NumJournee", "IdStade"])
                + ")"
            )
            values = [
                f"'{id_rencontre}'",
                f"'1'",
                f'\'{journee["num"]}\''
            ]
            vals = f'SELECT {", ".join([v for v in values])}, Case when exists(select * from Stade  where NomStade=\'{rencontre["Lieu"]}\') then IdStade else NULL end from Stade  limit 1'
            q_rencontres = f"Insert into Rencontre {attrs} {vals};\n"
            w.write(q_rencontres)

            # Joue
            sigleA, sigleB = rencontre["Rencontre"].split(" - ")
            ScoreEquipeA, ScoreEquipeB = rencontre["score"].split(" : ")
            q_Joue = generate_insertion(
                "Joue",
                ["SigleA", "SigleB", "IdRencontre", "ScoreEquipeA", "ScoreEquipeB"],
                [sigleA, sigleB, id_rencontre, ScoreEquipeA, ScoreEquipeB],
            )
            Joue_queries.append(q_Joue)

            # Marquer
            for but in rencontre["buts"]:
                nom_complet = but["joueur"].replace("'", "").split(" ")
                nom = nom_complet[0]
                prenom = nom_complet[1]
                attrs = "(" + ", ".join(["Idrencontre", "minuteBut", "Idjoueur"]) + ")"
                values = [
                    f"'{id_rencontre}'",
                    f'\'{but["minute"]}\''
                ]
                vals = f'SELECT {", ".join([v for v in values])}, IdJoueur from Joueur where ((NomJoueur LIKE \'%{nom}%\')AND (PrenomJoueur LIKE \'%{prenom}%\')) limit 1'
                q_marquer = f"Insert into Marquer {attrs} {vals};\n"
                marquer_queries.append(q_marquer)

            id_rencontre += 1

    w.write("\n\n/*  Joue  */\n")
    for q in Joue_queries:
        w.write(q)

    w.write("\n\n/*  Marquer  */\n")
    for q in marquer_queries:
        w.write(q)


def insert_presidents_club():
    global w, clubs
    w.write("\n\n/*  Presidents Club  */\n")
    id = 1
    for club in clubs:
        nom_complet = club["Président"].replace("'", "").split(" ")
        nom = nom_complet[0]
        prenom = " ".join(nom_complet[1:])
        q = generate_insertion(
            "President_Club",
            ["IdPresident", "NomPresident", "PrenomPresident"],
            [id, nom, prenom],
        )
        w.write(q)
        id += 1


def insert_arbitres():
    global w
    w.write("\n\n/*  Arbitres  */\n")
    id = 1
    with open("arbitres.csv", "r") as read_obj:
        csv_reader = list(reader(read_obj))
        header = csv_reader[0]
        csv_reader.pop(0)
        for row in csv_reader:
            d = {}
            for i, elt in enumerate(row):
                d[header[i]] = elt
            # print(d);input()

            q = generate_insertion(
                "Arbitre",
                ["IdArbitre", "NomArbitre", "PrenomArbitre"],
                [id, d["Nom"], d["Prenom"]],
            )
            w.write(q)
            id += 1


if __name__ == "__main__":
    clubs = loads(open("clubs.json").read())
    rencontres = loads(open("rencontres.json").read())

    with open("insertions.sql", "w") as w:
        # Wilayas (alger)
        insert_wilayas()

        # Division (Honneur)
        insert_divisions()

        # saison (2021-2022)
        insert_saisons()

        # journees
        insert_journees()

        # Stades
        insert_stades()

        # groupes (1,2,3)
        insert_groupes()

        # equipes
        insert_equipes()

        # Joueurs et JouerA et postes
        insert_joueurs_jouerA_postes()

        # rencontres et Joue et marquer
        insert_rencontres_Joue_marquer()

        # Arbitres
        insert_arbitres()
