import asyncio
import re
from unittest.mock import Mock

import pytest
import pytest_asyncio
from jupyterhub.objects import Hub, Server
from kubernetes_asyncio import client
from kubernetes_asyncio.utils import create_from_yaml
from traitlets.config import Config

from kubetemplatespawner.spawner import KubeTemplateSpawner

from .conftest import ROOT_DIR

pytestmark = pytest.mark.asyncio(loop_scope="module")


@pytest_asyncio.fixture(scope="module")
async def hub_pod(k8s_client, k8s_namespace):
    await create_from_yaml(
        k8s_client,
        yaml_file=str(ROOT_DIR / "tests" / "resources" / "jupyterhub.yaml"),
        namespace=k8s_namespace,
    )
    pod_name = "jupyterhub"
    config_name = "jupyterhub-config"

    v1 = client.CoreV1Api(k8s_client)
    conditions = {}
    for i in range(int(90)):
        pod = await v1.read_namespaced_pod(namespace=k8s_namespace, name=pod_name)
        for condition in pod.status.conditions or []:
            conditions[condition.type] = condition.status

        if conditions.get("Ready") != "True":
            print(
                f"Waiting for pod {k8s_namespace}/{pod_name}; current status: {pod.status.phase}; {conditions}"
            )
            await asyncio.sleep(1)
        else:
            break

    if conditions.get("Ready") != "True":
        raise TimeoutError(
            f"pod {k8s_namespace}/{pod_name} failed to start: {pod.status}"
        )
    yield pod

    try:
        await v1.delete_namespaced_pod(pod_name, k8s_namespace)
    except Exception as e:
        print(f"Failed to delete pod/{pod_name}: {e}")
    try:
        await v1.delete_namespaced_config_map(config_name, k8s_namespace)
    except Exception as e:
        print(f"Failed to delete cm/{config_name}: {e}")


@pytest_asyncio.fixture(scope="module")
async def hub(hub_pod):
    """Return the jupyterhub Hub object for passing to Spawner constructors

    Ensures the hub_pod is running
    """
    yield Hub(ip=hub_pod.status.pod_ip, port=8081)


@pytest.fixture
def config(k8s_namespace):
    cfg = Config()
    cfg.KubeTemplateSpawner.namespace = k8s_namespace
    cfg.KubeTemplateSpawner.start_timeout = 180
    # prevent spawners from exiting early due to missing env
    cfg.KubeTemplateSpawner.environment = {
        "JUPYTERHUB_API_TOKEN": "test-secret-token",
        "JUPYTERHUB_CLIENT_ID": "ignored",
    }
    return cfg


class MockUser(Mock):
    name = "test-1"
    id = 123
    server = Server()

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def escaped_name(self):
        return self.name

    @property
    def url(self):
        return self.server.url


async def test_spawner(k8s_client, k8s_namespace, config, hub):
    spawner = KubeTemplateSpawner(
        hub=hub,
        user=MockUser(),
        template_path=str(ROOT_DIR / "example"),
        config=config,
        api_token="abc123",
        oauth_client_id="unused",
    )

    # empty spawner isn't running
    status = await spawner.poll()
    assert status == 0

    url = await spawner.start()
    assert re.match(r"http://\d+\.\d+\.\d+\.\d+:8888$", url)

    assert spawner._manifests

    pod_name = None
    pvc_name = None
    for m in spawner._manifests:
        if m["kind"] == "Pod":
            assert not pod_name
            pod_name = m["metadata"]["name"]
        if m["kind"] == "PersistentVolumeClaim":
            assert not pvc_name
            pvc_name = m["metadata"]["name"]
    assert pod_name
    assert pvc_name

    v1 = client.CoreV1Api(k8s_client)

    # verify the pod and PVC exist
    pods = await v1.list_namespaced_pod(namespace=k8s_namespace)
    pod_names = [p.metadata.name for p in pods.items]
    assert pod_name in pod_names

    pvcs = await v1.list_namespaced_persistent_volume_claim(namespace=k8s_namespace)
    pvc_names = [p.metadata.name for p in pvcs.items]
    assert pvc_name in pvc_names

    # pod should be running when start returns
    pod = await v1.read_namespaced_pod(namespace=k8s_namespace, name=pod_name)
    assert pod.status.phase == "Running"

    # verify poll while running
    status = await spawner.poll()
    assert status is None

    # TODO: check connection to spawner URL

    await spawner.stop()

    # verify pod is gone but PVC is kept
    pods = await v1.list_namespaced_pod(namespace=k8s_namespace)
    pod_names = [p.metadata.name for p in pods.items]
    assert pod_name not in pod_names

    pvcs = await v1.list_namespaced_persistent_volume_claim(namespace=k8s_namespace)
    pvc_names = [p.metadata.name for p in pvcs.items]
    assert pvc_name in pvc_names

    # verify exit status
    status = await spawner.poll()
    assert status == 0

    # check state has been cleared
    assert not spawner._manifests
    assert not spawner._connection_manifest

    # should delete PVC
    await spawner.delete_forever()

    pvcs = await v1.list_namespaced_persistent_volume_claim(namespace=k8s_namespace)
    pvc_names = [p.metadata.name for p in pvcs.items]
    assert pvc_name not in pvc_names
