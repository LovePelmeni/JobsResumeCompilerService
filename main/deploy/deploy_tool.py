import contextlib
import docker


class ClusterBuildFailed(Exception):
    pass

class InvalidContainerPayload(Exception):
    pass

class FailedToAddContainer(Exception):
    pass

class FailedToRemoveContainer(Exception):
    pass

class CreateNetworkFailed(Exception):
    pass


class DockerSwarmContainer(object):

    def __init__(self, docker_compose_file: bytes):
        self.compose_file = docker_compose_file

    def validate(self) -> bytes:
        pass

class ClusterCredentials(object):

    def __init__(self, cluster_credentials: typing.Dict[str, typing.Any],
    return_content_type: typing.Literal["xml", "json"]):
        self.cluster_credentials = cluster_credentials
        self.return_content_type = return_content_type

    def __call__(self, *args, **kwargs):
        pass

    def validate(self):
        pass

    def json(self) -> str:
        """
        / * Returns Cluster Configuration info as JSON object.
        """
        import json
        return json.dumps(str())

    def xml(self) -> str:
        """
        / * Returns Cluster Configuration Info converted to XML.
        """
        return str()


class DockerSwarmClusterDeployTool(object):

    def create_cluster(self) -> typing.Union[ClusterCredentials, ClusterBuildFailed]:
        pass

    def create_network(self) -> typing.Union[CreateNetworkFailed, None]:
        pass

    def add_container(self) -> typing.Union[FailedToAddContainer, None]:
        pass

    def remove_container(self) -> typing.Union[FailedToRemoveContainer, None]:
        pass

    def __init__(self, containers: typing.List[DockerSwarmContainer]):
        self.containers = containers

    def __call__(self, *args, **kwargs):
        return self.create_cluster()


@contextlib.contextmanager
def get_cluster_instance():
    yield DockerSwarmClusterDeployTool