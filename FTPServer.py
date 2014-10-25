#!/usr/bin/python
__author__ = 't'
TEST = 0

from subprocess import Popen, PIPE, call
import logging
from os import system

from preprocess import preprocess
import includes


class FTPSrvr():
    def __init__(self):
        self.logger = logging.getLogger('FTPServer')
        self.IS_FTPServer_PRESENT = True

    def install_FTPServer(self):
        self.logger.info("installing FTPServer on system")
        cmd = "apt-get install -y vsftpd"
        self.logger.debug(cmd)
        a = Popen(["apt-get", "install", "vsftpd", "-y"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)

    def check_FTPServer_running(self):
        self.logger.info("checking if FTPServer is running on system")
        cmd = "pidof -c vsftpd"
        a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False)
        # cmd = "ps aux | grep /usr/sbin/vsftpd | awk 'NR>1{ print $2 }'"
        self.logger.debug(cmd)
        #a1 = Popen(["ps", "aux"], stdout=PIPE, shell=False)
        #a2 = Popen(["grep", "/usr/sbin/vsftpd"], stdin=a1.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        # a3=Popen(["grep", "root"], stdin=a2.stdout, stderr=PIPE,stdout=PIPE, shell=False)
        #a = Popen(["awk", "NR>1{ print $2 }"], stdin=a2.stdout, stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)
        cmdoutput = a.stdout.readline()
        if cmdoutput == "":
            self.logger.warning("FTPServer IS NOT RUNNING")
        else:
            self.logger.info("FTPServer IS RUNNING with pid %s", cmdoutput)

    def disable_FTPServer(self):
        self.logger.info("disabling FTPServer...")
        if self.IS_FTPServer_PRESENT:
            cmd = "service vstpd stop"
            self.logger.debug(cmd)
            a = Popen(["service", "vsftpd", "stop"], stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
        else:
            self.logger.warning("FTPServer IS NOT PRESENT")

            # system(includes.NGINX_STARTUP_FILE+" stop")
            # Popen(["/etc/init.d/nginx", "stop"])

    def enable_FTPServer(self):
        self.logger.info("enabing FTPServer...")
        if self.IS_FTPServer_PRESENT:
            cmd = "service vsftpd start"
            self.logger.debug(cmd)
            a = Popen(["service", "vsftpd", "start"], stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)
        else:
            self.logger.warning("FTPServer IS NOT PRESENT")

            # system(includes.APACHE_STARTUP_FILE+" start")

    # migrate_configuration_apache_to_nginx(self):
    def do_book_keeping(self):
        self.logger.info("performing book-keeping...")

    def update_config(self):
        self.logger.info("updating config file...")
        if self.IS_FTPServer_PRESENT:

            # disable anonymous login
            cmd = "sed -i 's/.*anonymous_enable.*/anonymous_enable=NO/g' /etc/vsftpd.conf"
            self.logger.debug(cmd)
            a = Popen(["sed", "-i", "s/.*anonymous_enable.*/anonymous_enable=NO/g", "/etc/vsftpd.conf"], stderr=PIPE,
                      stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            # enable local_logins
            cmd = "sed -i '0,/local_enable=/s/.*local_enable=.*/local_enable=YES/g' /etc/vsftpd.conf"
            self.logger.debug(cmd)
            a = Popen(["sed", "-i", "0,/local_enable=/s/.*local_enable=.*/local_enable=YES/g", "/etc/vsftpd.conf"],
                      stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            # enable wirting to filesystem
            cmd = "sed -i '0,/write_enable=/s/.*write_enable=.*/write_enable=YES/g' /etc/vsftpd.conf"
            self.logger.debug(cmd)
            a = Popen(["sed", "-i", "0,/write_enable=/s/.*write_enable=.*/write_enable=YES/g", "/etc/vsftpd.conf"],
                      stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

            # enable chroot
            cmd = "sed -i '0,/chroot_local_user=/s/.*chroot_local_user=.*/chroot_local_user=YES/g' /etc/vsftpd.conf"
            self.logger.debug(cmd)
            a = Popen(["sed", "-i", "0,/chroot_local_user=/s/*chroot_local_user=*/'chroot_local_user=YES'/g",
                       "/etc/vsftpd.conf"], stderr=PIPE, stdout=PIPE, shell=False)
            errmsg = a.stderr.read()
            if errmsg != "":
                self.logger.error(errmsg)

        else:
            self.logger.warning("FTPServer IS NOT PRESENT")


    def remove_FTPServer(self):
        self.logger.info("Removing FTPServer")
        cmd = "apt-get remove -y vsftpd"
        self.logger.debug(cmd)
        a = Popen(["apt-get", "remove", "vsftpd", "-y"], stderr=PIPE, stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        if errmsg != "":
            self.logger.error(errmsg)


if TEST == 1:
    f = FTPSrvr()
    f.install_FTPServer()
    f.update_config()
    f.check_FTPServer_running()
    f.disable_FTPServer()
    f.check_FTPServer_running()
    f.enable_FTPServer()
    f.check_FTPServer_running()
#f.remove_FTPServer()
