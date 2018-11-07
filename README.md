# Installation
```
python3.7 -m venv env
source env/bin/activate
pip install -r requirements.txt
``` 

# Utilisation
Il faut d'abord configurer un fichier `config.cfg`. Un exemple de configuration, `config_example.cfg` est fourni. 

La section `[general]` du fichier de configuration contient les informations pour les logs et pour l'envoie de
courriels. 

Toutes les autres sections ont comme titre l'adresse d'une page à analyser. Si le contenu des balises `<p>` de cette
page contient l'un ou l'autre des expressions régulières listées à l'option `patterns` de la section, une erreur est
loggée. Les patterns sont séparés par des virgules.

Pour lancer l'analyse, il suffit d'exécuter
`python monitor_vdq.py`

