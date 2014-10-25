#!/usr/bin/python

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging


class Wordpress():
    def __init__(self):
        self.logger = logging.getLogger('WORDPRESS')

    def install_Wordpress(self):
        self.logger.info("installing Wordpress on system")

        cmd = "mkdir public_html"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "wget https://www.wordpress.org/latest.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "tar -xf latest.tar.gz"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE,shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "mv * ../"
        self.logger.info(cmd)
        a = Popen([cmd], stderr=PIPE, shell=True,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html/wordpress') # mv is a special case for Popen
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "rm latest.tar.gz && rm wordpress/* -Rf && rmdir wordpress"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "cp wp-config-sample.php wp-config.php"
        self.logger.info(cmd)
        a = Popen([cmd], stderr=PIPE, shell=True,cwd=r'/home/'+includes.SYS_USERNAME+'/public_html')
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)
	
        cmd = "sed -i 's/.*DB_NAME.*/define( \'DB_NAME\', \'"+includes.MYSQL_DBNAME+"\' );/g' /home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"
        self.logger.info(cmd)
        a = Popen(["sed","-i","s/.*DB_NAME.*/define('DB_NAME', '"+includes.MYSQL_DBNAME+"');/g","/home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd ="sed -i 's/.*DB_NAME.*/define( \'DB_HOST\', \'localhost\' );/g' /home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"
        self.logger.info(cmd)
        a = Popen(["sed","-i","s/.*DB_HOST.*/define('DB_HOST', 'localhost');/g","/home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd="sed -i 's/.*DB_NAME.*/define( \'DB_USER\', \'root\' );/g' /home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"
        self.logger.info(cmd)
        a = Popen(["sed","-i","s/.*DB_USER.*/define('DB_USER', 'root');/g","/home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd="sed -i 's/.*DB_NAME.*/define( \'DB_PASSWORD\', \'"+includes.MYSQL_ROOT_NEW_PASSWORD+"\');/g' /home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"
        self.logger.info(cmd)
        a = Popen(["sed","-i","s/.*DB_PASSWORD.*/define('DB_PASSWORD', '"+includes.MYSQL_ROOT_NEW_PASSWORD+"');/g","/home/"+includes.SYS_USERNAME+"/public_html/wp-config.php"], stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

        cmd="chown "+includes.SYS_USERNAME+":www-data public_html -R"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False,cwd=r'/home/'+includes.SYS_USERNAME)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)


        self.logger.info("wordpress installation finished")
    
    def configure_Wordpress(self):
        if includes.check_apache2_enabled():
            self.logger.info("configuring wordpress to use with apache2")
            cmd = includes.WORDPRESS_APACHE_SERVER + " > /etc/apache2/sites-available/"+includes.SITE_NAME
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

            cmd = "/etc/init.d/apache2 restart"
            self.logger.debug(cmd)
            a = Popen(cmd.split(),stdout=PIPE,stderr=PIPE,shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            self.logger.info("Wordpress configured with apache")

        elif includes.check_nginx_enabled():
            self.logger.info("configuring wordpress to use with nginx")
            cmd = includes.WORDPRESS_NGINX_SERVER +" > /etc/nginx/sites-available/"+includes.SITE_NAME
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

            self.logger.info("Wordpress configured with nginx")


if TEST ==1:
	w = Wordpress()
	w.install_Wordpress()
	w.configure_Wordpress()