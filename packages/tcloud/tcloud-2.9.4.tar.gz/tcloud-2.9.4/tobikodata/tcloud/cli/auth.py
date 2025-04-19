import json
import typing as t

import click

from tobikodata.tcloud.auth import tcloud_sso

SSO = tcloud_sso()


@click.group()
def auth() -> None:
    """
    Tobiko Cloud Authentication
    """


@auth.command()
def status() -> None:
    """Display current session status"""
    SSO.status()


@auth.command(hidden=True)
def token() -> None:
    """Copy the current token onto clipboard"""
    SSO.copy_token()


@auth.command(hidden=True)
@click.option("-u", "--undo", required=False, is_flag=True, help="Remove current impersonation")
@click.option(
    "-o",
    "--org",
    required=False,
    help="The Tobiko org to use",
    default="*",
)
@click.option(
    "-p",
    "--project",
    required=False,
    help="The Tobiko project to use",
    default="*",
)
@click.option(
    "-l",
    "--level",
    required=False,
    type=click.Choice(["viewer", "developer", "admin"], case_sensitive=False),
    help="The permission level to use",
    default="admin",
)
@click.option(
    "-n",
    "--name",
    required=False,
    help="The name to include in the impersonated token",
)
@click.option(
    "-e",
    "--email",
    required=False,
    help="The email to include in the impersonated token",
)
def impersonate(
    undo: bool,
    org: str,
    project: str,
    level: str,
    name: t.Optional[str] = None,
    email: t.Optional[str] = None,
) -> None:
    """Impersonate another user that has a subset of your own permissions"""
    if undo:
        SSO.undo_impersonation()
        return

    SSO.impersonate(scope=f"tbk:scope:project:{org}:{project}:{level}", name=name, email=email)


@auth.command()
def refresh() -> None:
    """Refresh your current token"""
    SSO.refresh_token()


@auth.command()
def logout() -> None:
    """Logout of any current session"""
    SSO.logout()


@auth.command()
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Create a new session even when one already exists.",
)
def login(force: bool) -> None:
    """Login to Tobiko Cloud"""
    SSO.login() if force else SSO.id_token(login=True)
    SSO.status()


### Methods for VSCode
@auth.group(hidden=True)
def vscode() -> None:
    """Commands for VSCode integration"""
    pass


@vscode.command()
def login_url() -> None:
    """
    Login to Tobiko Cloud.

    This returns a JSON object with the following fields:
    - url: The URL to login open
    """
    url, verifier_code = SSO.vscode_get_login_url()
    print(json.dumps({"url": url, "verifier_code": verifier_code}))


@vscode.command()
@click.argument("code_verifier", type=str, required=True)
def start_server(code_verifier: str) -> None:
    """
    Start the server to catch the redirect from the browser.
    """
    auth = tcloud_sso(code_verifier=code_verifier)
    auth.vscode_start_server()


@vscode.command("status")
def vscode_status() -> None:
    """
    Auth status for logged in
    """
    logged_in, id_token = SSO.vscode_status()
    print(json.dumps({"is_logged_in": logged_in, "id_token": id_token}))
