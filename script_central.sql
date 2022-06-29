CREATE TABLE Region(
   IdRegion INT,
   NomRegion VARCHAR(50),
   PRIMARY KEY(IdRegion)
);


CREATE TABLE Joueur(
   IdJoueur INT,
   NomJoueur VARCHAR(50),
   PrenomJoueur VARCHAR(50),
   Age INT,
   PRIMARY KEY(IdJoueur)
);

CREATE TABLE Entraineur(
   IdEntraineur VARCHAR(50),
   NomEntraineur VARCHAR(50),
   PrenomEntraineur VARCHAR(50),
   PRIMARY KEY(IdEntraineur)
);

CREATE TABLE Saison(
   Saison DATE,
   DateDebut DATE,
   DateFin DATE,
   PRIMARY KEY(Saison)
);

CREATE TABLE Arbitre(
   IdArbitre VARCHAR(50),
   NomArbitre VARCHAR(50),
   PrenomArbitre VARCHAR(50),
   PRIMARY KEY(IdArbitre)
);

CREATE TABLE Wilaya(
   IdWilaya INT,
   Region INT,
   NomWilaya VARCHAR(50),
   PRIMARY KEY(IdWilaya),
   FOREIGN KEY(Region) REFERENCES Region(IdRegion)
);

CREATE TABLE Division(
   IdDivision VARCHAR(50),
   NomDivision VARCHAR(50),
   PRIMARY KEY(IdDivision)
);


CREATE TABLE Journee(
   Saison DATE,
   NumJournee INT,
   DateDebut DATE,
   DateFin VARCHAR(50),
   PRIMARY KEY(Saison, NumJournee),
   FOREIGN KEY(Saison) REFERENCES Saison(Saison)
);

CREATE TABLE Carte(
   idCarte INT,
   typeCarte VARCHAR(50),
   PRIMARY KEY(idCarte)
);

CREATE TABLE President_Club(
   IdPresident INT,
   NomPresident VARCHAR(50) NOT NULL,
   PrenomPresident VARCHAR(50) NOT NULL,
   PRIMARY KEY(IdPresident)
);

CREATE TABLE Poste(
   IdPoste INT,
   DescriptionPoste VARCHAR(50) NOT NULL,
   PRIMARY KEY(IdPoste)
);

CREATE TABLE Stade(
   IdStade VARCHAR(50),
   NomStade VARCHAR(50),
   NbPlace INT,
   IdWilaya INT NOT NULL,
   PRIMARY KEY(IdStade),
   FOREIGN KEY(IdWilaya) REFERENCES Wilaya(IdWilaya)
);

CREATE TABLE Groupe(
   IdDivision VARCHAR(50),
   NumGroupe VARCHAR(50),
   NbEquipe INT,
   PRIMARY KEY(IdDivision, NumGroupe),
   FOREIGN KEY(IdDivision) REFERENCES Division(IdDivision)
);

CREATE TABLE Equipe(
   Sigle VARCHAR(50),
   Colors VARCHAR(68),
   NomEqu VARCHAR(50),
   Date_Fondation DATE NOT NULL,
   Telephone INT,
   Mobile INT,
   FAX INT,
   Adresse VARCHAR(100),
   IdWilaya INT NOT NULL,
   IdDivision VARCHAR(50) NOT NULL,
   NumGroupe VARCHAR(50) NOT NULL,
   IdStade VARCHAR(50),
   PRIMARY KEY(Sigle),
   FOREIGN KEY(IdWilaya) REFERENCES Wilaya(IdWilaya),
   FOREIGN KEY(IdDivision, NumGroupe) REFERENCES Groupe(IdDivision, NumGroupe),
   FOREIGN KEY(IdStade) REFERENCES Stade(IdStade)
);

CREATE TABLE Rencontre(
   IdRencontre VARCHAR(50),
   Date_ DATE,
   Saison DATE NOT NULL,
   NumJournee INT NOT NULL,
   IdStade VARCHAR(50) NOT NULL,
   PRIMARY KEY(IdRencontre),
   FOREIGN KEY(Saison, NumJournee) REFERENCES Journee(Saison, NumJournee),
   FOREIGN KEY(IdStade) REFERENCES Stade(IdStade)
);

