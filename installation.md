# Installation SNISI

## Pré-requis

* Ubuntu 14.04.x server LTS fonctionnelle avec accès à Internet.
* Dump récent de la base de données SNISI.

## Création utilisateur SNISI

* `# useradd -m -g www-data -G cdrom,dip,plugdev,lpadmin,sambashare,adm -N -s /bin/bash snisi`
* Mise en place d'un mot de passe (temporaire)
* `# passwd snisi`
* Installer votre clé SSH via `ssh-copy-id`.
* suppression du mot de passe de l'utilisateur
* `# passwd -d snisi`

## Installation des dépendances

* Dépendances systèmes (paquets)
* `# apt-get install build-essential python-dev make mariadb-client nginx git-core sqlite3 tig traceroute unzip libmariadbclient-dev libmysqlclient18 libssl-dev libmagic1`
* `# apt-get install mariadb-server` choisir le mot de passe root pour MariaDB
* `# apt-get install postfix` choisir «site internet» et votre nom de domaine
* Dépendances python
* `# easy_install pip`
* `# pip install -U pip circus pew`
* `# locale-gen fr_FR.UTF-8`

## Base de données
* Création utilisateur `snisi/snisi` et base de données `snisi` dans MariaDB (MySQL)
* `# echo "grant all privileges on snisi.* to 'snisi'@'localhost' identified by 'snisi' with grant option; flush privileges; create database snisi;" | mysql -uroot -p` renseigner le mot de passe root de MariaDB
* Copie du dump depuis votre machine vers le serveur
* `$ scp snisi_2016-03-27-auto.sql.bz2 root@serveur:`
* Extraction du dump
* `# bunzip2 snisi_2015-01-01-auto.sql.bz2`
* Import du dump
* `# mysql -usnisi -psnisi snisi < snisi_2011-01-01-auto.sql`

## Démon SNISI
* créer le fichier `/etc/circus.conf`

```
[circus]
statsd = 0
httpd = 0

[watcher:snisiworker]
working_dir = /home/snisi/snisi
cmd = /home/snisi/.local/share/virtualenvs/snisi-env/bin/chaussette --backend tornado --fd $(circus.sockets.snisiapp) snisi.wsgi.application
numprocesses = 6
use_sockets = True
uid = snisi
gid = www-data

[socket:snisiapp]
host = 0.0.0.0
port = 8888

[env:snisiworker]
PYTHONPATH = /home/snisi/.local/share/virtualenvs/snisi-env
LANG = fr_FR.UTF-8
```
* créér le fichier `/etc/init/circus.conf`

```
description "circus daemon"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
exec /usr/local/bin/circusd --daemon /etc/circus.ini
```

## Configuration nginx
* créer le fichier `/etc/nginx/sites-enabled/snisi`.
* /!\ Modifier ici le `server_name`.

```
	server {
		listen 80;
	        server_name  test.snisi.sante.gov.ml;
	        charset utf-8;

		location /favicon.ico {
			alias /home/snisi/snisi/static/img/favicon.ico;
			expires max;
		}

		location /resources {
		    alias /home/snisi/resources/;
			autoindex on;
		}

		location /protected/ {
	        	expires max;
	        	root /home/snisi/snisi/;
			internal;
		}

		location /static {
	        	if ($query_string) {
	            		expires max;
	        	}
	    		alias /home/snisi/snisi/static/;
	    		autoindex on;
	    	}

	        location / {
		        root /home/snisi/snisi;
	                index index.html index.htm;
	                proxy_pass              http://127.0.0.1:8888;
	                proxy_set_header        X-Real-IP  $remote_addr;
	        }
	}
```

## Déploiement du code (utilisateur SNISI)

* Création de l'environnement
* `$ pew new -a /home/snisi/snisi snisi-env`
* Modification (ajout à la fin) du fichier `.bashrc` (optionnel)

