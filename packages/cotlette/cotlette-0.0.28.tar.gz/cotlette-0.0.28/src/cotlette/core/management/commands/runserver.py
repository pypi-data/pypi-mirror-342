import errno
import os
import re
import socket
import sys
from datetime import datetime
import uvicorn

from cotlette.conf import settings
from cotlette.core.management.base import BaseCommand, CommandError
from cotlette.utils.regex_helper import _lazy_re_compile
from cotlette.utils.version import get_docs_version

# Regular expression to validate IP address and port combinations
naiveip_re = _lazy_re_compile(
    r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address (e.g., 127.0.0.1)
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address (e.g., [::1])
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # Fully Qualified Domain Name (FQDN)
):)?(?P<port>\d+)$""",
    re.X,
)

# Logging configuration for Uvicorn
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(message)s",  # Default log format
            "datefmt": "%Y-%m-%d %H:%M:%S",  # Timestamp format
            "use_colors": True,  # Enable colored logs for better readability
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Log to standard output
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Log access logs to standard output
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}


class Command(BaseCommand):
    help = "Starts a lightweight web server for development purposes."

    stealth_options = ("shutdown_message",)
    suppressed_base_arguments = {"--verbosity", "--traceback"}

    default_addr = "127.0.0.1"  # Default IPv4 address
    default_addr_ipv6 = "::1"  # Default IPv6 address
    default_port = "8000"  # Default port number
    protocol = "http"

    def add_arguments(self, parser):
        """
        Define command-line arguments for the runserver command.
        """
        parser.add_argument(
            "addrport", nargs="?", help="Optional port number or ipaddr:port pair."
        )
        parser.add_argument(
            "--ipv6",
            "-6",
            action="store_true",
            dest="use_ipv6",
            help="Use IPv6 address instead of IPv4.",
        )
        parser.add_argument(
            "--reload",
            action="store_true",
            dest="use_reloader",
            help="Enable auto-reloading when source files change.",
        )

    def get_check_kwargs(self, options):
        """
        Validation is called explicitly each time the server reloads.
        """
        return {"tags": set()}

    def handle(self, *args, **options):
        """
        Main entry point for the command. Validates input and starts the server.
        """
        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            raise CommandError("You must set settings.ALLOWED_HOSTS if DEBUG is False.")

        self.use_ipv6 = options["use_ipv6"]
        if self.use_ipv6 and not socket.has_ipv6:
            raise CommandError("Your Python installation does not support IPv6.")

        self._raw_ipv6 = False

        # Parse the addrport argument if provided
        if not options["addrport"]:
            self.addr = ""
            self.port = self.default_port
        else:
            match = re.match(naiveip_re, options["addrport"])
            if not match:
                raise CommandError(
                    f'"{options["addrport"]}" is not a valid port number or address:port pair.'
                )
            self.addr, _ipv4, _ipv6, _fqdn, self.port = match.groups()

            if not self.port.isdigit():
                raise CommandError(f'"{self.port}" is not a valid port number.')

            if self.addr:
                if _ipv6:
                    # Strip brackets from IPv6 address
                    self.addr = self.addr[1:-1]
                    self.use_ipv6 = True
                    self._raw_ipv6 = True
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError(f'"{self.addr}" is not a valid IPv6 address.')

        # Set default address if none is provided
        if not self.addr:
            self.addr = self.default_addr_ipv6 if self.use_ipv6 else self.default_addr
            self._raw_ipv6 = self.use_ipv6

        # Start the server
        self.run(**options)

    def run(self, **options):
        """
        Run the Uvicorn server with the specified configuration.
        """
        use_reloader = options["use_reloader"]

        try:
            uvicorn.run(
                "core:app",  # Path to the ASGI application
                host=self.addr or self.default_addr,  # Host address
                port=int(self.port) or int(self.default_port),  # Port number
                reload=use_reloader,  # Enable auto-reloading
                log_level="debug" if settings.DEBUG else "info",  # Log level based on DEBUG setting
                access_log=True,  # Enable HTTP access logs
                log_config=LOGGING_CONFIG,  # Custom logging configuration
            )
        except KeyboardInterrupt:
            # Gracefully handle manual server shutdown (Ctrl+C)
            sys.exit(0)