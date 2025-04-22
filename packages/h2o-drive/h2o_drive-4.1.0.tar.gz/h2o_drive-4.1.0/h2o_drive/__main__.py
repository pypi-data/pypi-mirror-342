import asyncio
import functools
import json
import textwrap
import urllib.parse

import click
import h2o_discovery

import h2o_drive.connection


def async_command(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.group()
def aws():
    """Commands providing various compatibility with AWS SDKs."""
    pass


@aws.command()
@async_command
async def credentials():
    """Authenticate with drive and returns the credentials in the JSON format
    compatible with credential_process in AWS CLI configuration.
    """
    discovery = await h2o_discovery.discover_async()

    session = h2o_drive.connection.create_session(discovery=discovery)
    credentials = await session.get_credentials()
    frozen = await credentials.get_frozen_credentials()

    print_credentials(credentials=frozen)


def print_credentials(credentials):
    credentials_json = {
        "Version": 1,
        "AccessKeyId": credentials.access_key,
        "SecretAccessKey": credentials.secret_key,
        "SessionToken": credentials.token,
    }
    print(json.dumps(credentials_json))


@aws.command()
@async_command
@click.option(
    "--name",
    help="Name of the output profile, when not provided, generated name is used.",
    required=False,
    type=str,
)
@click.option(
    "--legacy-userdrive",
    "legacy_userdrive",
    help="When used the profile will be configured to access legacy userdrive.",
    is_flag=True,
)
@click.pass_context
async def profile(ctx: click.Context, name: str, legacy_userdrive: bool):
    """Outputs AWS CLI configuration profile for accessing H2O Drive."""

    discovery = await h2o_discovery.discover_async()
    environment = discovery.environment.h2o_cloud_environment
    version = discovery.environment.h2o_cloud_version
    svc_key = "workspacedrive"
    profile_suffix = "-drive"
    if legacy_userdrive:
        svc_key = "userdrive"
        profile_suffix = "-userdrive"

    try:
        sts_svc = discovery.services["drive-sts"]
        s3_svc = discovery.services[svc_key]
    except KeyError:
        raise click.ClickException(
            f"Environment {environment} ({version}) does not seem to have required"
            " Drive version. Please contact H2O.ai support or admins."
        ) from None

    env_uri = urllib.parse.urlparse(environment)
    profile = name or f"h2o-{env_uri.hostname}"

    profile += profile_suffix
    credentials_process = ctx.find_root().command_path + " aws credentials"
    ini = f"""
    [profile {profile}]
    credential_process = {credentials_process}
    services = {profile}

    [services {profile}]
    sts =
        endpoint_url = {sts_svc.uri}
    s3 =
        endpoint_url = {s3_svc.uri}
        addressing_style = path
    """
    print(textwrap.dedent(ini))


if __name__ == "__main__":
    cli()
