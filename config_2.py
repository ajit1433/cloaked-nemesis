#!/usr/bin/python
# __author__ = 'root'

import logging

from preprocess import preprocess
from Apache import apache
from Nginx import nginx
from FTPServer import FTPSrvr
from MySQL import MySQLSrvr
from phpMyAdmin import phpMyAdmin
from User import User
from PHP import PHP
from Wordpress import Wordpress
from Pagespeed import Pagespeed
from Varnish import Varnish
from Apc import APC

#core = 1   #apache2 as webserver
core = 0    #nginx as webserver


logger = logging.getLogger(__name__)

preprocessing = preprocess()

# check if script is being run as root
preprocessing.check_root()
logger.info("User.py START *************************************************************************************************************")
# create User
U = User()
U.create_User()
logger.info("User.py END *************************************************************************************************************")

logger.info("Nginx.py START *************************************************************************************************************")
# install Apache
A = nginx()
A.install_nginx()
A.enable_nginx()
logger.info("Nginx.py END *************************************************************************************************************")

logger.info("PHP.py START *************************************************************************************************************")
# install PHP
P = PHP()
P.install_PHP()
logger.info("PHP.py END *************************************************************************************************************")

logger.info("MySQL.py START *************************************************************************************************************")
# install MySQL
M = MySQLSrvr()
M.install_SQLServer()
M.check_SQLServer_running()
M.enable_SQLServer()
M.update_config()
M.disable_SQLServer()
M.enable_SQLServer()
M.enable_SQLServer()
logger.info("MySQL.py END *************************************************************************************************************")

logger.info("phpMyAdmin.py START *************************************************************************************************************")
# install phpmyadmin
PMA = phpMyAdmin()
PMA.install_phpMyAdmin()
PMA.enable_phpMyAdmin()
logger.info("phpMyAdmin.py END *************************************************************************************************************")

logger.info("Wordpress.py START *************************************************************************************************************")
# install wordpress
W = Wordpress()
W.install_Wordpress()
W.configure_Wordpress()
logger.info("Wordpress.py END *************************************************************************************************************")

logger.info("FTPServer.py START *************************************************************************************************************")
# install FTPServer
F = FTPSrvr()
F.install_FTPServer()
F.update_config()
F.disable_FTPServer()
F.enable_FTPServer()
F.do_book_keeping()
logger.info("FTPServer.py END *************************************************************************************************************")

logger.info("Pagespeed.py START *************************************************************************************************************")
# install Pagespeed
F = Pagespeed()
F.install_Pagespeed()
F.check_Pagespeed_enabled()
F.disable_Pagespeed()
F.check_Pagespeed_enabled()
logger.info("Pagespeed.py END *************************************************************************************************************")

logger.info("Varnish.py START *************************************************************************************************************")
# install Varnish
F = Varnish()
F.install_Varnish()
F.configure_Varnish()
logger.info("Varnish.py END *************************************************************************************************************")

logger.info("APC.py START *************************************************************************************************************")
# install APC
F = APC()
F.install_APC()
F.configure_APC()
logger.info("APC.py END *************************************************************************************************************")