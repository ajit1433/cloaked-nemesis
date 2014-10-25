#!/usr/bin/python

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging
import requests


class Varnish():
    def __init__(self):
        self.logger = logging.getLogger('Varnish')

    def install_Varnish(self):
        self.logger.info("installing Varnish on system")

        self.logger.info("add varnish repo key")

        r = requests.get("http://repo.varnish-cache.org/debian/GPG-key.txt")
        cmd = "echo \""+r.text+"\" | apt-key add -"
        self.logger.info(cmd)
        a = Popen([cmd], stderr=PIPE, stdout=PIPE, shell=True)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "echo \"deb http://repo.varnish-cache.org/ubuntu/ lucid varnish-3.0\" >> /etc/apt/sources.list"
        self.logger.info(cmd)
        a = Popen([cmd], stderr=PIPE, stdout=PIPE,shell=True)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "apt-get update"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "apt-get install -y varnish"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "sed -i 's/DAEMON_OPTS=\"-a :6081/DAEMON_OPTS=\"-a :80/g' /etc/default/varnish"
        self.logger.info(cmd)
        a = Popen(["sed","-i","s/DAEMON_OPTS=\"-a :6081/DAEMON_OPTS=\"-a :80/g","/etc/default/varnish"], stderr=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "/etc/init.d/varnish restart"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        self.logger.info("Varnish installation finished")

    def configure_Varnish_Webserver(self):
        if includes.check_apache2_enabled():
            self.logger.info("configuring Varnish to use with apache2")

            cmd = "ls /etc/apache2/sites-available"
            a= Popen(cmd.split(),stdout=PIPE,stderr=PIPE)
            while True:
                line = a.stdout.readline()
                if line != "":
                    f = line.strip()
                    cmd = "sed -i 's/:80>/:8080>/g' /etc/apache2/sites-available"+f
                    self.logger.debug(cmd)
                    b = Popen(["sed","-i","s/:80>/:8080>/g","/etc/apache2/sites-available/"+f],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
                    errmsg = b.stdout.read()
                    if errmsg != "":
                        self.logger.error(errmsg)
                else:
                    break

            cmd = "sed -i 's/.*\*:80.*/NameVirtualHost *:8080/g' /etc/apache2/ports.conf"
            self.logger.debug(cmd)
            b = Popen(["sed","-i","s/.*:80.*/NameVirtualHost *:8080/g","/etc/apache2/ports.conf"],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
            errmsg = b.stdout.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "sed -i 's/Listen 80/Listen 127.0.0.1:8080/g' /etc/apache2/ports.conf"
            self.logger.debug(cmd)
            b = Popen(["sed","-i","s/Listen 80/Listen 127.0.0.1:8080/g","/etc/apache2/ports.conf"],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
            errmsg = b.stdout.read()
            if errmsg != "":
                self.logger.error(errmsg)



            cmd = "/etc/init.d/apache2 restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/varnish restart"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish configured with apache")

        elif includes.check_nginx_enabled():
            self.logger.info("configuring Varnish to use with nginx")
            cmd = "ls /etc/nginx/sites-available"
            a= Popen(cmd.split(),stdout=PIPE,stderr=PIPE)
            while True:
                line = a.stdout.readline()
                if line != "":
                    f = line.strip()
                    cmd = "sed -i 's/\*:80;/\listen 8080>/g' /etc/nginx/sites-available"+f
                    self.logger.debug(cmd)
                    b = Popen(["sed","-i","s/.*80;.*/listen 8080;/g","/etc/nginx/sites-available/"+f],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
                    errmsg = b.stdout.read()
                    if errmsg != "":
                        self.logger.error(errmsg)
                else:
                    break


            cmd = "/etc/init.d/nginx restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/varnish restart"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish configured with nginx")

    def de_configure_Varnish_Webserver(self):
        if includes.check_apache2_enabled():
            self.logger.info("de-configuring Varnish to use with apache2")
            cmd = "ls /etc/nginx/sites-available"
            a= Popen(cmd.split(),stdout=PIPE,stderr=PIPE)
            while True:
                line = a.stdout.readline()
                if line != "":
                    f = line.strip()
                    cmd = "sed -i 's/:8080>/:80>/g' /etc/apache2/sites-available"+f
                    self.logger.debug(cmd)
                    b = Popen(["sed","-i","s/:8080>/:80>/g","/etc/apache2/sites-available/"+f],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
                    errmsg = b.stdout.read()
                    if errmsg != "":
                        self.logger.error(errmsg)
                else:
                    break

            cmd = "sed -i 's/NameVirtualHost *:8080/NameVirtualHost *:80/g' /etc/apache2/ports.conf"
            self.logger.debug(cmd)
            b = Popen(["sed","-i","s/NameVirtualHost *:8080/NameVirtualHost *:80/g","/etc/apache2/ports.conf"],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
            errmsg = b.stdout.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "sed -i 's/.*8080.*/Listen 80/g' /etc/apache2/ports.conf"
            self.logger.debug(cmd)
            b = Popen(["sed","-i","s/.*8080.*/Listen 80/g","/etc/apache2/ports.conf"],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
            errmsg = b.stdout.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/varnish stop"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/apache2 restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish de-configured with apache")

        elif includes.check_nginx_enabled():
            self.logger.info("de-configuring Varnish to use with nginx")
            cmd = "ls /etc/nginx/sites-available"
            a= Popen(cmd.split(),stdout=PIPE,stderr=PIPE)
            while True:
                line = a.stdout.readline()
                if line != "":
                    f = line.strip()
                    cmd = "sed -i 's/listen 8080;/listen 80;/g' /etc/nginx/sites-available"+f
                    self.logger.debug(cmd)
                    b = Popen(["sed","-i","s/listen 8080;/listen 80;/g","/etc/nginx/sites-available/"+f],stdout=PIPE,stderr=PIPE) #can add a comment in the files alerting user to not make changes to 80 again
                    errmsg = b.stdout.read()
                    if errmsg != "":
                        self.logger.error(errmsg)
                else:
                    break

            cmd = "/etc/init.d/varnish stop"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/nginx restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish de-configured with nginx")

    def configure_Varnish_WebStore(self):
        if includes.check_apache2_enabled():
            self.logger.info("configuring Varnish to use with apache2")
            cmd = includes.MAGENTO_APACHE_SERVER + " > /etc/apache2/sites-available/"+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen([cmd],stdout=PIPE,stderr=PIPE,shell=True) # echo and redirection are special take care
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "a2dissite default"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "a2ensite "+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "a2enmod rewrite"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/apache2 restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish configured with apache")

        elif includes.check_nginx_enabled():
            self.logger.info("configuring Varnish to use with nginx")
            cmd = includes.MAGENTO_NGINX_SERVER +" > /etc/nginx/sites-available/"+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen([cmd],stdout=PIPE,stderr=PIPE,shell=True) # echo and redirection are special take care
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "ln -s /etc/nginx/sites-available/"+includes.SITE_NAME+" "+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False,cwd=r'/etc/nginx/sites-enabled/')
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/nginx restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish configured with nginx")

    def de_configure_Varnish_WebStore(self):
        if includes.check_apache2_enabled():
            self.logger.info("configuring Varnish to use with apache2")
            cmd = includes.MAGENTO_APACHE_SERVER + " > /etc/apache2/sites-available/"+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen([cmd],stdout=PIPE,stderr=PIPE,shell=True) # echo and redirection are special take care
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "a2dissite default"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "a2ensite "+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "a2enmod rewrite"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/apache2 restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish configured with apache")

        elif includes.check_nginx_enabled():
            self.logger.info("configuring Varnish to use with nginx")
            cmd = includes.MAGENTO_NGINX_SERVER +" > /etc/nginx/sites-available/"+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen([cmd],stdout=PIPE,stderr=PIPE,shell=True) # echo and redirection are special take care
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "ln -s /etc/nginx/sites-available/"+includes.SITE_NAME+" "+includes.SITE_NAME
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False,cwd=r'/etc/nginx/sites-enabled/')
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/nginx restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Varnish configured with nginx")

    def configure_Varnish(self):
        self.configure_Varnish_Webserver()
        #self.configure_Varnish_WebStore()

    def de_configure_Varnish(self):
        self.de_configure_Varnish_Webserver()
        #self.de_configure_Varnish_WebStore()

    def remove_Varnish(self):
        self.logger.info("not implemented yet")

if TEST ==1:
	w = Varnish()
	w.install_Varnish()
	w.configure_Varnish()