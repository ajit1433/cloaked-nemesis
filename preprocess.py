__author__ = 't'
TEST = 0

import os
import sys
import logging
import logging.config
from subprocess import Popen, PIPE, call

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=True)


class preprocess:
    def check_root(self):
        if os.geteuid() != 0:
            # print >> sys.stderr, "This script needs to be run as root"
            logger.error("This script needs to be run as root")
            sys.exit(1)

        else:
            logger.info("ROOT_CHK_SUCCESS")




if TEST == 1:
    ns = preprocess()
    ns.check_root()
