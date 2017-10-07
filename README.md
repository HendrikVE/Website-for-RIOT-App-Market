# RIOT App Market website

## What you need:
* Apache2 Webserver with python enabled ([follow this guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-apache-mysql-and-python-lamp-server-without-frameworks-on-ubuntu-14-04))

[Bootswatch Cyborg](https://bootswatch.com/cyborg/)

## Setup
0. Important to notice: Please run every command with 'sudo -u www-data'
1. copy config/db_config_EXAMPLES.py and rename the copy to db_config.py
2. change password in config/db_config.py to the password you set by creating user 'riotam-website'