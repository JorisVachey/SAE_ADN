-- --------------------------
-- 1. LABORATOIRE
-- --------------------------
insert into LABORATOIRE values ('Lab Orléans', '1 rue des Fossiles', 500000);

-- --------------------------
-- 2. HABILITATIONS
-- --------------------------
insert into HABILITATION values ('BIOLOGIQUE');
insert into HABILITATION values ('ELECTRIQUE');
insert into HABILITATION values ('CHIMIQUE');
insert into HABILITATION values ('RADIOACTIVE');

-- --------------------------
-- 3. LIEUX
-- --------------------------
insert into LIEU values ('Site Orléans');
insert into LIEU values ('Site Tours');

-- --------------------------
-- 4. PLATEFORMES
-- --------------------------
insert into PLATEFORMEFOUILLE values ('Plateforme A', 5, 1000.00, 30, '2025-01-01', 'Lab Orléans');
insert into PLATEFORMEFOUILLE values ('Plateforme B', 3, 800.00, 25, '2025-02-01', 'Lab Orléans');

-- --------------------------
-- 5. HABILITATIONS REQUISES
-- --------------------------
insert into NECESSITER values ('Plateforme A', 'BIOLOGIQUE');
insert into NECESSITER values ('Plateforme A', 'ELECTRIQUE');
insert into NECESSITER values ('Plateforme A', 'CHIMIQUE');

insert into NECESSITER values ('Plateforme B', 'BIOLOGIQUE');
insert into NECESSITER values ('Plateforme B', 'RADIOACTIVE');

-- --------------------------
-- 6. PERSONNES
-- --------------------------
insert into PERSONNE values (1, 'Durand', 'Alice', 'Chercheuse');
insert into PERSONNE values (2, 'Martin', 'Bob', 'Technicien');
insert into PERSONNE values (3, 'Petit', 'Clara', 'Chercheuse');

-- --------------------------
-- 7. HABILITATIONS POSSEDÉES
-- --------------------------
insert into POSSEDER values (1, 'BIOLOGIQUE');
insert into POSSEDER values (1, 'ELECTRIQUE');
insert into POSSEDER values (1, 'CHIMIQUE');
insert into POSSEDER values (1, 'RADIOACTIVE');
insert into POSSEDER values (2, 'BIOLOGIQUE');
insert into POSSEDER values (2, 'ELECTRIQUE');
insert into POSSEDER values (2, 'CHIMIQUE');
insert into POSSEDER values (3, 'BIOLOGIQUE');
insert into POSSEDER values (3, 'RADIOACTIVE');

-- --------------------------
-- 8. CAMPAGNES
-- --------------------------
insert into CAMPAGNEFOUILLE values (1, '2025-01-10', 5, 'Plateforme A', 'Site Orléans');
insert into CAMPAGNEFOUILLE values (2, '2025-01-20', 3, 'Plateforme A', 'Site Orléans');
insert into CAMPAGNEFOUILLE values (3, '2025-01-12', 4, 'Plateforme B', 'Site Tours');

-- --------------------------
-- 9. PARTICIPATION
-- --------------------------
insert into PARTICIPER values (1, 1);
insert into PARTICIPER values (2, 1);
insert into PARTICIPER values (3, 3);



-- Bob (id 2) participe à Plateforme B (nécessite BIOLOGIQUE + RADIOACTIVE)
-- Bob n'a pas RADIOACTIVE
insert into PARTICIPER values (2, 3);
-- ❌ Erreur : PersonnePossedeLesBonnesHabilitations

-- Créer une campagne sur Plateforme A qui chevauche la campagne 1 (10-14 mars)
insert into CAMPAGNEFOUILLE values (4, '2025-01-12', 3, 'Plateforme A', 'Site Orléans');
-- ❌ Erreur : VerifierDisponibilitePlateforme

-- Alice (id 1) participe à une nouvelle campagne (3) qui chevauche sa participation à la campagne 1
insert into PARTICIPER values (1, 3);
-- ❌ Erreur : VerifierDisponibilitePersonne

-- La plateforme nécessite une maintenance avant cette campagne
insert into CAMPAGNEFOUILLE (numCamp, dateCamp, duree, nomPlat, nomL)
values (200, '2025-09-05', 3, 'Plateforme A', 'Site1');
-- ❌ Erreur : VerifierMaintenancePlateforme

-- La plateforme nécessite une maintenance car elle va arriver pendant la camapgnes
insert into CAMPAGNEFOUILLE 
values (300, DATE '2025-01-29', 5, 'Plateforme A', 'Site Orléans');
-- ❌ Erreur : VerifierMaintenancePlateforme