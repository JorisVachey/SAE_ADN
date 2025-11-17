delimiter |
create or replace trigger PersonnePossedeLesBonnesHabilitations before insert on PARTICIPER for each row
begin
    declare nb_requises int;
    declare nb_possedees int;
    
    select  count(*) into nb_requises from NECESSITER
    natural join PLATEFORMEFOUILLE natural join CAMPAGNEFOUILLE 
    where numCamp = NEW.numCamp;

    select count(*) into nb_possedees from POSSEDER
    natural join CAMPAGNEFOUILLE natural join PLATEFORMEFOUILLE natural join NECESSITER
    where idPers = NEW.idPers and numCamp = NEW.numCamp;

    if nb_possedees < nb_requises then
        signal SQLSTATE '45000' 
        set MESSAGE_TEXT = 'Vous ne pouvez mettre que des personnes qui possède les mêmes habilitations que la plateforme de la campagne demmande.';
    end if;
end |
delimiter ;


delimiter |
create or replace trigger VerifierDisponibilitePlateforme before insert on CAMPAGNEFOUILLE for each row
begin
    if exists (
        select 1 from CAMPAGNEFOUILLE 
        where nomPlat = NEW.nomPlat and dateCamp <= (NEW.dateCamp + NEW.duree - 1) + 1
        and (dateCamp + duree - 1) + 1 >= NEW.dateCamp
    ) then
        SIGNAL SQLSTATE '45000' 
        set MESSAGE_TEXT = 'La plateforme est déjà mobilisée sur une autre campagne à cette période';
    end if;
end |
delimiter ;


delimiter |
create or replace trigger VerifierDisponibilitePersonne before insert on PARTICIPER for each row
begin
    declare dateDebut date;
    declare dateFin date;

    select dateCamp, dateCamp + duree - 1 into dateDebut, dateFin
    from CAMPAGNEFOUILLE where numCamp = NEW.numCamp;

    if exists (
        select 1 from PARTICIPER natural join CAMPAGNEFOUILLE
        where idPers = NEW.idPers and dateCamp <= dateFin and dateCamp + duree - 1 >= dateDebut
    ) then
        SIGNAL SQLSTATE '45000' 
        set MESSAGE_TEXT = 'Cette personne est déjà mobilisée sur une autre campagne à cette période';
    end if;
end |
delimiter ;


delimiter |
create or replace trigger VerifierMaintenancePlateforme before insert on CAMPAGNEFOUILLE for each row
begin
    declare derniereMaintenance date;
    declare intervalMaintenance int;

    select dernMaint, interMaint into derniereMaintenance, intervalMaintenance 
    from PLATEFORMEFOUILLE where nomPlat = NEW.nomPlat;

    if NEW.dateCamp > derniereMaintenance + INTERVAL intervalMaintenance DAY then
        SIGNAL SQLSTATE '45000'
        set MESSAGE_TEXT = 'La plateforme nécessite une maintenance avant cette campagne';
    end if;
    if NEW.dateCamp <= derniereMaintenance + INTERVAL intervalMaintenance DAY and
    derniereMaintenance + INTERVAL intervalMaintenance DAY <= NEW.dateCamp + INTERVAL NEW.duree - 1 DAY then
        SIGNAL SQLSTATE '45000'
        set MESSAGE_TEXT = 'La Maintenance de la plateforme arrive pendant la campagne, vous devait
        la faire avant de lancer une nouvelle campagne';
    end if;
END |
delimiter ;


delimiter |
create or replace trigger VerifierSiBudgetSuffisantPourNouvelleCampagne before insert on CAMPAGNEFOUILLE for each row
begin
    declare budgetLabo float;
    declare coutJournalTemp float;
    declare dureeCamp int;
    declare budgetCampagne float;

    select budget into budgetLabo from LABORATOIRE
    where nomLab = (select nomLab from PLATEFORMEFOUILLE where nomPlat = NEW.nomPlat);

    select coutJournal into coutJournalTemp from PLATEFORMEFOUILLE where nomPlat = NEW.nomPlat;

    set dureeCamp = NEW.duree;

    set budgetCampagne = coutJournalTemp * dureeCamp;
    if budgetCampagne > budgetLabo then
        SIGNAL SQLSTATE '45000'
        set MESSAGE_TEXT = 'Le budget nécessaire pour la campagne, dépasse le budget total mensuel du laboratoire';
    else
        set budgetLabo = budgetLabo - budgetCampagne;

        update LABORATOIRE set budget = budgetLabo
        where nomLab = (select nomLab from PLATEFORMEFOUILLE where nomPlat = NEW.nomPlat);
    end if;
END |
delimiter ;


delimiter |
create or replace trigger VerifierSiDateDejaPassé before insert on CAMPAGNEFOUILLE for each row
begin
    if new.datecamp < curdate() then
        signal sqlstate '45000'
        set message_text = 'La date de début de la campagne est déjà passée';
    end if;
end |
delimiter ;