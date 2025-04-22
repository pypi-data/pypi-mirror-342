"""
Describes the full command-line interface provided by MetGenC. The commandline
operations described here are implemented by other modules within the
`nsidc.metgen` package.
"""

import logging

import click

from nsidc.metgen import config, constants, metgen

LOGGER = logging.getLogger(constants.ROOT_LOGGER)


@click.group(epilog="For detailed help on each command, run: metgenc COMMAND --help")
@click.version_option(package_name="nsidc-metgenc")
def cli():
    """The metgenc utility allows users to create granule-level
    metadata, stage granule files and their associated metadata to
    Cumulus, and post CNM messages."""
    pass


@cli.command()
@click.option("-c", "--config", help="Path to configuration file to create or replace")
def init(config):
    """Populates a configuration file based on user input."""
    click.echo(metgen.banner())
    config = metgen.init_config(config)
    click.echo(f"Initialized the metgen configuration file {config}")


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_filename",
    help="Path to configuration file to display",
    required=True,
)
def info(config_filename):
    """Summarizes the contents of a configuration file."""
    click.echo(metgen.banner())
    configuration = config.configuration(
        config.config_parser_factory(config_filename), {}
    )
    metgen.init_logging(configuration)
    configuration.show()


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_filename",
    help="Path to configuration file",
    required=True,
)
@click.option(
    "-t",
    "--type",
    "content_type",
    help="JSON content type",
    default="cnm",
    show_default=True,
)
def validate(config_filename, content_type):
    """Validates the contents of local JSON files."""
    click.echo(metgen.banner())
    configuration = config.configuration(
        config.config_parser_factory(config_filename), {}
    )
    metgen.init_logging(configuration)
    metgen.validate(configuration, content_type)


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_filename",
    help="Path to configuration file",
    required=True,
)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    required=False,
    default=None,
    help="Don't stage files on S3 or publish messages to Kinesis",
)
@click.option(
    "-e",
    "--env",
    help="environment",
    default=constants.DEFAULT_CUMULUS_ENVIRONMENT,
    show_default=True,
)
@click.option(
    "-n",
    "--number",
    help="Process at most 'count' granules.",
    metavar="count",
    required=False,
    default=constants.DEFAULT_NUMBER,
)
@click.option(
    "-wc",
    "--write-cnm",
    is_flag=True,
    required=False,
    default=None,
    help="Write CNM messages to files.",
)
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    required=False,
    default=None,
    help="Overwrite existing UMM-G files.",
)
def process(config_filename, dry_run, env, number, write_cnm, overwrite):
    """Processes science data files based on configuration file contents."""
    click.echo(metgen.banner())
    overrides = {
        "dry_run": dry_run,
        "number": number,
        "overwrite_ummg": overwrite,
        "write_cnm_file": write_cnm,
    }
    try:
        configuration = config.configuration(
            config.config_parser_factory(config_filename), overrides, env
        )
        metgen.init_logging(configuration)
        configuration.show()
        config.validate(configuration)
        metgen.process(configuration)
    except config.ValidationError as e:
        logger = logging.getLogger(constants.ROOT_LOGGER)
        logger.error("\nThe configuration is invalid:")
        for error in e.errors:
            logger.error(f"  * {error}")
        exit(1)
    except Exception as e:
        logger = logging.getLogger(constants.ROOT_LOGGER)
        logger.error("\nUnable to process data: " + str(e))
        exit(1)
    click.echo("Processing complete")


if __name__ == "__main__":
    cli()
