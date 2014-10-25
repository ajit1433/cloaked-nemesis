#!/usr/bin/python

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging


class PHPFPM():
    def __init__(self):
        self.logger = logging.getLogger('PHPFPM')

    def install_PHPFPM(self):
        self.logger.warning("installing only on nginx system")
        self.logger.info("installing PHPFPM on system")

        #install php5-fpm
        cmd = "apt-get install php5-fpm php5-cli php5-mysql libcurl3 php5-curl php5-gd php5-mcrypt -y"
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "apt-get install php5-fpm php5-cli php5-mysql libcurl3 php5-curl php5-gd php5-mcrypt -y"
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        # update php5-fpm config
        cmd = "sed -i 's/.*listen = 127.0.0.1:9000.*/;listen = 127.0.0.1:9000\\nlisten = \/tmp\/php5-fpm.sock/g' /etc/php5/fpm/pool.d/www.conf"
        a = Popen(["sed","-i","s/.*listen = 127.0.0.1:9000.*/;listen = 127.0.0.1:9000\\nlisten = \/tmp\/php5-fpm.sock/g","/etc/php5/fpm/pool.d/www.conf"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "sed -i 's/.*listen.owner =.*/listen.owner = www-data/g' /etc/php5/fpm/pool.d/www.conf"
        a = Popen(["sed","-i","s/.*listen.owner = www-data.*/listen.owner = www-data/g","/etc/php5/fpm/pool.d/www.conf"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "sed -i 's/.*listen.group =.*/listen.group = www-data/g' /etc/php5/fpm/pool.d/www.conf"
        a = Popen(["sed","-i","s/.*listen.group =.*/listen.group = www-data/g","/etc/php5/fpm/pool.d/www.conf"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "sed -i 's/.*listen.mode =*/listen.mode = 0660/g' /etc/php5/fpm/pool.d/www.conf"
        a = Popen(["sed","-i","s/.*listen.mode =.*/listen.mode = 0660/g","/etc/php5/fpm/pool.d/www.conf"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "/etc/init.d/php5-fpm restart"
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

    def uninstall_PHPFPM(self):
        self.logger.info("Hell awaits you...")

if TEST==1:
	p = PHPFPM()
	p.install_PHPFPM()
