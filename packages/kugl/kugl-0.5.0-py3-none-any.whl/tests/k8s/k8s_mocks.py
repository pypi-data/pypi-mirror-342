"""
Common utilities for Kubernetes unit testing.
"""

import json
import os
from functools import cache
from pathlib import Path
from typing import Optional, Tuple, Union, List

import yaml
from pydantic import Field, BaseModel, ConfigDict

from kugl.util import to_utc, UNIT_TEST_TIMEBASE


def kubectl_response(kind: str, output: Union[str, dict]):
    """
    Put a mock response for 'kubectl get {kind} ...' into the mock responses folder,
    to be found by an invocation of ./kubectl in a test.
    :param kind: e.g. "pods", "nodes, "jobs" etc
    :param output: A dict (will be JSON-serialized) or a string (will be trimmed)
    """
    if isinstance(output, dict):
        output = json.dumps(output)
    else:
        output = str(output).strip()
    folder = Path(os.getenv("KUGL_MOCKDIR"))
    folder.mkdir(exist_ok=True)
    folder.joinpath(kind).write_text(output)


class Taint(BaseModel):
    """Helper class for creating taints in test nodes"""
    key: str
    effect: str
    value: Optional[str] = None


class CGM(BaseModel):
    """Helper class for creating CPU/GPU/Memory resources in test containers"""
    model_config = ConfigDict(populate_by_name=True)
    cpu: Union[int, str, None] = None
    mem: Union[int, str, None] = Field(None, alias="memory")
    gpu: Union[int, str, None] = Field(None, alias="nvidia.com/gpu")


class Container(BaseModel):
    """Helper class for creating containers in test pods"""
    name: str = "main"
    command: List[str] = Field(default_factory = lambda: ["echo", "hello"])
    requests: Optional[CGM] = CGM(cpu=1, mem="10M")
    limits: Optional[CGM] = CGM(cpu=1, mem="10M")
    # Don't specify this in the constructor, it's a derived field
    resources: Optional[dict[str, CGM]] = None

    def model_post_init(self, *args):
        # Move requests and limits to resources so they match the Pod layout.
        self.resources = dict(requests=self.requests, limits=self.limits)
        self.requests = self.limits = None


def make_node(name: str, taints: Optional[List[Taint]] = None, labels: Optional[dict] = None):
    """
    Construct a Node dict from a generic chunk of node YAML that we can alter to simulate different
    responses from the K8S API.
    :param name: Node name
    """
    node = yaml.safe_load(_static_content("sample_node.yaml"))
    node["metadata"]["name"] = name
    node["metadata"]["uid"] = "uid-" + name
    if taints:
        node["spec"]["taints"] = [taint.model_dump(exclude_none=True) for taint in taints]
    if labels is not None:
        node["metadata"]["labels"] = labels
    return node


def make_pod(name: str,
             no_metadata: bool = False,
             name_at_root: bool = False,
             no_name: bool = False,
             is_daemon: bool = False,
             creation_ts: int = UNIT_TEST_TIMEBASE,
             deletion_ts: int = None,
             namespace: Optional[str] = None,
             node_name: Optional[str] = None,
             containers: List[Container] = [Container()],
             labels: Optional[dict] = None,
             phase: Optional[str] = "Running",
             ):
    """
    Construct a Pod dict from a generic chunk of pod YAML that we can alter to simulate different
    responses from the K8S API.

    :param no_metadata: Pretend there is no metadata
    :param name_at_root: Put the object name at top level, not in the metadata
    :param no_name: Pretend there is no object name
    """
    obj = yaml.safe_load(_static_content("sample_pod.yaml"))
    if name_at_root:
        obj["name"] = name
    elif not no_name:
        obj["metadata"]["name"] = name
    obj["metadata"]["uid"] = "uid-" + name
    if no_metadata:
        del obj["metadata"]
    if is_daemon:
        obj["metadata"]["ownerReferences"] = [{"kind": "DaemonSet"}]
    if namespace:
        obj["metadata"]["namespace"] = namespace
    if node_name:
        obj["spec"]["nodeName"] = node_name
    if labels is not None:
        obj["metadata"]["labels"] = labels
    if creation_ts and not no_metadata:
        obj["metadata"]["creationTimestamp"] = to_utc(creation_ts)
    if deletion_ts and not no_metadata:
        obj["metadata"]["deletionTimestamp"] = to_utc(deletion_ts)
    obj["spec"]["containers"] = [c.model_dump(by_alias=True, exclude_none=True) for c in containers]
    obj["status"]["phase"] = phase
    return obj


def make_job(name: str,
             namespace: str = None,
             active_count: Optional[int] = None,
             condition: Optional[Tuple[str, str, Optional[str]]] = None,
             suspend: bool = False,
             pod: Optional[dict] = None,
             labels: Optional[dict] = None,
             pod_labels: Optional[dict] = None,
             ):
    """
    Construct a Job dict from a generic chunk of pod YAML that we can alter to simulate different
    responses from the K8S API.

    :param name: Job name
    :param active_count: If present, the number of active pods
    :param condition: If present, a condition tuple (type, status, reason)
    :param suspend: If true, mark the job suspended and with no status
    :param: pod: If present, a pod dict to be used as the template, returned from make_pod
    """
    obj = yaml.safe_load(_static_content("sample_job.yaml"))
    obj["metadata"]["name"] = name
    obj["metadata"]["uid"] = "uid-" + name
    obj["metadata"]["labels"]["job-name"] = name
    if namespace is not None:
        obj["metadata"]["namespace"] = namespace
    if len([x for x in [active_count, condition, suspend] if x]) > 1:
        raise ValueError("Only one of active_count, condition, or suspend can be set")
    if active_count is not None:
        obj["status"]["active"] = active_count
    elif condition is not None:
        obj["status"]["conditions"] = [{"type": condition[0], "status": condition[1], "reason": condition[2]}]
    elif suspend:
        obj["spec"]["suspend"] = True
        del obj["status"]
    if labels is not None:
        obj["metadata"]["labels"] = labels
    if pod is not None:
        obj["spec"]["template"]["spec"] = pod["spec"]
    if pod_labels is not None:
        obj["spec"]["template"]["metadata"]["labels"] = pod_labels
    return obj


@cache
def _static_content(filename: str):
    return Path(__file__).parent.parent.joinpath("static", filename).read_text()

