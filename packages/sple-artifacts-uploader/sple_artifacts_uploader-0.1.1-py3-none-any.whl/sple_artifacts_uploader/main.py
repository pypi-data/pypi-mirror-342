import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from py_app_dev.core.exceptions import UserNotificationException
from py_app_dev.core.logging import logger, setup_logger, time_it

from sple_artifacts_uploader import __version__
from sple_artifacts_uploader.artifact_uploader import ArtifactUploader

package_name = "sple_artifacts_uploader"

app = typer.Typer(name=package_name, help="An spl-core extension to upload artifacts", no_args_is_help=True)


@app.callback(invoke_without_command=True)
def version(
    version: bool = typer.Option(None, "--version", "-v", is_eager=True, help="Show version and exit."),
) -> None:
    """
    Show the version of the application.

    Args:
        version (bool = typer.Option): Command flag to show the version.

    Raises:
        typer.Exit: Exits the application after displaying the version.

    """
    if version:
        typer.echo(f"{package_name} {__version__}")
        raise typer.Exit()


@app.command()
@time_it("upload")
def upload_file(
    artifact_path: Annotated[Path, typer.Option(..., "--artifact-path", help="Path to the file to upload.")],
    destination_url: Annotated[str, typer.Option(..., "--destination-url", help="Destination URL for the upload.")],
    username: Annotated[str, typer.Option(..., "--username", help="Username for authentication.")],
    password: Annotated[str, typer.Option(..., "--password", help="Password for authentication.")],
    timeout: Annotated[Optional[int], typer.Option("--timeout", help="Timeout for the upload in [s].")] = 10,
) -> None:
    """
    Upload a file to a specified destination URL.

    Args:
        artifact_path (Annotated[Path, typer.Option): Path to the file to upload.
        destination_url (Annotated[str, typer.Option): Destination URL for the upload.
        username (Annotated[str, typer.Option): Username for authentication.
        password (Annotated[str, typer.Option): Password for authentication.
        timeout (Annotated[int, typer.Option, optional): Timeout for the upload in seconds. Default is 10 seconds.

    """
    ArtifactUploader().upload_file(artifact_path, destination_url, username, password, timeout)


def main() -> None:
    """Main entry point for the application."""
    try:
        setup_logger()
        app()
    except UserNotificationException as e:
        logger.error(f"{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
