#!/usr/bin/python

__author__ = 't'
TEST = 0

from preprocess import preprocess
from subprocess import Popen, PIPE, call
from os import system
import includes
import logging
import crypt

class User():
    def __init__(self):
        self.logger = logging.getLogger('User creation...')

    def create_User(self):
        self.logger.info("creating User on system")

        cmd = "adduser --disabled-password --gecos '' "+includes.SYS_USERNAME
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=False)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)
            
        cmd = "echo "+includes.SYS_USERNAME+":"+includes.SYS_PASSWORD+" | chpasswd"
        self.logger.info(cmd)
        a = Popen(["echo",includes.SYS_USERNAME+":"+includes.SYS_PASSWORD],stdout=PIPE,stderr=PIPE)
        errmsg = a.stderr.read()
	
        a = Popen(["chpasswd"],stdin=a.stdout,stdout=PIPE,stderr=PIPE)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)

        cmd = "cd /home/"+includes.SYS_USERNAME
        self.logger.info(cmd)
        a = Popen(cmd.split(), stderr=PIPE,stdout=PIPE, shell=True)
        errmsg = a.stderr.read()
        cmdoutput = a.stdout.read()
        includes.logit(cmd,cmdoutput,errmsg)
        if errmsg != "":
            self.logger.error(errmsg)



        self.logger.info("creating user finished")

if TEST==1:
	u=User()
	u.create_User()
