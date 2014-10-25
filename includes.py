__author__ = 't'

from subprocess import Popen, PIPE, call
import logging


# [system]
SYS_USERNAME = "test"
SYS_PASSWORD = "testpassword"

# [SITE]
SITE_NAME = "mysite"
# [MYSQL]
PASSWORD = "password"
MYSQL_ROOT_PASSWORD = "test123"
MYSQL_ROOT_NEW_PASSWORD = "test123"
MYSQL_ROOT_OLD_PASSWORD = "test123"
MYSQL_DBNAME = "testing"


PHPFPM_NGINX_SERVER = "echo \"upstream php {\n" \
                "\tserver unix:/tmp/php5-fpm.sock;\n" \
                "}\""

PMA_APACHE_SERVER = "echo \"<VirtualHost *:9000> \n" \
                    "\tServerAdmin webmaster@localhost\n" \
                    "\n" \
                    "\tDocumentRoot /usr/share/phpmyadmin\n" \
                    "\t<Directory />\n" \
                    "\t\tOptions FollowSymLinks\n" \
                    "\t\tAllowOverride All\n" \
        	        "\t</Directory>\n" \
        	        "\n" \
        	        "\tErrorLog \${APACHE_LOG_DIR}/error.log\n" \
        	        "\n" \
        	        "\t# Possible values include: debug, info, notice, warn, error, crit,\n" \
        	        "\t# alert, emerg.\n" \
        	        "\tLogLevel warn\n" \
        	        "\n" \
        	        "\tCustomLog \${APACHE_LOG_DIR}/access.log combined\n" \
        	        "</VirtualHost>\""

PMA_NGINX_SERVER =  "echo \"server {\n" \
                    "\tlisten 9000;\n" \
                    "\troot /usr/share/phpmyadmin;\n" \
                    "\tindex index.php;\n" \
                    "\tlocation / {\n" \
                    "\t\ttry_files \$uri \$uri/ /index.php =404;\n" \
                    "\t}\n" \
                    "\tlocation ~ \.php\$ {\n" \
                    "\t\ttry_files \$uri =404;\n" \
                    "\t\tfastcgi_split_path_info ^(.+\.php)(/.+)\$;\n" \
                    "\t\tfastcgi_pass unix:/tmp/php5-fpm.sock;\n" \
                    "\t\tfastcgi_index index.php;\n" \
                    "\t\tfastcgi_param SCRIPT_FILENAME /usr/share/phpmyadmin\$fastcgi_script_name;\n" \
                    "\t\tfastcgi_param DOCUMENT_ROOT /usr/share/phpmyadmin;\n" \
                    "\t\tfastcgi_intercept_errors on;\n" \
                    "\t\tinclude fastcgi_params;\n" \
                    "\t}\n" \
                    "}\""

WORDPRESS_APACHE_SERVER = "echo \"<VirtualHost *:80> \n" \
                    "\tServerAdmin webmaster@localhost\n" \
                    "\n" \
                    "\tDocumentRoot /home/"+SYS_USERNAME+"/public_html\n" \
                    "\t<Directory />\n" \
                    "\t\tOptions FollowSymLinks\n" \
                    "\t\tAllowOverride All\n" \
        	        "\t</Directory>\n" \
        	        "\n" \
        	        "\tErrorLog \${APACHE_LOG_DIR}/error.log\n" \
        	        "\n" \
        	        "\t# Possible values include: debug, info, notice, warn, error, crit,\n" \
        	        "\t# alert, emerg.\n" \
        	        "\tLogLevel warn\n" \
        	        "\n" \
        	        "\tCustomLog \${APACHE_LOG_DIR}/access.log combined\n" \
        	        "</VirtualHost>\""

WORDPRESS_NGINX_SERVER =  "echo \"server {\n" \
                    "\tlisten 80;\n" \
                    "\troot /home/"+SYS_USERNAME+"/public_html;\n" \
                    "\tindex index.php index.html;\n" \
                    "\tlocation / {\n" \
                    "\t\ttry_files \$uri \$uri/ /index.php =404;\n" \
                    "\t}\n" \
                    "\tlocation ~ \.php\$ {\n" \
                    "\t\ttry_files \$uri =404;" \
                    "\t\tfastcgi_split_path_info ^(.+\.php)(/.+)\$;\n" \
                    "\t\tfastcgi_pass unix:/tmp/php5-fpm.sock;\n" \
                    "\t\tfastcgi_index index.php;\n" \
                    "\t\tfastcgi_param SCRIPT_FILENAME /home/"+SYS_USERNAME+"/public_html\$fastcgi_script_name;\n" \
                    "\t\tfastcgi_param DOCUMENT_ROOT /home/"+SYS_USERNAME+"/public_html;\n" \
                    "\t\tfastcgi_intercept_errors on;\n" \
                    "\t\tinclude fastcgi_params;\n" \
                    "\t}\n" \
                    "}\""
