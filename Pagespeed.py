#!/usr/bin/python
from shlex import shlex

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging


class Pagespeed():
    def __init__(self):
        self.logger = logging.getLogger('Pagespeed')

    def install_Pagespeed(self):
        if includes.check_apache2_enabled():
            self.logger.info("installing Pagespeed on Apache system")

            cmd = "wget https://dl-ssl.google.com/dl/linux/direct/mod-pagespeed-stable_current_amd64.deb"   #x64 only
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/root/scripts')
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "dpkg -i mod-pagespeed-stable_current_amd64.deb"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/root/scripts')
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)


            cmd = "apt-get -f install"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "rm mod-pagespeed-stable_current_amd64.deb"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/root/scripts')
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)


            cmd = "/etc/init.d/apache2 restart"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            #cmd = "curl -I -p http://localhost"
            #self.logger.debug(cmd)
            #a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
            #errmsg = a.stderr.read()
            #if errmsg != "":
            #    self.logger.error(errmsg)


            #cmd = "grep -c 'X-Page-Speed'"
            #a = Popen(cmd.split(),stdin=a.stdout, stderr=PIPE, shell=False)
            #errmsg = a.stderr.read()
            #if errmsg != "":
            #    self.logger.error(errmsg)
            #cmdoutput = a.stdout.read()
            #if cmdoutput =="0":
            #     self.logger.warning("mod-pagespeed not installed/enabled over apache")
            #else:
            self.logger.info("mod-pagespeed installed+enabled")


        elif includes.check_nginx_enabled():
            self.logger.warning("not ready for hell")

    def check_Pagespeed_enabled(self):
        self.logger.info("checking if Pagespeed is enabled on system")
        if includes.check_apache2_enabled():
            cmd = "sed -nr '/ModPagespeed on/p' /etc/apache2/mods-available/pagespeed.conf | awk '{ print $2 }'"

            a = Popen(["sed","-nr","/ModPagespeed on/p","/etc/apache2/mods-available/pagespeed.conf"],stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            a = Popen(["grep","ModPagespeed on", "-c"],stdin=a.stdout,stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
            cmdoutput = a.stdout.read()
            if cmdoutput =="0":
                self.logger.warning("ModPagespeed not enabled")
                return False
            else:
                self.logger.info("ModPagespeed is enabled")
                return True
        elif includes.check_nginx_enabled():
            self.logger.warning("not ready for hell")

    def disable_Pagespeed(self):
        self.logger.info("disabling pagespeed on system")
        if includes.check_apache2_enabled():
            a = Popen(["sed","-i","s/.*ModPagespeed on.*/ModPagespeed off/g", "/etc/apache2/mods-available/pagespeed.conf"], stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
            else:
                cmd = "/etc/init.d/apache2 restart"
                self.logger.info(cmd)
                a = Popen(cmd.split(), stderr=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)
                self.logger.warning("Pagespeed disabled on Apache")

        elif includes.check_nginx_enabled():
            self.logger.warning("not ready for hell")

    def enable_Pagespeed(self):
        self.logger.info("enabing Pagespeed...")
        if includes.check_apache2_enabled():
            a = Popen(["sed","-i","s/.*ModPagespeed off.*/ModPagespeed on/g", "/etc/apache2/mods-available/pagespeed.conf"], stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
            else:
                cmd = "/etc/init.d/apache2 restart"
                self.logger.info(cmd)
                a = Popen(cmd.split(), stderr=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)
                self.logger.warning("Pagespeed enabled on Apache")

        elif includes.check_nginx_enabled():
            self.logger.warning("not ready for hell")

    # migrate_configuration_apache_to_nginx(self):
    def do_book_keeping(self):
        self.logger.info("performing book-keeping...")

    def update_config(self):
        self.logger.info("updating config file...")

if TEST == 1:
    m = Pagespeed()
    m.install_Pagespeed()
    m.check_Pagespeed_enabled()
    m.disable_Pagespeed()
    m.check_Pagespeed_enabled()
    m.enable_Pagespeed()
    m.check_Pagespeed_enabled()
