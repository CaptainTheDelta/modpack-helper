# Modpack generator for dummies

Modder son instance minecraft, ça a toujours été un plaisir.

Seulement, les (faibles) efforts demandés peuvent arrêter les néophytes.

Dans l'objectif de partager ce plaisir, il est nécessaire de réduire au minimum les tâches répétitives.

Mais comment ?

### Côté experimenté :
1. en sélectionnant une liste de mods disponibles sur [Modrinth](https://modrinth.com/discover/mods) sous la forme suivante :
```yaml
infos:
  author: CaptainTheDelta
  version: 0.3.1
  mc_version: 1.21.11
  name: Together

mods:
  Catégorie:
    mod-sans-description:
    mod-avec-description:
      desc: En une ligne
      env: [singleplayer, server-side]
    autre-mod:
      desc: |
        Description en deux lignes.
        Et oui.
```
2. en hébergeant ce projet

### côté néophyte
1. via ce projet, cocher les mods interessants ;
2. générer le modpack [packwiz](https://packwiz.infra.link/) et noter l'url
3. renseigner l'url dans l'instance [MultiMC](https://multimc.org/)


## ToDo
- [x] PoC
- [x] refactor & clean
- [ ] préparer instance [MultiMC](https://multimc.org/) à laquelle sera ajoutée [packwiz-installer](https://packwiz.infra.link/tutorials/installing/packwiz-installer/)
- [ ] traduire en anglais
- [ ] Déployer avec [Gunicorn](https://gunicorn.org/) dans un container
- [x] trouver une licence correcte

## Fonctionnalités à ajouter
- [ ] Gestion modpack pour serveur
- [ ] Ajouter de la capture d'erreurs ?
- [ ] hash pour modpacks identiques
- [x] infos modpack dans la liste de mods (auteur, mc_version, etc)
- [ ] URL personnalisées
- [ ] multiples listes de mods ?
- [ ] outil d'aide à la création de liste
- [ ] traduction/personnalisation des descriptions
- [ ] affichage d'une config depuis un token
- [ ] affichage de tous les tokens générés ou personnalisés
- [ ] filtres côté interface utilisateur (version mc, serveur/client, (pas) à jour, etc)
- [ ] tri (par défaut, catégories, nb de téléchargement, MàJ)