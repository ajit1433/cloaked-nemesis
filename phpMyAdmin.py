#!/usr/bin/python
from shlex import shlex

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging


class phpMyAdmin():
    def __init__(self):
        self.logger = logging.getLogger('phpMyAdmin')
        # self.IS_SQLServer_PRESENT = True

    def install_phpMyAdmin(self):
        self.logger.info("installing phpMyAdmin on system")

        cmd = "wget http://sourceforge.net/projects/phpmyadmin/files/phpMyAdmin/4.2.10/phpMyAdmin-4.2.10-all-languages.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False, cwd=r'/usr/share')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "tar -xf phpMyAdmin-4.2.10-all-languages.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False, cwd=r'/usr/share')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "rm phpMyAdmin-4.2.10-all-languages.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False, cwd=r'/usr/share')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "mv phpMyAdmin-4.2.10-all-languages phpmyadmin"
        self.logger.info(cmd)
        a = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True, cwd=r'/usr/share')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "chown www-data:www-data phpmyadmin -R"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False, cwd=r'/usr/share')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "chmod 755 -R phpmyadmin"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False, cwd=r'/usr/share')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        #cmd = "echo " \
        #      "     \"Alias /phpmyadmin \"/usr/share/phpmyadmin\"\n" \
        #      "     Alias /phpMyAdmin \"/usr/share/phpmyadmin\"\n" \
        #      "     <Directory /usr/share/phpmyadmin>\n" \
        #      "        	\tOptions Indexes FollowSymLinks\n" \
        #      "         \tAllowOverride None\n" \
        #      "         \tOrder allow,deny\n" \
        #      "         \tallow from all\n" \
        #      "     </Directory>\"  > /etc/apache2/conf.d/phpmyadmin.conf"
        #self.logger.info(cmd)
        #a = Popen([cmd], stderr=PIPE, stdout=PIPE, shell=True)
        #errmsg = a.stderr.read()
        #if errmsg != "":
        #    self.logger.error(errmsg)

        #cmd = "/etc/init.d/apache2 restart"
        #a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
        #errmsg = a.stderr.read()
        #if errmsg != "":
        #    self.logger.error(errmsg)


    # to be named exactly as enable_phpMyAdmin_Apache
    def enable_phpMyAdmin(self):
        self.logger.info("enabing phpMyAdmin...")
        if includes.check_apache2_enabled():
            cmd = "ls -la /etc/apache2/sites-available/ | grep -c phpmyadmin"
            a1 = Popen(["ls", "-la", "/etc/apache2/sites-available/"], stderr=PIPE, stdout=PIPE, shell=False)
            a = Popen(["grep", "phpmyadmin", "-c"], stdin=a1.stdout, stdout=PIPE, stderr=PIPE, shell=False)

            errmsg = a.stderr.read()
            cmdoutput = a.stdout.read()
            if errmsg != "":
                self.logger.error(errmsg)

            if cmdoutput.strip() == "0":  # no phpmyadmin present in that directory

                cmd = includes.PMA_APACHE_SERVER+"  > /etc/apache2/sites-available/phpmyadmin"
                self.logger.info(cmd)
                a = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "echo \"NameVirtualHost *:9000\\nListen 127.0.0.1:9000\" >> /etc/apache2/ports.conf"
                self.logger.info(cmd)
                a = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)


                cmd = "a2ensite phpmyadmin"
                self.logger.debug(cmd)
                a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "/etc/init.d/apache2 restart"
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

            else:
                cmd = "a2ensite phpmyadmin"
                self.logger.debug(cmd)
                a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "/etc/init.d/apache2 restart"
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)
        elif includes.check_nginx_enabled():
            cmd = "ls -la /etc/nginx/sites-enabled/ | grep -c phpmyadmin"
            a1 = Popen(["ls", "-la", "/etc/nginx/sites-enabled/"], stderr=PIPE, stdout=PIPE, shell=False)
            a = Popen(["grep", "phpmyadmin", "-c"], stdin=a1.stdout, stdout=PIPE, stderr=PIPE, shell=False)

            errmsg = a.stderr.read()
            cmdoutput = a.stdout.read()
            if errmsg != "":
                self.logger.error(errmsg)

            if cmdoutput.strip() == "0":  # no phpmyadmin.conf present in that directory

                cmd = includes.PMA_NGINX_SERVER+"  > /etc/nginx/sites-available/phpmyadmin"
                self.logger.info(cmd)
                a = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "ln -s /etc/nginx/sites-available/phpmyadmin phpmyadmin"
                self.logger.info(cmd)
                a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False,cwd=r'/etc/nginx/sites-enabled/')
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "/etc/init.d/nginx restart"
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

            else:
                cmd = "ln -s /etc/nginx/sites-available/phpmyadmin phpmyadmin"
                self.logger.info(cmd)
                a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False,cwd=r'/etc/nginx/sites-enabled/')
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "/etc/init.d/apache2 restart"
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)


    # to be named exactly as disable_phpMyAdmin_Apache
    def disable_phpMyAdmin(self):
        self.logger.info("Disabling phpMyAdmin")
        if includes.check_apache2_enabled():

            cmd = "a2dissite phpmyadmin"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            cmd = "/etc/init.d/apache2 restart"
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            else:
                self.logger.info("phpmyadmin disabled")

        elif includes.check_nginx_enabled():
            cmd = "ls -la /etc/nginx/sites-enabled/ | grep -c phpmyadmin"
            self.logger.debug(cmd)
            a1 = Popen(["ls", "-la", "/etc/nginx/sites-enabled"], stderr=PIPE, stdout=PIPE, shell=False)
            a = Popen(["grep", "phpmyadmin", "-c"], stdin=a1.stdout, stdout=PIPE, stderr=PIPE, shell=False)

            errmsg = a.stderr.read()
            cmdoutput = a.stdout.read()
            includes.logit(cmd,cmdoutput,errmsg)
            if errmsg != "":
                self.logger.error(errmsg)
            if cmdoutput.strip() != "0":  # no phpmyadmin.conf present in that directory
                cmd = "rm phpmyadmin"
                self.logger.debug(cmd)
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False,cwd=r'/etc/nginx/sites-enabled')
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

                cmd = "/etc/init.d/nginx restart"
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

            else:
                self.logger.error("phpmyadmin not found in sites-enabled. phpmyadmin should already be disabled")

if TEST == 1:
    pma = phpMyAdmin()
    # pma.install_phpMyAdmin()
    pma.disable_phpMyAdmin()
    pma.enable_phpMyAdmin()