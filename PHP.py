#!/usr/bin/python

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
from PHPFPM import PHPFPM
import includes
import logging


class PHP():
    def __init__(self):
        self.logger = logging.getLogger('PHP')

    def install_PHP(self):
        if includes.check_apache2_enabled():
            self.logger.info("installing PHP on system")
            cmd = "apt-get install -y php5 libapache2-mod-php5 libapache2-mod-auth-mysql php5-mysql php5-gd libcurl3 php5-curl php5-gd php5-mcrypt"

            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            cmdoutput = a.stdout.read()
            includes.logit(cmd,cmdoutput,errmsg)
            if errmsg != "":
                self.logger.error(errmsg)

        elif includes.check_nginx_enabled():
            p = PHPFPM()
            p.install_PHPFPM()

    def uninstall_PHP(self):
        self.logger.info("Un-installing PHP on system")
        cmd = "apt-get remove -y php5 libapache2-mod-php5 libapache2-mod-auth-mysql php5-mysql php5-gd libcurl3 php5-curl php5-gd php5-mcrypt"

        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

if TEST==1:
	p = PHP()
	p.install_PHP()
