import click

from .drain import drain
from .summary import summary


@click.group()
def cluster():
    """K8Ops Cluster Management CLI"""
    pass


# Add other cluster-related commands here
cluster.add_command(summary)
cluster.add_command(drain)
