#!/usr/bin/python
from shlex import shlex

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging


class MySQLSrvr():
    def __init__(self):
        self.logger = logging.getLogger('MySQLServer')
        self.IS_SQLServer_PRESENT = True

    def install_SQLServer(self):
        self.logger.info("installing MySQLServer on system")

        # cmd = "sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password "+includes.MYSQL_ROOT_OLD_PASSWORD+"'"
        #self.logger.info(cmd)
        #a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)

        #cmd = "sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password "+includes.MYSQL_ROOT_OLD_PASSWORD+"'"
        #self.logger.info(cmd)
        #a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)

        #cmd = "sudo apt-get -y install mysql-server"
        cmd = "sudo DEBIAN_FRONTEND=noninteractive apt-get install mysql-server-5.5 libapache2-mod-auth-mysql php5-mysql --yes --force-yes"
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

    def check_SQLServer_running(self):
        self.logger.info("checking if SQLerver is running on system")
        cmd = "pidof -c mysqld"
        self.logger.debug(cmd)
        a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
        # a1 = Popen(["ps", "aux"], stdout=PIPE, shell=False)
        #a2 = Popen(["grep", "/usr/sbin/mysqld"], stdin=a1.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        #a = Popen(["awk", "NR>1{ print $2 }"], stdin=a2.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)
        cmdoutput = a.stdout.read()
        if cmdoutput == "":
            self.logger.warning("SQLServer IS NOT RUNNING")
        else:
            self.logger.info("SQLServer IS RUNNING with pid %s", cmdoutput)

    def disable_SQLServer(self):
        self.logger.info("disabling SQLServer...")
        if self.IS_SQLServer_PRESENT:
            a = Popen(["service", "mysql", "stop"], stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
        else:
            self.logger.warning("SQLServer IS NOT PRESENT")

    def enable_SQLServer(self):
        self.logger.info("enabing SQLServer...")
        if self.IS_SQLServer_PRESENT:
            a = Popen(["service", "mysql", "start"], stderr=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
        else:
            self.logger.warning("SQLServer IS NOT PRESENT")

    # migrate_configuration_apache_to_nginx(self):
    def do_book_keeping(self):
        self.logger.info("performing book-keeping...")

    def update_config(self):
        self.logger.info("updating config file...")
        if self.IS_SQLServer_PRESENT:
            # put your config updation code

            # change root password
            # IMPORTANT LINKS
            # http://serverfault.com/questions/4309/how-to-reset-or-recover-admin-account-password-for-mysql
            # http://stackoverflow.com/questions/6067694/mysql-reinstalled-but-root-password-still-there-and-i-forgot-it?rq=1
            # system("echo \"SET PASSWORD FOR root@localhost = PASSWORD('"+includes.MYSQL_ROOT_OLD_PASSWORD+"');\" > /root/scripts/reset.mysqld")
            # system("echo \"init-file=/root/scripts/reset.mysqld\" >> /etc/mysql/my.cnf")
            # self.logger.info(cmd)
            #a = Popen(cmd.split(),stderr=PIPE,stdout=PIPE,shell=True)
            #errmsg = a.stderr.read()
            #if errmsg != "":
            #    self.logger.error(errmsg)

            #cmd  ="service mysql restart && sed -i 's/init-file=\/root\/scripts\/reset.mysqld/d' /etc/mysql/my.cnf && service mysql restart && 
            #cmd = " service mysql restart"
            self.logger.info("resetting mysql root password...")
            #self.logger.info(cmd)
            cmd = "mysqladmin -u root password " + includes.MYSQL_ROOT_NEW_PASSWORD
            self.logger.info(cmd)
            a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)


                #cmd = "mysqladmin -u root -p"+includes.MYSQL_ROOT_OLD_PASSWORD+" password "+includes.MYSQL_ROOT_NEW_PASSWORD
                #self.logger.info(cmd)
            #a = Popen(cmd.split(),stderr=PIPE,stdout=PIPE,shell=False)
            #errmsg = a.stderr.read()
            #if errmsg != "":
            #    self.logger.error(errmsg)

            self.logger.info("done resetting mysql root password...")

            # create database
            #self.logger.info("creating datebase for default installation...")
            cmd = "echo \"create database " + includes.MYSQL_DBNAME + ";\" | mysql -u root -p" + includes.MYSQL_ROOT_PASSWORD
            self.logger.info(cmd)
            system(cmd)
            a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=True)
            errmsg = a.stderr.read()
            cmdoutput = a.stdout.read()
            #print cmdoutput
            if errmsg != "":
                self.logger.error(errmsg)

            TEST1 = 0
            if TEST1 == 0:
                cmd = "echo \"show databases;\" | mysql -u root -p" + includes.MYSQL_ROOT_PASSWORD
                self.logger.info(cmd)
                system(cmd)
                # command below i am not able to make it work r8 now
                a = Popen(cmd.split(), stderr=PIPE, stdout=PIPE, shell=True)
                errmsg = a.stderr.read()
                if errmsg != "":
                    self.logger.error(errmsg)

            self.logger.info("done creating database for default installation...")


            # grant all priviledges to user till now no need as root is given to user || is a security concern as mysql
            # runs as root and by this process developer will have access to root user


            self.logger.warning("no config updates defined yet...")
            # mail user his db details from backend  or if you have taken this info from user itself then just die
        else:
            self.logger.warning("SQLServer IS NOT PRESENT")


    def remove_SQLServer(self):
        self.logger.info("Removing SQLServer")
        system(
            "echo \"update user set password=password('') where user='root'; flush privileges;\" | mysql --defaults-file=/etc/mysql/debian.cnf mysql")
        cmd = "apt-get remove --purge -y mysql-server-5.5"
        self.logger.info(cmd)
        # a = Popen(["apt-get", "remove", "mysql-server-5.5", "-y"], stderr=PIPE, stdout=PIPE, shell=False)
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)


if TEST == 1:
    m = MySQLSrvr()
    m.check_SQLServer_running()
    m.install_SQLServer()
    m.check_SQLServer_running()
    m.update_config()
    m.disable_SQLServer()
    m.check_SQLServer_running()
    m.enable_SQLServer()
    m.check_SQLServer_running()
    #m.remove_SQLServer()
