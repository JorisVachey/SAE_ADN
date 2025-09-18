-- Suppression des tables si elles existent déjà (ordre inverse des dépendances)
DROP TABLE IF EXISTS FICHIERS;
DROP TABLE IF EXISTS ECHANTILLONS;
DROP TABLE IF EXISTS CAMPAGNE;
DROP TABLE IF EXISTS PLATEFORME;
DROP TABLE IF EXISTS EQUIPEMENT;
DROP TABLE IF EXISTS PERSONNE;
DROP TABLE IF EXISTS HABILITATION;
DROP TABLE IF EXISTS LIEU;
DROP TABLE IF EXISTS LABORATOIRE;


-- Création des tables
CREATE TABLE IF NOT EXISTS LABORATOIRE (
    nomLab VARCHAR(255) PRIMARY KEY,
    adresse VARCHAR(255),
    budget INT
);

CREATE TABLE IF NOT EXISTS LIEU (
    nomL VARCHAR(255) KEY, 
    typeL VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS HABILITATION (
    typeHab ENUM('Electrique','Chimique','Biologique','Radioactive')
);

CREATE TABLE IF NOT EXISTS PERSONNE (
    idP int PRIMARY KEY,
    nomP VARCHAR(30),
    prenomP VARCHAR(30),
    poste ENUM("Chercheur","Administratif","Technique","Direction"),
    typeHab ENUM('Electrique','Chimique','Biologique','Radioactive'),
    FOREIGN KEY (typeHab) REFERENCES HABILITATION(typeHab)
);

CREATE TABLE IF NOT EXISTS EQUIPEMENT (
    idE INT PRIMARY KEY,
    nomEquipement varchar(255)
);

CREATE TABLE IF NOT EXISTS PLATEFORME (
    nomPlateforme VARCHAR(255),
    nbPersonne int,
    coutJournalier int,
    intervalleMaintenance int,
    derniereMaintenance DATE,
    typeHab ENUM('Electrique','Chimique','Biologique','Radioactive'),
    FOREIGN KEY (typeHab) REFERENCES HABILITATION(typeHab)

);

CREATE TABLE IF NOT EXISTS CAMPAGNE (
    numCampagne int PRIMARY KEY,
    dateDebut DATE,
    duree INT,
     nomL VARCHAR(255),
    FOREIGN KEY (nomL) REFERENCES LIEU(nomL)
);

CREATE TABLE IF NOT EXISTS ECHANTILLONS (
    numEchantillon int,
    espece VARCHAR(255),
    commentaire VARCHAR(500), --un tweet
    FOREIGN KEY (numCampagne) REFERENCES CAMPAGNE(numCampagne),
    FOREIGN KEY (idP) REFERENCES PERSONNE(idP) 
);

CREATE TABLE IF NOT EXISTS FICHIERS (
    idFichier int PRIMARY KEY,
    numEchantillon int,
    FOREIGN KEY (numEchantillon) REFERENCES (numEchantillon) 
);


CREATE TABLE IF NOT EXISTS PARTICIPER (
    idP INT,
    numCampagne INT,
    dateParticipation DATE,
    PRIMARY KEY (idP, numCampagne, dateParticipation),
    FOREIGN KEY (idP) REFERENCES PERSONNE(idP),
    FOREIGN KEY (numCampagne) REFERENCES CAMPAGNE(numCampagne),
    FOREIGN KEY (dateDebut) REFERENCES CAMPAGNE(dateDebut)
);

CREATE TABLE IF NOT EXISTS POSSEDER (
    idP INT,
    typeHab VARCHAR(50),
    PRIMARY KEY (idP, typeHab),
    FOREIGN KEY (idP) REFERENCES PERSONNE(idP),
    FOREIGN KEY (typeHab) REFERENCES HABILITATION(typeHab)
);

CREATE TABLE IF NOT EXISTS CONTENIR (
    idE INT,
    nomPlateforme VARCHAR(255),
    PRIMARY KEY (idE, nomPlateforme),
    FOREIGN KEY (idE) REFERENCES EQUIPEMENT(idE),
    FOREIGN KEY (nomPlateforme) REFERENCES PLATEFORME(nomPlateforme)
);