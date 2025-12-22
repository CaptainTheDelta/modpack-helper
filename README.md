# Modpack generator for dummies

Modder son instance minecraft, ça a toujours été un plaisir.
Seulement, les (faibles) efforts demandés peuvent arrêter les néophytes.
Dans l'objectif de partager ce plaisir, il est nécessaire de réduire au minimum les tâches répétitives.

Mais comment ?

### Côté experimenté :
1. en sélectionnant une liste de mods disponibles sur [Modrinth](https://modrinth.com/discover/mods) sous la forme suivante :
```
# Minimum
modmenu
no-chat-reports
simple-voice-chat

# Opti & fixes
sodium
sodium-extra
reeses-sodium-options
```
2. en hébergeant ce projet

### côté néophyte
1. via ce projet, cocher les mods interessants ;
2. générer le modpack [packwiz](https://packwiz.infra.link/) et noter l'url
3. renseigner l'url dans l'instance [MultiMC](https://multimc.org/)


## ToDo
[x] PoC
[ ] refactor & clean
[ ] préparer instance [MultiMC](https://multimc.org/) à laquelle sera ajoutée [packwiz-installer](https://packwiz.infra.link/tutorials/installing/packwiz-installer/)
[ ] traduire en anglais
[ ] Déployer avec [Gunicorn](https://gunicorn.org/) dans un container
[ ] un chouille plus de CSS ?
[ ] variables d'environnement pour liste de mods, auteur, mc_version...

## Fonctionnalités à ajouter
[ ] Gestion modpack pour serveur
[ ] Ajouter de la capture d'erreurs ?
[ ] hash pour modpacks identiques
[ ] URL personnalisées
[ ] multiples listes de mods ?
[ ] outil d'aide à la création de liste
[ ] traduction/personnalisation des descriptions