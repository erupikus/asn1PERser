import os
import logging
import logging.config


def asn1perser_logging_setup(handler=logging.NullHandler(), level=logging.INFO):
    default_formatter = logging.Formatter("%(name)s:%(filename)s:%(lineno)-4d - %(levelname)-7s - %(message)s")
    handler.setFormatter(handler.formatter if handler.formatter else default_formatter)

    asn1perser_root = logging.getLogger("asn1perser")
    asn1perser_root.propagate = False
    asn1perser_root.setLevel(level)
    asn1perser_root.addHandler(handler)
