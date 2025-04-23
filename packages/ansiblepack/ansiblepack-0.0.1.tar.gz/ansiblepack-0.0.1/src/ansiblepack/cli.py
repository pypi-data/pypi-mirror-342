import argparse
import logging
import os
import sys

import ansiblepack.pack

log = logging.getLogger(__name__)


def setup_logging(log_level="info"):
    """
    Setup logging for the project
    """
    root_logger = logging.getLogger()

    # Clear existing configuration
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Validate and set level
    level = getattr(logging, log_level.upper())
    root_logger.setLevel(level)

    # Configure handlers
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s [%(name)-17s][%(levelname)-8s:%(lineno)-4d][%(processName)s:%(process)d] %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)


def cli():
    parser = argparse.ArgumentParser(
        description="Ansible Module Packager: A CLI tool for creating self-contained, distributable Ansible modules"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        help="Sets the logging level",
        default="info",
    )

    subparser = parser.add_subparsers()
    create_parser = subparser.add_parser("create")
    create_parser.add_argument(
        "-n",
        "--name",
        help="Name of the package to create.",
    )
    create_parser.add_argument(
        "-d",
        "--dest",
        help="Destination of the package. Default is current working dir.",
        default=os.getcwd(),
    )
    create_parser.add_argument(
        "-m",
        "--modules",
        type=lambda x: x.split(","),
        help="Comma-separated list of modules",
        default=None,
    )
    create_parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        help="Glob pattern to match the module name",
        default=None,
    )

    create_parser.set_defaults(func=ansiblepack.pack.pack)

    opts = parser.parse_args()
    setup_logging(log_level=opts.log_level)
    opts.func(opts)
