# tartempion

Un projet vide juste pour montrer comment structurer un projet en python.

## Comment structurer un projet Python

**Par Julien Castiaux**

Host par [Not a Hub](https://hub.notaname.fr/langages/python/comment-structurer-un-projet-python)

## Comment générer une documentation avec sphinx

### Quelques ajouts au projet

L'installation de sphinx est détaillé [ici](https://www.sphinx-doc.org/en/master/usage/installation.html).
Je vais synthétiser et réduire les instructions au strict nécessaire pour notre projet.

Nous allons ajouter sphinx dans une liste de dépendances optionnelles dans notre  `pyproject.toml`.
Ainsi, elles ne seront pas installées par un utilisateur, mais uniquement par les personnes le souhaitant.
Pour ce faire on ajoute simplement au fichier `pyproject.toml` :
```toml
[project.optional-dependencies]
doc = ["sphinx"]
```
Le champ `[project.optional-dependencies]` est défini par la [PyPa](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#dependencies-optional-dependencies).
Ce champ permet d'associer à des clés une liste de dépendances (ici `doc = ["sphinx"]`) qu'un utilisateur pourra installer avec la syntaxe :
```bash
python3 -m pip install tartempion[doc]
```
Où, tartempion est le nom de notre module et entre crochets l'ensemble des clés dont on veut installer les dépendances optionnelles (ici doc).

Si vous avez déjà crée un environement virtuel en ayant suivit le [tuto précédent](https://hub.notaname.fr/langages/python/comment-structurer-un-projet-python), je vous invite a installer tartempion avec la commande suivante :
```bash
source venv/bin/activate
python -m pip install -e .[doc]
```
Pour rappel `.` ici représente notre module tartempion et `-e` permet d'installer le module en mode éditable. Nous allons faire des modifications du code de tartempion, il est donc nécessaire de l'installer comme ça pour ne pas avoir à réinstaller à chaque modification.

### Sphinx quick start en ligne de commande

Une fois sphinx installé dans votre environnement virtuel, il vous fournira la commande `sphinx-quickstart`, la meilleure manière de déployer une documentation, son fonctionnement est détaillé [ici](https://www.sphinx-doc.org/en/master/usage/quickstart.html#getting-started).
Pour séparer la documentation du reste, nous allons juste créer un sous-dossier.
```bash
mkdir doc
```

Ensuite, simplement utiliser :
```bash
sphinx-quickstart doc
```
Vous serez accueilli par un prompt qui va vous demander plusieurs choses.
```
> Separate source and build directories (y/n) [n]: y
> Project name: tartempion
> Author name(s): bob
> Project release []: 0.0.1
> Project language [en]: en
```
Le premier, si vous entrez `y`, deux dossiers `build` et `source` seront créés dans le dossier doc.
Cela évite d'avoir les fichiers générés par sphinx mélangés à ceux que l'on va éditer.
Les trois suivants sont évidents, mais sphinx ne peut pas récupérer ces informations depuis notre `pyproject.toml`.
Enfin, le dernier est utile si vous souhaitez supporter plusieurs langues dans votre documentation, pour l'instant pas touche.

Après avoir lancé la commande, le dossier doc aura la structure suivante :
```bash
doc
|-- Makefile
|-- build
|-- make.bat
`-- source
    |-- _static
    |-- _templates
    |-- conf.py
    `-- index.rst
```
Les fichiers `Makefile` et `make.bat` fournissent des utilitaires pour build la documentation avec la commande `make html`.
Je détaillerai plus tard comment faire.

Le dossier `build` va contenir des fichiers auto-générés, on n'y touchera jamais.
Et les `source` contiennent toute la structure et le contenu de notre documentation.

`conf.py` est la configuration de la doc (l'équivalent de pyproject.toml), nous ne le modifierons qu'une fois lors de ce tuto.

Et `index.rst`...


### Ecriture de la documentation

Maintenant, nous allons écrire de la documentation, l'activité favorite de tout développeur qui se respecte.

Ouvrons le fichier `doc/source/index.rst`, la base de notre documentation.
Ce fichier contient de base :
```rst
.. tartempion documentation master file, created by
   sphinx-quickstart on Sat Aug  3 19:26:31 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tartempion documentation
========================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
```
Les premières lignes avant `tartempion documentation` est un commentaire, vous pouvez le laisser ou le supprimer, je vais le supprimer pour des raisons de lisibilité.
Les trois lignes suivantes vous donnent le lien vers la documentation de la syntaxe utilisée par sphinx pour la documentation.
Je vous invite à la lire après avoir suivi ce tuto. Nous n'utiliserons que quelques-unes de ces fonctionnalités uniquement.
En revanche, si vous devez écrire une documentation, vous aurez besoin d'autres fonctionnalités.
Nous allons le remplacer par la description suivante :
```
La documentation presque vide d'un projet vide juste pour montrer comment créer une docuemntation avec sphinx.
```

Pour build la documentation :
```bash
cd doc
make html
```
Vous pouvez voir votre doc en ouvrant dans un navigateur le fichier `doc/build/html/index.html`
Simple non ?

Maintenant, on va ajouter du contenu et donc jouer avec le `.. toctree::`
Le toctree permet de créer la structure de notre documentation.
On va donc essayer d'ajouter une partie `User Guide` qui expliquera le fonctionnement de notre package.
Pour ce faire, il suffit de créer un fichier `user_guide.rst` à côté de l'index avec le contenu :
```rst
User Guide
==========

Faire des tartes, c'est avant tout de la pratique, après avoir brûlé deux ou trois fours, vous saurez comment faire ;)
```
Modifiez ensuite le toctree pour qu'il ressemble à ça :
```rst
.. toctree::
	:maxdepth: 2
	:caption: Contents:

	user_guide
```
Relancez `make html` et vous verrez apparaitre le champ `User Guide` dans la doc.
Sphinx a ajouté une section User Guide à la structure de la documentation et y a inclus le contenu du fichier `user_guide.rst`

Attention, la syntaxe de rst est capricieuse, n'oubliez pas la ligne vide dans le `toctree`, le titre dans le fichier `user_guide.rst` (l'extension des fichiers dans le toctree n'est pas nécessaire).

### Génération automatique de documentation

Je dis bien générer, car même si on pouvait écrire toute la doc en rst, il est plus intéressant de laisser sphinx générer des fichiers rst à partir des docstring que l'on écrira pour nos class.

Tout d'abord, il faut configurer sphinx pour qu'il active son module permettant de générer la doc.
Pour cela, il suffit de modifier `conf.py` en ajoutant `"sphinx.ext.autodoc"` aux `extensions`.
```python
extensions = ["sphinx.ext.autodoc"]
```

Ensuite, on va créer un fichier api_doc.rst à coté de l'index qui contient :
```
Api
===
```
et l'ajouter au toctree.
Vous pouvez vérifier qu'il s'ajoute bien avec un `make html`.

Ajoutons plutôt tout de suite la doc de notre module:
```python
# tartes/__init__.py
"""
Une collection de tartes délicieuse.
"""

from tartempion.tartes.tarte import Tarte
from tartempion.tartes.tarte_cerise import TarteCerise
from tartempion.tartes.tarte_pomme import TartePomme

__all__ = ["Tarte", "TarteCerise", "TartePomme"]

# tartes/tarte.py
class Tarte:
    """
    C'est triste une tarte sans gout.
    """

# tartes/tarte_cerise.py
from tartempion.tartes.tarte import Tarte


class TarteCerise(Tarte):
    """
    Je préfère les pommes.
    """

# tartes/tarte_pomme.py
from tartempion.tartes.tarte import Tarte


class TartePomme(Tarte):
    """
    Tarte au pomme ça reste le meilleur.
    """
```
Et le contenue de `api_doc.rst` :
```rst
Api
===

.. automodule:: tartempion.tartes

.. autoclass:: tartempion.tartes.Tarte
.. autoclass:: tartempion.tartes.TarteCerise
.. autoclass:: tartempion.tartes.TartePomme```
```
Les instructions `automodule` et `autoclass` vont générer de la doc automatiquement en se basant sur le contenue en doctring des fichiers python.