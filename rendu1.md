<h1 align="center"> <u>SAE ADN</u></h1>
 
<h4>Membres du groupe F :</h4>
<p>Nolan Morain<br> Tifany Meunier<br> Joris Vachey </p>

<h2>MCD</h2>

![Image mcd](/MCD.png)

<h2>Dépendances fonctionnelles</h2>

nomPlateforme |--> nomLab, typeHab

numCampagne |--> nomPlateforme, nomL 

idp |--> typeHab, numCampagne

numEchantillon |--> idP, numCampagne

<h2> Contraintes supplémentaires</h2>

Il faut qu'une personne inscrite sur une campagne possède les habilitations nécessaires sur cette dernière. Nous avons créé un trigger "PersonnePossedeLesBonnesHabilitations" pour vérifier cela.</br>
Dans le trigger nous vérifions que la personne qui sera inscrite dans la plateforme possède le même nombre d'habilitations et les mêmes habilitations que celles de la plateforme.



Pour utiliser une plateforme il faut que celle ci soit disponible c'est à dire qu'elle ne soit pas utilisée dans une autre campagne au moment où nous voulons l'utiliser. Pour vérifier cela nous avons créé un trigger "VerifierDisponibilitePlateforme".</br>
Dans le trigger nous vérifions que la plateforme n'est pas utilisée durant la période à laquelle on veut l'assigner et qu'elle a eu un jour de maintenance avant le début de la nouvelle campagne.


Dans le même principe, une personne ne peut être dans deux campagnes en même temps, nous vérifions donc que ce n'est pas le cas avec le trigger "VerifierDisponibilitePersonne".</br>
Dans le trigger nous vérifions que la personne n'est pas prise durant la période à laquelle on veut l'assigner.


<h2> Maquette</h2>

https://www.canva.com/design/DAGzDYr0IHw/0ENBXZemSIaOBzoxHsP7JQ/edit?utm_content=DAGzDYr0IHw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
