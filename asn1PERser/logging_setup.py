import os
import logging
import logging.config


def logging_setup():
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.cfg'))
    logging.getLogger('asn1perser').addHandler(logging.NullHandler())