MAGENTO_NGINX_SERVER = "echo \"server {\n" \
    "\tlisten 80 default;\n" \
    "\t## SSL directives might go here\n" \
    "\t#server_name www.DOMAIN.com *.DOMAIN.com; ## Domain is here twice so server_name_in_redirect will favour the www\n" \
    "\troot /home/"+SYS_USERNAME+"/public_html;\n" \
    "\tlocation / {\n" \
        "\t\tindex index.html index.php; ## Allow a static html file to be shown first\n" \
        "\t\ttry_files \$uri \$uri/ @handler; ## If missing pass the URI to Magento's front handler\n" \
        "\t\t#expires 30d; ## Assume all files are cachable\n" \
    "\t}\n" \
    "\t## These locations would be hidden by .htaccess normally\n" \
    "\tlocation ^~ /app/                { deny all; }\n" \
    "\tlocation ^~ /includes/           { deny all; }\n" \
    "\tlocation ^~ /lib/                { deny all; }\n" \
    "\tlocation ^~ /media/downloadable/ { deny all; }\n" \
    "\tlocation ^~ /pkginfo/            { deny all; }\n" \
    "\tlocation ^~ /report/config.xml   { deny all; }\n" \
    "\tlocation ^~ /var/                { deny all; }\n" \
    "\tlocation /var/export/ { ## Allow admins only to view export folder\n" \
        "\t\tauth_basic           \"Restricted\"; ## Message shown in login window\n" \
        "\t\tauth_basic_user_file htpasswd_magento; ## See /etc/nginx/htpassword_magento\n" \
        "\t\tautoindex            on;\n" \
    "\t}\n" \
     "\tlocation  /. { ## Disable .htaccess and other hidden files\n" \
        "\t\treturn 404;\n" \
    "\t}\n" \
    "\tlocation @handler { ## Magento uses a common front handler\n" \
        "\t\trewrite / /index.php;\n" \
    "\t}\n" \
    "\tlocation ~ .php/ { ## Forward paths like /js/index.php/x.js to relevant handler\n" \
        "\trewrite ^(.*.php)/ \$1 last;\n" \
    "\t}\n" \
    "\tlocation ~ .php$ { ## Execute PHP scripts\n" \
        "\t\tif (!-e \$request_filename) { rewrite / /index.php last; } ## Catch 404s that try_files miss\n" \
        "\t\texpires        off; ## Do not cache dynamic content\n" \
        "\t\tfastcgi_pass   unix:/tmp/php5-fpm.sock;\n" \
        "\t\tfastcgi_param  SCRIPT_FILENAME  /home/"+SYS_USERNAME+"/public_html\$fastcgi_script_name;\n" \
        "\t\tfastcgi_param  MAGE_RUN_CODE default; ## Store code is defined in administration > Configuration > Manage Stores\n" \
        "\t\tfastcgi_param  MAGE_RUN_TYPE store;\n" \
        "\t\tinclude        fastcgi_params; ## See /etc/nginx/fastcgi_params\n" \
    "\t}\n" \
"\t}\"" # sirf ek \n ne maar li thi yaad rakhnaa

MAGENTO_APACHE_SERVER = "echo \"<VirtualHost *:80>\n" \
        "\tServerAdmin webmaster@localhost\n" \
        "\tDocumentRoot /home/"+SYS_USERNAME+"/public_html\n" \
        "\t<Directory />\n" \
                "\t\tOptions FollowSymLinks\n "\
                "\t\tAllowOverride all\n" \
        "\t</Directory>\n" \
        "\tErrorLog \${APACHE_LOG_DIR}/error.log\n" \
        "\tLogLevel warn\n" \
        "\tCustomLog \${APACHE_LOG_DIR}/access.log combined\n" \
        "</VirtualHost>\""


logger = logging.getLogger("OMNIKNIGHT")

def logit(cmd, cmdoutput, cmderr):
    if cmd != "":
        logger.debug("command: " + cmd)
    if cmdoutput != "":
        logger.debug("command output: " + cmdoutput)
    if cmderr != "":
        logger.debug("command error: " + cmderr)


def check_nginx_present():
    cmd = "nginx -v 2>&1 > /dev/null | grep nginx -c"
    logger.debug(cmd)

    cmd = "nginx -v 2>&1 > /dev/null"
    a = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
    errmsg = a.stderr.read()
    if errmsg != "":
        logger.error(errmsg)

    a = Popen(["grep", "nginx", "-c"], stdin=a.stdout, stdout=PIPE, stderr=PIPE, shell=False)
    errmsg = a.stderr.read()
    if errmsg != "":
        logger.error(errmsg)
    cmdoutput = a.stdout.read()
    logit(cmd,cmdoutput,errmsg)
    if cmdoutput != "0":
        return True
    else:
        return False


def check_nginx_enabled():
    cmd = "pidof -c nginx"
    #logger.debug(cmd)

    a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False)
    errmsg = a.stderr.read()
    if errmsg != "":
        logger.error(errmsg)
    cmdoutput = a.stdout.read()
    logit(cmd,cmdoutput,errmsg)
    if cmdoutput == "":
        return False
    else:
        return True


def check_apache2_present():
    cmd = "apache2 -v 2>&1 > /dev/null | grep apache -c"
    logger.debug(cmd)

    cmd = "apache2 -v 2>&1 > /dev/null"
    a = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
    errmsg = a.stderr.read()
    if errmsg != "":
        logger.error(errmsg)

    a = Popen(["grep", "apache", "-c"], stdin=a.stdout, stdout=PIPE, stderr=PIPE, shell=False)
    errmsg = a.stderr.read()
    if errmsg != "":
        logger.error(errmsg)
    cmdoutput = a.stdout.read()
    logit(cmd,cmdoutput,errmsg)
    if cmdoutput != "0":
        return True
    else:
        return False


def check_apache2_enabled():
    cmd = "pidof -c apache2"

    a = Popen(cmd.split(), stdout=PIPE, stderr=PIPE, shell=False)
    errmsg = a.stderr.read()
    if errmsg != "":
        logger.error(errmsg)
    cmdoutput = a.stdout.read()
    logit(cmd,cmdoutput,errmsg)
    if cmdoutput == "":
        return False
    else:
        return True

#chkconfig --levels 235 mysqld on
#chkconfig --levels 235 apache2 on
#chkconfig --levels 235 nginx on
#chkconfig --levels 235 php-fpm on
#chkconfig --levels 235 varnish on
#chkconfig --levels 235 vsftpd on