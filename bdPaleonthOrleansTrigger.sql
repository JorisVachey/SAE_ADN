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
        where nomPlat = NEW.nomPlat and dateCamp <= NEW.dateCamp + NEW.duree - 1
        and dateCamp + duree - 1 >= NEW.dateCamp
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