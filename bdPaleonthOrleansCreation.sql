drop table if exists FICHIER;
drop table if exists ECHANTILLON;
drop table if exists PARTICIPER;
drop table if exists POSSEDER;
drop table if exists NECESSITER;
drop table if exists CONTENIR;
drop table if exists HABILITATION;
drop table if exists EQUIPEMENT;
drop table if exists CAMPAGNEFOUILLE;
drop table if exists PLATEFORMEFOUILLE;
drop table if exists PERSONNE;
drop table if exists LIEU;
drop table if exists LABORATOIRE;

create table LABORATOIRE (
    nomLab varchar(100) primary key,
    adresse varchar(255),
    budget float
);

create table PLATEFORMEFOUILLE (
    nomPlat varchar(100) primary key,
    nbPers int,
    coutJournal float,
    interMaint int,
    dernMaint date,
    nomLab varchar(100)
);

create table EQUIPEMENT (
    idE int primary key,
    nomE varchar(100)
);

create table CONTENIR (
    idE int,
    nomPlat varchar(100),
    primary key (idE, nomPlat)
);

create table HABILITATION (
    typeHab ENUM('BIOLOGIQUE','ELECTRIQUE','RADIOACTIVE','CHIMIQUE') primary key
);

create table NECESSITER (
    nomPlat varchar(100),
    typeHab ENUM('BIOLOGIQUE','ELECTRIQUE','RADIOACTIVE','CHIMIQUE'),
    primary key (nomPlat, typeHab)
);

create table PERSONNE (
    idPers int primary key,
    nom varchar(50),
    prenom varchar(50),
    poste varchar(50)
);

create table POSSEDER (
    idPers int,
    typeHab ENUM('BIOLOGIQUE','ELECTRIQUE','RADIOACTIVE','CHIMIQUE'),
    primary key (idPers, typeHab)
);

create table PARTICIPER (
    idPers int,
    numCamp int,
    primary key (idPers, numCamp)
);

create table LIEU (
    nomL varchar(100) primary key
);

create table CAMPAGNEFOUILLE (
    numCamp int primary key,
    dateCamp date,
    duree int,
    nomPlat varchar(100),
    nomL varchar(100)
);

create table ECHANTILLON (
    numEchant int primary key,
    espece varchar(100),
    commentaire text,
    numCampagne int,
    idPers int
);

create table FICHIER (
    idFichier int primary key,
    numEchant int
);

alter table PLATEFORMEFOUILLE add foreign key (nomLab) references LABORATOIRE(nomLab);

alter table CONTENIR add foreign key (idE) references EQUIPEMENT(idE);
alter table CONTENIR add foreign key (nomPlat) references PLATEFORMEFOUILLE(nomPlat);

alter table NECESSITER add foreign key (nomPlat) references PLATEFORMEFOUILLE(nomPlat);
alter table NECESSITER add foreign key (typeHab) references HABILITATION(typeHab);

alter table POSSEDER add foreign key (idPers) references PERSONNE(idPers);
alter table POSSEDER add foreign key (typeHab) references HABILITATION(typeHab);

alter table PARTICIPER add foreign key (idPers) references PERSONNE(idPers);
alter table PARTICIPER add foreign key (numCamp) references CAMPAGNEFOUILLE(numCamp);

alter table CAMPAGNEFOUILLE add foreign key (nomPlat) references PLATEFORMEFOUILLE(nomPlat);
alter table CAMPAGNEFOUILLE add foreign key (nomL) references LIEU(nomL);

alter table FICHIER add foreign key (numEchant) references ECHANTILLON(numEchant);

alter table ECHANTILLON add foreign key (numCampagne) references CAMPAGNEFOUILLE(numCamp);
alter table ECHANTILLON add foreign key (idPers) references PERSONNE(idPers);