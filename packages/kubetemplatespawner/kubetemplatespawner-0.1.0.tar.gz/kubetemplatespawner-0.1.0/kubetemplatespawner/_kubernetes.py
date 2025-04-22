# These are seperated from the spawner to make testing easier

import asyncio
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache
from typing import (
    Any,
)

from kubernetes_asyncio import client, config, watch
from kubernetes_asyncio.config import ConfigException
from kubernetes_asyncio.dynamic import DynamicClient
from kubernetes_asyncio.dynamic.exceptions import ResourceNotFoundError
from kubernetes_asyncio.dynamic.resource import ResourceInstance
from tornado.log import app_log as log

# YamlT = dict[str, Any]
YamlT = Any

ManifestSummary = namedtuple("ManifestSummary", "api_version kind name namespace")


def manifest_summary(manifest: YamlT) -> ManifestSummary:
    api_version = manifest["apiVersion"]
    kind = manifest["kind"]
    metadata = manifest.get("metadata", {})
    name = metadata.get("name")
    namespace = metadata.get("namespace", "default")
    return ManifestSummary(api_version, kind, name, namespace)


@lru_cache()
def load_config(config_file: str | None = None) -> None:
    if not config_file:
        try:
            config.load_incluster_config()
            return
        except ConfigException:
            pass

    def load_sync():
        asyncio.run(config.load_kube_config(config_file=config_file))

    with ThreadPoolExecutor(1) as pool:
        future = pool.submit(load_sync)
        # blocking wait
        future.result()


def not_found(resource_status: ResourceInstance):
    return not resource_status or resource_status.kind == "Status"


def object_is_ready(obj: ResourceInstance) -> bool:
    """
    Is a K8s object "ready"?
    There isn't a standard way to tell.

    https://github.com/helm/helm/blob/v3.17.3/pkg/kube/ready.go#L85
    """
    if not_found(obj):
        return False

    kind = obj.kind
    name = obj.metadata.get("name")
    status = obj.get("status", {})
    conditions = status.get("conditions", [])

    if kind == "Pod":
        for c in conditions:
            if c.get("type") == "Ready" and c.get("status") == "True":
                return True
        return False
    if kind == "DaemonSet":
        if obj.metadata.generation != status.observedGeneration:
            return False
        return status.get("desiredNumberScheduled") == status.get("numberReady")
    if kind == "Deployment":
        if obj.metadata.generation != status.observedGeneration:
            return False
        for c in conditions:
            if c.get("type") == "Available" and c.get("status") == "True":
                return True
        return False
    if kind == "PersistentVolumeClaim":
        return status.get("phase") == "Bound"
    if kind == "Service":
        return bool(obj.spec.clusterIP)
    if kind in ("ConfigMap", "Secret"):
        return True

    # else if object exists assume it's ready
    log.warning(f"Unable to check if kind {kind}/{name} is ready")
    return True


async def k8s_resource(dyn_client: DynamicClient, api_version: str, kind: str) -> Any:
    try:
        resource = await dyn_client.resources.get(api_version=api_version, kind=kind)
        return resource
    except ResourceNotFoundError:
        log.exception(f"Resource not found: {api_version}/{kind}")
        raise


async def wait_for_ready(
    dyn_client: DynamicClient, obj: ResourceInstance, timeout: int
) -> None:
    api_version = obj.apiVersion
    kind = obj.kind
    name = obj.metadata.name
    namespace = getattr(obj.metadata, "namespace", "default")
    if kind == "Status":
        raise RuntimeError(f"Unexpected status: {obj}")
    resource = await k8s_resource(dyn_client, api_version, kind)

    async def is_ready() -> bool:
        try:
            refreshed = await resource.get(name=name, namespace=namespace)
            return object_is_ready(refreshed)
        except Exception as e:
            log.info(e)
        return False

    log.info(f"Waiting for {kind}/{name} to be ready (timeout={timeout})...")
    for _ in range(timeout):
        if await is_ready():
            log.info(f"{kind}/{name} is ready")
            return
        await asyncio.sleep(1)
    raise RuntimeError(f"Timeout ({timeout}) waiting for {kind}/{name}")


