from pathlib import Path
from typing import Optional

import requests
from py_app_dev.core.docs_utils import fulfills
from py_app_dev.core.logging import logger


class ArtifactUploader:
    """Class to handle the uploading of artifacts."""

    def __init__(self) -> None:
        """Constructor for the ArtifactUploader class."""
        self.logger = logger.bind()

    @fulfills("REQ-ARTIFACTS-UPLOADER-1.0")
    def upload_file(self, artifact_path: Path, destination_url: str, username: str, password: str, timeout: Optional[int] = 10) -> None:
        """
        Upload a single file to a specified destination URL.

        Args:
            artifact_path (Path): Path to the file to upload.
            destination_url (str): Destination URL for the upload.
            username (str): Username for authentication.
            password (str): Password for authentication.
            timeout (Optional[int]): Timeout for the upload in seconds. Default is 10 seconds.

        """
        self.logger.info(f"Uploading artifact from {artifact_path} to {destination_url}")
        # Read file in binary mode and properly close it after block execution
        with open(artifact_path, "rb") as file:
            try:
                # Upload to Artifactory is done via PUT request
                response = requests.put(destination_url, data=file, auth=(username, password), timeout=timeout)
                # Check if the response status code indicates success (2xx)
                if 200 <= response.status_code < 300:
                    self.logger.info("Upload successful!")
                else:
                    self.logger.warning(f"Failed to upload. Status code: {response.status_code}")
            except requests.exceptions.Timeout:
                self.logger.warning("Upload failed due to a timeout.")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"An error occurred during upload: {e}")
