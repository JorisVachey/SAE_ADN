# Modèle Logique de Données

### Clef Primaire : <span style="color:red">rouge</span>
### Clef Étrangère : \#
<br>

- LABORATOIRE [<span style="color:red">nomLab</span>, adresse, budget]

- PLATEFORMEFOUILLE [<span style="color:red">nomPlat</span>, nbPers, coutJournal, interMaint, dernMaint, #nomLab]

- EQUIPEMENT [<span style="color:red">idE</span>, nomE]

- CONTENIR [#<span style="color:red">idE</span>, #<span style="color:red">nomPlat</span>]

- HABILITATION [<span style="color:red">typeHab</span>]

- NECESSITER [#<span style="color:red">nomPlat</span>, #<span style="color:red">typeHab</span>]

- PERSONNE [<span style="color:red">idPers</span>, nom, prenom, poste]

- POSEDER [#<span style="color:red">idPers</span>, #<span style="color:red">typeHab</span>]

- PARTICIPER [#<span style="color:red">idPers</span>, #<span style="color:red">numCamp</span>]

- LIEU [<span style="color:red">nomL</span>]

- CAMPAGNEFOUILLE [<span style="color:red">numCamp</span>, dateCamp, duree, #nomPlat, #nomL]

- FICHIER [<span style="color:red">idFichier</span>, #numEchant]

- ECHANTILLON [<span style="color:red">numEchant</span>, espece, commentaire, #numCampagne, #idFichier, #idPers]