# Roleplaying Scripts
This repo contains programs i have used to aid me in rolling dice while playing Dungeons and Dragons, as of writing this i have only made scripts for the wizard class.

## wizard scripts
There are two scripts for necromancy wizard, the old script in wizard/old/ and the new in wizard/

The new script is tested and works in both windows and linux but there are a few requirements to run it
* have mysql installed
* have a user in mysql
* the user follows the pattern of user@"ip or domain using the script from" on the mysql database
* have tkinter and mysql python packages installed

Install script is still WIP

Here are the steps to install mysql in Linux and relevant database and tables, you can use mysql workbench to use the sql scripts under wizard/sql to do this
I will use $ to indicate shell commands and # to indicate the mysql cli, your choice of entry is written in <>
```shell
$ sudo systemctl enable --now mysql
$ sudo mysql
# create user <your username, save for config>@<ip or domain connecting to database> identified by <password, save for config>;
# grant all on *.* to <your username>@<ip>;
# flush privileges;
# create database dnd;
# use dnd;
# create table summons(id int not null, creature_type tinytext, health int not null, hit_modifier int not null, damage_modifier int not null, permanent boolean not null);
# exit
```
Now your mysql database should be running at port 3306 at the ip of the device running it, this will be your host and port prompted by the necromancy script, the password and username created before will also be entered here.
