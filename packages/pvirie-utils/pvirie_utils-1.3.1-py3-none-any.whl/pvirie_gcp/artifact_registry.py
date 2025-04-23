from . import gcp
from googleapiclient.discovery import build
from google.cloud import artifactregistry_v1
import logging

# Access Cloud Storage

def get_session(credentials=None):
    if credentials is None:
        credentials = gcp.get_credentials()
    client = artifactregistry_v1.ArtifactRegistryClient(credentials=credentials)
    return client


class Docker_Registry:
    def __init__(self, project_id, location, repository, credentials=None):
        self.session = get_session(credentials)
        self.project_id = project_id
        self.location = location
        self.repository = repository

        self.artifact_registry = f"{self.location}-docker.pkg.dev/{self.project_id}/{self.repository}"


    def build_and_push_image(self, docker_client, image_name, tag, dockerfile_path, dockerfile_context):
        """
        Build and push a Docker image to Artifact Registry.
        :param docker_client: Docker client instance
        :param image_name: Name of the image
        :param tag: Tag for the image
        :param dockerfile_path: Path to the Dockerfile
        :param dockerfile_context: Context for the Docker build
        """
        # Build the Docker image
        docker_client.images.build(path=dockerfile_context, dockerfile=dockerfile_path, tag=image_name)
        local_tag = f"{image_name}:{tag}"
        built_image = docker_client.images.get(local_tag)
        logging.info(f"Successfully built image: {built_image.id}")

        # Tag the image for Artifact Registry
        artifact_registry_tag = f"{self.artifact_registry}/{image_name}:{tag}"
        docker_client.images.tag(local_tag, artifact_registry_tag)
        logging.info(f"Tagged image for Artifact Registry: {artifact_registry_tag}")

        # Push the Docker image to Artifact Registry
        docker_client.images.push(image_name, tag=tag)
        logging.info(f"Pushed image to Artifact Registry: {artifact_registry_tag}")

        return True
    

    def list_images(self):
        """
        List all images in the Artifact Registry repository.
        :return: List of image names
        """
        request = self.session.projects().locations().repositories().dockerImages().list(
            parent=f"projects/{self.project_id}/locations/{self.location}/repositories/{self.repository}"
        )
        response = request.execute()
        images = response.get('dockerImages', [])
        return [image['name'] for image in images]
    

    def delete_image(self, image_name):
        """
        Delete a Docker image from the Artifact Registry repository.
        :param image_name: Name of the image to delete
        """
        request = self.session.projects().locations().repositories().dockerImages().delete(
            name=f"projects/{self.project_id}/locations/{self.location}/repositories/{self.repository}/dockerImages/{image_name}"
        )
        response = request.execute()
        return response
    



