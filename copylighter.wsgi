import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/copylighter/")

from copylighter import app as application
application.secret_key = '6cf34ed05e241ac72456425779220bfeaf3557ef8371bed4'