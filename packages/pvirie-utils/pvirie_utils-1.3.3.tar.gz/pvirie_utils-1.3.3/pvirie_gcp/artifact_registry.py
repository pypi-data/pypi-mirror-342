from . import gcp
from google.cloud import artifactregistry
from google.api_core import exceptions as google_api_exceptions
import logging
import subprocess
import os

# Access Cloud Storage

def get_session(credentials=None):
    if credentials is None:
        credentials = gcp.get_credentials()
    client = artifactregistry.ArtifactRegistryClient(credentials=credentials)
    return client


class Docker_Registry:
    def __init__(self, project_id, location, repository, credentials=None):
        self.session = get_session(credentials)
        self.project_id = project_id
        self.location = location
        self.repository = repository

        host = f"{self.location}-docker.pkg.dev"
        self.artifact_registry = f"{host}/{self.project_id}/{self.repository}"

        """Sets ADC env var and runs 'gcloud auth configure-docker'."""
        key_file_path = os.getenv('GCP_CREDENTIALS')
        # Set environment variable for the subprocess call
        env_with_adc = os.environ.copy()
        env_with_adc['GOOGLE_APPLICATION_CREDENTIALS'] = key_file_path

        logging.info(f"Attempting to configure Docker authentication for {self.artifact_registry} using gcloud...")
        try:
            # gcloud auth activate-service-account --key-file=/path/to/your/service-account-key.json
            process = subprocess.run(
                ['gcloud', 'auth', 'activate-service-account', '--key-file', key_file_path],
                check=True,
                capture_output=True,
                text=True,
                env=env_with_adc # Pass the environment with the ADC variable set
            )
            logging.info("'gcloud auth activate-service-account' executed successfully.")
            logging.debug(f"gcloud stdout:\n{process.stdout}")
            if process.stderr:
                logging.warning(f"gcloud stderr:\n{process.stderr}")

        except FileNotFoundError:
            logging.error("'gcloud' command not found. Is the Google Cloud SDK installed and in PATH?")
        except subprocess.CalledProcessError as e:
            logging.error(f"'gcloud auth configure-docker' failed with exit code {e.returncode}")
            logging.error(f"Stderr:\n{e.stderr}")
            logging.error(f"Stdout:\n{e.stdout}")
            logging.error("Check if the service account key is valid and has permissions.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while running subprocess: {e}")


    def build_and_push_image(self, docker_client, image_name, tag, dockerfile_path, dockerfile_context):
        """
        Build and push a Docker image to Artifact Registry.
        """
        # Build the Docker image
        local_name_tag = f"{image_name}:{tag}"
        built_image, build_log_generator = docker_client.images.build(path=dockerfile_context, dockerfile=dockerfile_path, tag=local_name_tag, rm=True, forcerm=True)
        logging.info(f"Successfully built image: {image_name} {tag}")

        # Tag the image for Artifact Registry
        # Push the Docker image to Artifact Registry
        artifact_registry_name = f"{self.artifact_registry}/{image_name}"
        built_image.tag(repository=artifact_registry_name, tag=tag)
        docker_client.images.push(artifact_registry_name, tag=tag)
        logging.info(f"Pushed image to Artifact Registry: {artifact_registry_name}")

        return build_log_generator
    

    def list_images(self):
        parent_repo = self.session.repository_path(self.project_id, self.location, self.repository)
        logging.info(f"Listing packages (image names) in repository: {parent_repo}")

        try:
            package_pager = self.session.list_packages(parent=parent_repo)
            image_names = [pkg.name.split('/')[-1] for pkg in package_pager] # Extract just the image name
            return image_names
        except google_api_exceptions.PermissionDenied:
            logging.error(f"Permission denied listing packages in {parent_repo}. Need artifactregistry.reader role?")
        except Exception as e:
            logging.error(f"Error listing packages: {e}")
        return None


    def list_versions(self, image_name: str):
        parent_package = self.session.package_path(self.project_id, self.location, self.repository, image_name)
        logging.info(f"Listing versions for package: {parent_package}")

        try:
            # Use view=FULL to include tag information with versions
            request = artifactregistry.ListVersionsRequest(parent=parent_package, view=artifactregistry.VersionView.FULL)
            version_pager = self.session.list_versions(request=request)

            versions = []
            for version in version_pager:
                # Extract the digest and tags
                tags = version.related_tags
                tag = tags[0].name if tags else None
                parts = tag.split('/')
                if len(parts) > 1:
                    tag = parts[-1]
                # Extract the creation time
                created_time = version.create_time
                versions.append({'tag': tag, 'created_time': created_time})
            return versions
        
        except google_api_exceptions.NotFound:
            logging.error(f"Package (image) '{image_name}' not found in repository.")
        except google_api_exceptions.PermissionDenied:
            logging.error(f"Permission denied listing versions/tags for {parent_package}. Need artifactregistry.reader role?")
        except Exception as e:
            logging.error(f"Error listing versions/tags: {e}")
        return None