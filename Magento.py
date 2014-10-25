#!/usr/bin/python

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging


class Magento():
    def __init__(self):
        self.logger = logging.getLogger('Magento')

    def install_Magento(self):
        self.logger.info("installing Magento on system")

        cmd = "mkdir public_html"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "wget http://www.magentocommerce.com/downloads/assets/1.9.0.1/magento-1.9.0.1.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "tar -xf magento-1.9.0.1.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE,shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "mv * .htaccess ../"
        self.logger.info(cmd)
        a = Popen([cmd], stderr=PIPE, shell=True,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html/magento') # mv is a special case for Popen
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "rm magento-1.9.0.1.tar.gz && rm magento/* -Rf && rmdir magento"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "chmod -R o+w media var"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "chmod o+w app/etc"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        self.logger.info("Magento installation finished")

    def configure_Magento(self):
        if includes.check_apache2_enabled():
            self.logger.info("configuring Magento to use with apache2")
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

            self.logger.info("Magento configured with apache")

        elif includes.check_nginx_enabled():
            self.logger.info("configuring Magento to use with nginx")
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

            self.logger.info("Magento configured with nginx")


if TEST ==1:
	w = Magento()
	w.install_Magento()
	w.configure_Magento()