CREATE TABLE JouerA(
   IdJoueur INT,
   IdPoste INT,
   DateDebut DATE,
   DateFin DATE,
   Sigle VARCHAR(50) NOT NULL,
   PRIMARY KEY(IdJoueur, IdPoste, DateDebut),
   FOREIGN KEY(IdJoueur) REFERENCES Joueur(IdJoueur),
   FOREIGN KEY(IdPoste) REFERENCES Poste(IdPoste),
   FOREIGN KEY(DateDebut) REFERENCES Date_(DateDebut),
   FOREIGN KEY(Sigle) REFERENCES Equipe(Sigle)
);

CREATE TABLE Entraine(
   IdEntraineur VARCHAR(50),
   DateDebut DATE,
   DateFin DATE,
   Sigle VARCHAR(50) NOT NULL,
   PRIMARY KEY(IdEntraineur, DateDebut),
   FOREIGN KEY(IdEntraineur) REFERENCES Entraineur(IdEntraineur),
   FOREIGN KEY(DateDebut) REFERENCES Date_(DateDebut),
   FOREIGN KEY(Sigle) REFERENCES Equipe(Sigle)
);

CREATE TABLE Joue(
   SigleA VARCHAR(50),
   SigleB VARCHAR(50),		
   IdRencontre VARCHAR(50),
   ScoreEquipeA INT NOT NULL,
   ScoreEquipeB INT NOT NULL,
   PRIMARY KEY(SigleA, SigleB, IdRencontre),
   FOREIGN KEY(SigleA) REFERENCES Equipe(Sigle),
   FOREIGN KEY(SigleB) REFERENCES Equipe(Sigle),
   FOREIGN KEY(IdRencontre) REFERENCES Rencontre(IdRencontre)
);

CREATE TABLE Abitrer(
   IdRencontre VARCHAR(50),
   IdArbitre VARCHAR(50),
   PRIMARY KEY(IdRencontre, IdArbitre),
   FOREIGN KEY(IdRencontre) REFERENCES Rencontre(IdRencontre),
   FOREIGN KEY(IdArbitre) REFERENCES Arbitre(IdArbitre)
);

CREATE TABLE Paricipe(
   IdJoueur INT,
   IdRencontre VARCHAR(50),
   MinEnt TIME,
   MinSor VARCHAR(50),
   PRIMARY KEY(IdJoueur, IdRencontre),
   FOREIGN KEY(IdJoueur) REFERENCES Joueur(IdJoueur),
   FOREIGN KEY(IdRencontre) REFERENCES Rencontre(IdRencontre)
);

CREATE TABLE Marquer(
   IdJoueur INT,
   IdRencontre VARCHAR(50),
   minuteBut TIME NOT NULL,
   PRIMARY KEY(IdJoueur, IdRencontre),
   FOREIGN KEY(IdJoueur) REFERENCES Joueur(IdJoueur),
   FOREIGN KEY(IdRencontre) REFERENCES Rencontre(IdRencontre)
);

CREATE TABLE Attribuer(
   IdJoueur INT,
   IdRencontre VARCHAR(50),
   idCarte INT,
   minuteAttribution TIME NOT NULL,
   PRIMARY KEY(IdJoueur, IdRencontre, idCarte),
   FOREIGN KEY(IdJoueur) REFERENCES Joueur(IdJoueur),
   FOREIGN KEY(IdRencontre) REFERENCES Rencontre(IdRencontre),
   FOREIGN KEY(idCarte) REFERENCES Carte(idCarte)
);

CREATE TABLE Presider(
   Sigle VARCHAR(50),
   DateDebut DATE,
   IdPresident INT,
   DateFin DATE,
   PRIMARY KEY(Sigle, DateDebut, IdPresident),
   FOREIGN KEY(Sigle) REFERENCES Equipe(Sigle),
   FOREIGN KEY(DateDebut) REFERENCES Date_(DateDebut),
   FOREIGN KEY(IdPresident) REFERENCES President_Club(IdPresident)
);
