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

## Fonctionnalités implémentées
- [x] Gestion de multiples modpacks
- [x] Synchronisation automatisée à la demande
- [x] Sous-sélection de mods
- [ ] Génération d'un modpack packwiz
- [ ] URL personnalisée
- [ ] Profils : Singleplayer, Multiplayer côté client, Multiplayer côté serveur

## Roadmap
1. Sélection
- [x] CSS minimum
- [ ] Media query

2. Generation
- [x] Dossier temporaire
- [ ] Création modpack
- [ ] Ajout des mods

3. Validation
- [ ] Invite
- [ ] Déplacement

4. Partage
- [x] servir le dossier
- [ ] customisation URL

5. Gestion des générés
- [ ] Enregistrement bdd & check avant génération
- [ ] Gestion via interface modpacks

6. Amélioration interface
- [ ] Catégories
- [ ] Licenses
- [ ] Recherche & filtres
- [ ] Profil

### Simplification de la vie utilisateur
- [ ] préparer instance [MultiMC](https://multimc.org/) à laquelle sera ajoutée [packwiz-installer](https://packwiz.infra.link/tutorials/installing/packwiz-installer/)
- [ ] traduire en anglais
- [ ] Déployer avec [Gunicorn](https://gunicorn.org/) dans un container

## Fonctionnalités à ajouter
- [ ] outil d'aide à la création de liste
- [ ] traduction/personnalisation des descriptions
- [ ] affichage d'une config depuis un token
- [ ] filtres côté interface utilisateur (version mc, serveur/client, (pas) à jour, etc)
- [ ] tri (par défaut, catégories, nb de téléchargement, MàJ)