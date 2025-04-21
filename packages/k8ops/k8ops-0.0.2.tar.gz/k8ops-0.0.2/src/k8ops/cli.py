import logging

import click

from k8ops import __version__
from k8ops.cluster import cluster


class ClickEchoHandler(logging.Handler):
    """Custom logging handler to output logs to Click's echo function."""

    def emit(self, record):
        try:
            msg = self.format(record)
            # If the log level is WARNING or higher, print to stderr
            # Otherwise, print to stdout
            if record.levelno >= logging.WARNING:
                click.echo(msg, err=True)
            else:
                click.echo(msg)
        except Exception:
            self.handleError(record)


def configure_logging() -> None:
    # Clear other handlers to prevent duplicate output
    logging.getLogger().handlers.clear()

    # Create and add ClickEchoHandler
    handler = ClickEchoHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """K8Ops CLI - A command line tool for Kubernetes operations."""
    ctx.ensure_object(dict)
    ctx.obj["version"] = __version__
    configure_logging()


# Register subcommands
cli.add_command(cluster)

if __name__ == "__main__":
    cli()
