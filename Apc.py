#!/usr/bin/python
__author__ = 't'
TEST = 0

from subprocess import Popen, PIPE, call
import logging
from os import system

from preprocess import preprocess
import includes


class APC():
    def __init__(self):
        self.logger = logging.getLogger('APC')

    def install_APC(self):
        self.logger.info("installing APC on system")
        cmd = "apt-get install -y php-pear php5-dev make libpcre3-dev"
        a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "\"\n\" |pecl -f install apc"
        a = Popen([cmd], stderr=PIPE, stdout=PIPE, shell=True)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

    def configure_APC(self):
        self.logger.info("Configuring APC with PHP")

        self.logger.info("add APC to PHP")
        cmd = "echo \"extension=apc.so\" >> /etc/php5/apache2/php.ini"
        self.logger.debug(cmd)
        a = Popen([cmd], stderr=PIPE, stdout=PIPE, shell=True)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        if includes.check_apache2_enabled():
            cmd = "/etc/init.d/apache2 restart"
            a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

        if includes.check_nginx_enabled():
            cmd = "/etc/init.d/nginx restart"
            a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)