# kind, name, namespace
async def stream_events(
    events: asyncio.Queue | None,
    objects: list[ManifestSummary],
    since: datetime,
    timeout: int,
) -> None:
    log.info(f"Watching {objects} since {since} for {timeout} s")
    namespaces = set(obj.namespace for obj in objects)
    if len(namespaces) > 1:
        raise ValueError("All objects must be in the same namespace")
    namespace = namespaces.pop()
    obj_match = set((obj.kind, obj.name) for obj in objects)
    v1 = client.CoreV1Api()
    w = watch.Watch()

    try:
        async for event in w.stream(
            v1.list_namespaced_event, namespace=namespace, timeout_seconds=timeout
        ):
            involved = event["object"].involved_object
            timestamp = event["object"].event_time or event["object"].last_timestamp
            if not timestamp:
                log.error(f"No timestamp in {event['object']}")
            if (involved.kind, involved.name) in obj_match:
                m = f"{timestamp} {involved.kind}/{involved.name} {event['object'].message}"
                if timestamp and timestamp < since:
                    log.info(f"Ignoring old Event: {m}")
                else:
                    log.info(f"Event: {m}")
                    if events:
                        events.put_nowait({"message": m})
    except Exception:
        log.exception(f"Event watch error for {obj_match} ns={namespace}")


async def deploy_manifest(
    dyn_client: DynamicClient, manifest: YamlT, timeout: int
) -> None:
    s = manifest_summary(manifest)

    resource = await k8s_resource(dyn_client, s.api_version, s.kind)

    try:
        obj = await resource.get(name=s.name, namespace=s.namespace)
    except Exception:
        obj = None
    if obj and obj.kind == s.kind:
        log.info(f"Updating {s.api_version}/{s.kind}/{s.name}")
        obj = await resource.patch(body=manifest, name=s.name, namespace=s.namespace)
    elif not_found(obj):
        log.info(f"Creating {s.api_version}/{s.kind}/{s.name}")
        obj = await resource.create(body=manifest, namespace=s.namespace)
    else:
        raise RuntimeError(f"Unexpected status: {obj}")

    if not obj:
        raise RuntimeError(f"No object created: {s}")

    await wait_for_ready(dyn_client, obj, timeout)


async def delete_manifest(
    dyn_client: DynamicClient,
    manifest: YamlT | ManifestSummary,
    timeout: int,
) -> None:
    if isinstance(manifest, ManifestSummary):
        s = manifest
    else:
        s = manifest_summary(manifest)
    resource = await k8s_resource(dyn_client, s.api_version, s.kind)

    try:
        log.info(f"Deleting {s}")
        await resource.delete(name=s.name, namespace=s.namespace)

        if timeout:
            for _ in range(timeout):
                obj = await resource.get(name=s.name, namespace=s.namespace)
                if not_found(obj):
                    log.info(f"Deleted {s}")
                    return
                await asyncio.sleep(1)
            log.error(f"Timeout waiting for {s} to be deleted")
        else:
            log.info(f"Delete request sent for {s}")
    except Exception:
        log.exception(f"Failed to delete {s}")
        raise


async def get_deletions_by_labels(
    dyn_client: DynamicClient,
    api_version: str,
    kind: str,
    namespace: str,
    labels: dict[str, str],
    annotations: dict[str, str],
) -> list[ResourceInstance]:
    to_delete: list[ResourceInstance] = []

    objs = await get_resource_by_labels(
        dyn_client, api_version, kind, labels, namespace
    )
    for obj in objs:
        obj_annotations = obj.metadata.get("annotations", {})
        for k, v in annotations.items():
            if obj_annotations.get(k) != v:
                s = manifest_summary(obj)
                log.info(f"Not deleting {s}: Missing annotation {k}={v}")
                break
        else:
            to_delete.append(obj)

    return to_delete


async def get_resource_by_name(
    dyn_client, api_version, kind, name, namespace="default"
) -> ResourceInstance | None:
    resource = await k8s_resource(dyn_client, api_version, kind)
    obj = await resource.get(name=name, namespace=namespace)
    if obj.kind == "Status":
        if obj.code == 404:
            return None
        raise RuntimeError(f"Unexpected status: {obj}")
    return obj


async def get_resource_by_labels(
    dyn_client,
    api_version,
    kind,
    labels: dict[str, str] = {},
    namespace="default",
) -> list[ResourceInstance]:
    resource = await k8s_resource(dyn_client, api_version, kind)
    label_selector = ",".join(f"{k}={v}" for (k, v) in labels.items())

    obj = await resource.get(label_selector=label_selector, namespace=namespace)
    if not obj.kind.endswith("List"):
        raise RuntimeError(f"Unexpected object: {obj}")
    return obj.items
