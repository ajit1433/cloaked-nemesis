#!/usr/bin/python
__author__ = 't'
TEST = 0

from subprocess import Popen, PIPE, call
import logging
from os import system

from preprocess import preprocess
import includes


class nginx():
    def __init__(self):
        self.logger = logging.getLogger('NGINX')
        #self.IS_APACHE_PRESENT = includes.check_apache2_present()
        #self.IS_APACHE_ENABLED = includes.check_apache2_enabled()
        #self.IS_NGINX_PRESENT = includes.check_nginx_present()
        #self.IS_NGINX_ENABLED = includes.check_nginx_enabled()

    def install_nginx(self):
        self.logger.info("installing nginx on system")
        a = Popen(["apt-get", "install", "nginx", "-y"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        a = Popen(["rm", "default"], stderr=PIPE, stdout=PIPE, shell=False,cwd=r'/etc/nginx/sites-enabled/')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

    def check_nginx_running(self):
        self.logger.info("checking if nginx is running on system")
        a1 = Popen(["ps", "aux"], stdout=PIPE, shell=False)
        a2 = Popen(["grep", "nginx: master process /usr/sbin/nginx"], stdin=a1.stdout, stderr=PIPE, stdout=PIPE,
                   shell=False)
        a = Popen(["awk", "{ print $2 }"], stdin=a2.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)
        cmdoutput = a.stdout.readline()
        if cmdoutput == "":
            self.logger.warning("NGINX IS NOT RUNNING")
        else:
            self.logger.info("NGINX IS RUNNING with pid %s", cmdoutput)

    def enable_nginx(self):
        self.logger.info("enabling nginx...")
        a = Popen(["/etc/init.d/nginx", "start"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)
        else:
            self.logger.warning("NGINX IS NOT PRESENT")

            # system(includes.NGINX_STARTUP_FILE+" start")

            # need to check if nginx stopped successfully


    # migrate_configuration_apache_to_nginx(self):
    def do_book_keeping(self):
        self.logger.info("performing book-keeping...")

    def remove_nginx(self):
        self.logger.info("Removing nginx")
        a = Popen(["apt-get", "remove", "nginx", "-y"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)
        else:
            self.logger.warning("NGINX IS NOT PRESENT")

    def disable_nginx(self):
        self.logger.info("disabling nginx")
        a = Popen(["/etc/init.d/nginx", "stop"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.err(errmsg)
        else:
            self.logger.warning("NGINX IS NOT PRESENT")

        #system(includes.NGINX_STARTUP_FILE +" stop")
        # need to check if apache stopped successfully


if TEST == 1:
    pre = preprocess()
    pre.check_root()
    ngnx = nginx()
    ngnx.do_book_keeping()
    ngnx.install_nginx()
    ngnx.enable_nginx()
    ngnx.check_nginx_running()
    #ngnx.remove_nginx()