```
	export EDITOR="vim -v"

	function color_my_prompt {
	    local __user_and_host="\[\033[01;32m\]\u@\h"
	    local __cur_location="\[\033[01;34m\]\w"
	    local __git_branch_color="\[\033[31m\]"
	    #local __git_branch="\`ruby -e \"print (%x{git branch 2> /dev/null}.grep(/^\*/).first || '').gsub(/^\* (.+)$/, '(\1) ')\"\`"
	    local __git_branch='`git branch 2> /dev/null | grep -e ^* | sed -E  s/^\\\\\*\ \(.+\)$/\(\\\\\1\)\ /`'
	    local __prompt_tail="\[\033[35m\]$"
	    local __last_color="\[\033[00m\]"
	    export PS1="$__user_and_host $__cur_location $__git_branch_color$__git_branch$__prompt_tail$__last_color "
	}
	color_my_prompt

	if [ "${VIRTUAL_ENV}a" != "a" ]
	then
		export PS1="(\$(basename '$VIRTUAL_ENV'))$PS1";
	else
	    pew workon snisi-env
	fi
```

### Dépendances python
* `$ pip install circus tornado chaussette`
* Copie du code
* `$ git clone https://github.com/yeleman/snisi.git`
* Déplacement dans dossier `snisi`
* `$ cd snisi`
* Dépendances python
* `$ pip install -r requirements.pip`
* Création dossier
* `$ mkdir -p ~/resources`
* Création du fichier `/home/snisi/snisi/snisi/settings_local.py`

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

import os
SNISI_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SNISI_DIR)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (,)

DATABASES = {'default': {'NAME': 'snisi',
                         'ENGINE': 'django.db.backends.mysql',
                         'CONN_MAX_AGE': 0,
                         'USER': 'snisi',
                         'PASSWORD': 'snisi',
                         'HOST': 'localhost',
                        }
}
TIME_ZONE = 'Africa/Bamako'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
STATIC_URL = '/static/'
SECRET_KEY = 'hop hop'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SENDER = "ANTIM <antim@sante.gov.ml>"
HOTLINE_NUMBER = "76104025"
HOTLINE_EMAIL = "antim@sante.gov.ml"
SUPPORT_CONTACTS = {
    'antim': {'name': "ANTIM", 'email': "antim@sante.gov.ml", 'phone': HOTLINE_NUMBER},
    'pnlp': {'name': "PNLP", 'email': "groupepnlp@sante.gov.ml"},
    'pnlc': {'name': "PNLC", 'email': "groupepnlp@sante.gov.ml"},
}
USE_HTTPS = False
COUNTRY_PREFIX = 223
ORANGE = 'orange'
MALITEL = 'malitel'
FOREIGN = 'foreign'
OPERATORS = {ORANGE: ("Orange MALI", [7, 9, 4, 8, 90, 91]),
             MALITEL: ("Malitel", [2, 6, 98, 99]),
             FOREIGN: ("Extérieur", [])}
FONDA_INCOMING_NUMBERS = ['70062552']
SMS_CONVERT_UNICODE_TO_ASCII = True
SERVE_PROTECTED_FILES = False
FLOTTE_ONLY_NOTIFICATIONS = True
```

## Lancement
* `# start circus`
* `# nginx -s reload`

## Tâches régulières
Les *cron jobs* ne sont pas nécessaires pour le développement ou les tests.

```
# m h  dom mon dow   command

# create expected reportings on period starts
# we launch them all everyday even though it's only need on the day
# the period starts.
# allows us to automaticaly recover from black-out day.
# script is responsible for not creating duplicates.
0 4 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t MonthPeriod
30 4 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t DayPeriod
40 4 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t FixedMonthFirstWeek
45 4 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t FixedMonthSecondWeek
50 4 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t FixedMonthThirdWeek
55 4 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t FixedMonthFourthWeek
0 5 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py create-expected-reporting -d previous -t FixedMonthFifthWeek

# daily check-ups
# this script will call every projects's daily checkups.
0 6 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py daily-checkups

# Fire notifications for quickly
0 8 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py fire-notifications -t quickly
0 12 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py fire-notifications -t quickly
0 17 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py fire-notifications -t today
0 9 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py fire-notifications -t soon
0 10 * * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py fire-notifications -t later


# Backup DB to jigine
30 23 * * * /home/snisi/daily_backup.sh


0 4 16 * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py export_all_malariar_xls -p /home/snisi/snisi/protected/malaria/all_malariar.xls
0 4 1,4,11,17,24 * * /home/snisi/.local/share/virtualenvs/snisi-env/bin/python /home/snisi/snisi/manage.py export_all_dailymalariar_xls -p /home/snisi/snisi/protected/malaria/all_dailymalariar.xls

```
