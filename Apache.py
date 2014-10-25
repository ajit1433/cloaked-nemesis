#!/usr/bin/python

__author__ = 't'
TEST = 0

from subprocess import Popen, PIPE, call
import logging
import includes
from os import system

from preprocess import preprocess
import includes


class apache():
    def __init__(self):
        self.logger = logging.getLogger('APACHE')
        #self.IS_APACHE_PRESENT = includes.check_apache2_present()
        #self.IS_APACHE_ENABLED = includes.check_apache2_enabled()
        #self.IS_NGINX_PRESENT = includes.check_nginx_present()
        #self.IS_NGINX_ENABLED = includes.check_nginx_enabled()

    def install_apache(self):
        self.logger.info("installing apache on system")
        self.logger.debug("CMD: apt-get install apache2 -y" )
        a = Popen(["apt-get","install","apache2","-y"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        if cmdoutput!="":
            self.logger.debug("CMD_OP: "+cmdoutput)
        if errmsg != "":
            self.logger.error(errmsg)

        self.logger.info("finished installing apache on system")

    def check_apache_running(self):
        self.logger.info("checking if apache is running on system")
        self.logger.debug("CMD: ps aux | grep '/usr/sbin/apache2 -k start' | grep root | awk '{ print $2 }'" )
        a1 = Popen(["ps", "aux"], stdout=PIPE, shell=False)
        a2 = Popen(["grep", "/usr/sbin/apache2 -k start"], stdin=a1.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        a3 = Popen(["grep", "root"], stdin=a2.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        a = Popen(["awk", "{ print $2 }"], stdin=a3.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        cmdoutput = a.stdout.readline()
        errmsg = a.stderr.read()
        if cmdoutput!="":
            self.logger.debug("CMD_OP: "+cmdoutput)
        if errmsg != "":
            self.logger.warning("APACHE IS NOT RUNNING")
        else:
            self.logger.info("APACHE IS RUNNING with pid "+cmdoutput)

    def disable_nginx(self):
        self.logger.info("disabling nginx...")
        self.logger.debug("CMD: /etc/init.d/nginx stop" )
        a = Popen(["/etc/init.d/nginx", "stop"], stderr=PIPE, stdout=PIPE, shell=False)
        cmdoutput = a.stdout.read()
        errmsg = a.stderr.read()
        if cmdoutput!="":
            self.logger.debug("CMD_OP: "+cmdoutput)
        if errmsg != "":
            self.logger.error(errmsg)

    def enable_apache(self):
        self.logger.info("enabing apache...")

        a = Popen(["/etc/init.d/apache2", "start"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        if cmdoutput!="":
            self.logger.debug("CMD_OP: "+cmdoutput)
        if errmsg != "":
            self.logger.error(errmsg)

            # system(includes.APACHE_STARTUP_FILE+" start")

    # migrate_configuration_apache_to_nginx(self):
    def do_book_keeping(self):
        self.logger.info("performing book-keeping...")
        #self.disable_nginx()

    def remove_apache(self):
        self.logger.info("Removing apache")
        self.logger.debug("CMD: apt-get remove apache2 -y")
        a = Popen(["apt-get", "remove", "apache2", "-y"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        if cmdoutput!="":
            self.logger.debug("CMD_OP: "+cmdoutput)
        if errmsg != "":
            self.logger.error(errmsg)

    def disable_apache(self):
        self.logger.info("disabling apache")
        self.logger.debug("CMD: /etc/init.d/apache2 stop")
        a = Popen(["/etc/init.d/apache2", "stop"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        if cmdoutput!="":
            self.logger.debug("CMD_OP: "+cmdoutput)
        if errmsg != "":
            self.logger.err(errmsg)


if TEST == 1:
    pre = preprocess()
    pre.check_root()
    apche = apache()
    apche.do_book_keeping()
    apche.install_apache()
    apche.enable_apache()
    apche.check_apache_running()
    apche.remove_apache()
