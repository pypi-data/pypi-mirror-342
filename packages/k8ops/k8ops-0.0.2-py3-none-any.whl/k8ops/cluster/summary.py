import json
import logging
import math
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import click

from k8ops.types import (
    Address,
    AddressList,
    Condition,
    ConditionList,
    Image,
    ImageList,
    Node,
    NodeList,
    NodeResource,
    Pod,
    PodList,
    Resource,
    Taint,
    TaintList,
    Toleration,
    TolerationList,
)
from k8ops.utils.parser import parse_cpu, parse_pod_count, parse_storage
from k8ops.utils.table import Column, print_table


def get_node_attr(attr: str) -> Callable[[Any, Node], str]:
    """Get a function to retrieve an attribute from a Node object"""

    def get_attr(val: Any, node: Node) -> str:
        return getattr(node, attr, "")

    return get_attr


def format_dict_in_table(val: Dict[str, str], _: Node) -> str:
    """Format a dictionary into a string for table display"""
    if len(val) == 0:
        return "-"

    display = f"{list(val.keys())[0]}: {list(val.values())[0]}"
    if len(val) > 1:
        display += f" +{len(val) - 1}"
    return display


def len_of(val: Any, _: Any) -> str:
    """Get the length of a value for table display"""
    if hasattr(val, "__len__"):
        return str(len(val))
    return "NaN"


NODE_HEADERS = [
    "Node",
    "Allocatable",
    "Capacity",
    "Metrics",
    Column("Pods", formatter=len_of),
    Column("Images", formatter=len_of),
]

NODE_HEADERS_WIDE = NODE_HEADERS + [
    Column("Labels", formatter=len_of),
    Column("Annotations", formatter=len_of),
    Column("Taints", formatter=len_of),
    Column("OS", virtual=True, formatter=get_node_attr("operatingSystem")),
    Column("Arch", virtual=True, formatter=get_node_attr("architecture")),
]

POD_HEADERS = ["Namespace", "Name", "Node", "Requests", "Limits", "Metrics"]

POD_HEADERS_WIDE = POD_HEADERS + [
    "ControlledBy",
    "Priority",
    Column("Tolerations", formatter=len_of),
]

IMAGE_HEADERS = ["Name", Column("Size", suffix="(MB)")]


KUBECTL = "kubectl"


def kubectl(args: List[str], exit_on_error: bool = True) -> str:
    """Run kubectl command and return output"""
    command = [KUBECTL] + args
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {e}")
        if exit_on_error:
            sys.exit(1)
        raise e


def collect_pod_list() -> PodList:
    """Collect information for all Pods"""

    # collect all pods metrics first, store it into a Dict, use the namespace/name as key, Resource as value
    top_pods_metrics = {}
    try:
        top_pods_output = kubectl(["top", "pods", "-A", "--no-headers"], exit_on_error=False)
        top_pods_lines = top_pods_output.splitlines()
        for line in top_pods_lines:
            parts = line.split()
            namespace = parts[0]
            name = parts[1]
            cpu = parse_cpu(parts[2])
            memory = parse_storage(parts[3])
            top_pods_metrics[f"{namespace}/{name}"] = Resource(cpu=cpu, memory=memory)
    except Exception:
        top_pods_metrics = {}

    # collect all pods info
    pod_list = PodList()
    output = kubectl(["get", "pods", "-A", "-o", "json"])
    pods = json.loads(output)["items"]

    for pod in pods:
        namespace = pod["metadata"]["namespace"]
        name = pod["metadata"]["name"]
        node_name = pod["spec"].get("nodeName")
        tolerations = TolerationList(
            items=[
                Toleration(
                    key=t.get("key"),
                    operator=t.get("operator", "Equal"),
                    value=t.get("value"),
                    effect=t.get("effect"),
                    toleration_seconds=t.get("tolerationSeconds"),
                )
                for t in pod["spec"].get("tolerations", [])
            ]
        )
        requests = Resource(0, 0)
        limits = Resource(0, 0)
        containers = pod["spec"].get("containers", [])
        for container in containers:
            requests += Resource(
                cpu=parse_cpu(container["resources"].get("requests", {}).get("cpu", 0)),
                memory=parse_storage(container["resources"].get("requests", {}).get("memory", 0)),
            )
            limits += Resource(
                cpu=parse_cpu(container["resources"].get("limits", {}).get("cpu", 0)),
                memory=parse_storage(container["resources"].get("limits", {}).get("memory", 0)),
            )

        # Get Pod metrics
        metrics = top_pods_metrics.get(f"{namespace}/{name}", Resource(0, 0))

        pod_list.add_pod(
            Pod(
                namespace=namespace,
                name=name,
                requests=requests,
                limits=limits,
                metrics=metrics,
                node=node_name,
                tolerations=tolerations,
                priority=pod["spec"].get("priority"),
                controller_type=pod["metadata"].get("ownerReferences", [{}])[0].get("kind"),
                node_selector=pod["spec"].get("nodeSelector"),
                affinity=pod["spec"].get("affinity"),
                anti_affinity=pod["spec"].get("antiAffinity"),
                status=pod["status"].get("phase"),
            )
        )

    return pod_list


def collect_node_list() -> NodeList:
    """Collect information for all nodes"""
    # collect all nodes metrics first, store it into a Dict, use the node name as key, Resource as value
    top_nodes_metrics = {}
    try:
        top_nodes_output = kubectl(["top", "nodes", "--no-headers"], exit_on_error=False)
        top_nodes_lines = top_nodes_output.splitlines()
        for line in top_nodes_lines:
            parts = line.split()
            name = parts[0]
            cpu = parse_cpu(parts[1])
            memory = parse_storage(parts[3])
            top_nodes_metrics[name] = Resource(cpu=cpu, memory=memory)
    except Exception:
        top_nodes_metrics = {}

    # collect all pods info
    pod_list = collect_pod_list()

    # collect all nodes info
    node_list = NodeList()
    output = kubectl(["get", "nodes", "-o", "json"])
    nodes = json.loads(output)["items"]

    for node in nodes:
        name = node["metadata"]["name"]
        architecture = node["status"]["nodeInfo"]["architecture"]
        operating_system = node["status"]["nodeInfo"]["operatingSystem"]
        allocatable = NodeResource(
            cpu=int(node["status"]["allocatable"].get("cpu", 0)) * 1000,  # Convert to millicores
            ephemeralStorage=int(parse_storage(node["status"]["allocatable"].get("ephemeral-storage", 0))),
            memory=int(parse_storage(node["status"]["allocatable"].get("memory", 0))),
            pods=parse_pod_count(node["status"]["allocatable"].get("pods", 0)),
        )
        capacity = NodeResource(
            cpu=int(node["status"]["capacity"].get("cpu", 0)) * 1000,  # Convert to millicores
            ephemeralStorage=int(parse_storage(node["status"]["capacity"].get("ephemeral-storage", 0))),
            memory=int(parse_storage(node["status"]["capacity"].get("memory", 0))),
            pods=parse_pod_count(node["status"]["capacity"].get("pods", 0)),
        )
        taints = TaintList(
            items=[
                Taint(
                    key=t["key"],
                    value=t.get("value"),
                    effect=t.get("effect"),
                )
                for t in node["spec"].get("taints", [])
            ]
        )

        image_list = ImageList()
        for image in node["status"].get("images", []):
            names = image.get("names", [])
            size_bytes = image.get("sizeBytes", 0)
            image_list.add_image(Image(names=names, sizeBytes=size_bytes))

        condition_list = ConditionList()
        for condition in node["status"].get("conditions", []):
            condition_list.add_condition(
                Condition(
                    type=condition["type"],
                    status=condition["status"],
                    reason=condition.get("reason"),
                    message=condition.get("message"),
                )
            )

        address_list = AddressList()
        for address in node["status"].get("addresses", []):
            address_list.add_address(
                Address(
                    type=address["type"],
                    address=address["address"],
                )
            )

        node_list.add_node(
            Node(
                name=name,
                architecture=architecture,
                operatingSystem=operating_system,
                allocatable=allocatable,
                capacity=capacity,
                taints=taints,
                images=image_list,
                pods=pod_list.get_pods_by_node(name),
                metrics=top_nodes_metrics.get(name, Resource(0, 0)),
                labels=node["metadata"].get("labels", {}),
                annotations=node["metadata"].get("annotations", {}),
                conditions=condition_list,
                addresses=address_list,
            )
        )

    return node_list


@dataclass
class SummaryFlags:
    wide: bool = False
    pods: bool = False
    images: bool = False
    taints: bool = False
    labels: bool = False
    annotations: bool = False
    capacity: bool = False
    allocatable: bool = False
    conditions: bool = False
    addresses: bool = False
    metrics: bool = False
    all: bool = False

    def is_empty(self) -> bool:
        """Check if all flags are empty"""
        return (
            not any(
                [
                    self.pods,
                    self.images,
                    self.taints,
                    self.labels,
                    self.annotations,
                    self.capacity,
                    self.allocatable,
                    self.conditions,
                    self.addresses,
                    self.metrics,
                ]
            )
            and not self.all
        )


def display_resources_node_details(
    node: Node,
    flags: SummaryFlags,
    namesuffix: str = "",
):
    if flags.is_empty():
        return

    logging.info(f"Node: {node.name}{namesuffix}")

    if (flags.all or flags.addresses) and node.addresses:
        logging.info("Addresses:")
        print_table(["Type", "Address"], node.addresses.items, lineprefix="  ")
        logging.info("")

    if (flags.all or flags.labels) and node.labels:
        logging.info("Labels:")
        for key, value in node.labels.items():
            logging.info(f"  {key}={value}")
        logging.info("")

    if (flags.all or flags.annotations) and node.annotations:
        logging.info("Annotations:")
        for key, value in node.annotations.items():
            logging.info(f"  {key}={value}")
        logging.info("")

    if (flags.all or flags.taints) and node.taints:
        logging.info("Taints:")
        for taint in node.taints:
            # format: key=value:effect
            logging.info(
                f"  {taint.key}={taint.value}:{taint.effect}" if taint.value else f"  {taint.key}:{taint.effect}"
            )
        logging.info("")

    if (flags.all or flags.capacity) and node.capacity:
        logging.info("Capacity:")
        logging.info(f"  CPU: {node.capacity.cpu}m")
        logging.info(f"  Memory: {math.ceil(node.capacity.memory)}Mi")
        logging.info(f"  Ephemeral Storage: {math.ceil(node.capacity.ephemeralStorage)}Mi")
        logging.info(f"  Pods: {node.capacity.pods}")
        logging.info("")

    if (flags.all or flags.allocatable) and node.allocatable:
        logging.info("Allocatable:")
        logging.info(f"  CPU: {node.allocatable.cpu}m")
        logging.info(f"  Memory: {math.ceil(node.allocatable.memory)}Mi")
        logging.info(f"  Ephemeral Storage: {math.ceil(node.allocatable.ephemeralStorage)}Mi")
        logging.info(f"  Pods: {node.allocatable.pods}")
        logging.info("")

    if (flags.all or flags.conditions) and node.conditions:
        logging.info("Conditions:")
        print_table(["Type", "Status", "Reason", "Message"], node.conditions.items, lineprefix="  ")
        logging.info("")

    if (flags.all or flags.metrics) and node.metrics:
        logging.info("Metrics:")
        logging.info(f"  {node.metrics}")
        logging.info("")

    if (flags.all or flags.pods) and node.pods:
        logging.info("Pods:")
        print_table(POD_HEADERS_WIDE if flags.wide else POD_HEADERS, node.pods.items, lineprefix="  ")
        logging.info("")

    if (flags.all or flags.images) and node.images:
        logging.info(f"Images: {math.ceil(node.images.size() / 1024 / 1024)}MB")
        print_table(IMAGE_HEADERS, node.images.items, lineprefix="  ")
        logging.info("")


def display_nodes(node_list: NodeList, wide: bool = False):
    """Display nodes in a table format"""
    if not node_list.items:
        logging.info("No nodes found.")
        return

    headers = NODE_HEADERS_WIDE if wide else NODE_HEADERS
    print_table(headers, node_list.items, lineprefix="  ")


@click.command()
@click.option(
    "--wide",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display more information.",
)
@click.option(
    "--pods",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display pods in every node.",
)
@click.option(
    "--images",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display images in every node.",
)
@click.option(
    "--taints",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display taints in every node.",
)
@click.option(
    "--labels",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display labels in every node.",
)
@click.option(
    "--annotations",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display annotations in every node.",
)
@click.option(
    "--capacity",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display capacity resources in every node.",
)
@click.option(
    "--allocatable",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display allocatable resources in every node.",
)
@click.option(
    "--conditions",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display conditions in every node.",
)
@click.option(
    "--addresses",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display addresses in every node.",
)
@click.option(
    "--metrics",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display metrics in every node.",
)
@click.option(
    "--all",
    is_flag=True,
    default=False,
    show_default=True,
    help="Display all information in every node.",
)
def summary(
    wide: bool,
    pods: bool,
    images: bool,
    taints: bool,
    labels: bool,
    annotations: bool,
    capacity: bool,
    allocatable: bool,
    conditions: bool,
    addresses: bool,
    metrics: bool,
    all: bool,
):
    node_list = collect_node_list()

    flags = SummaryFlags(
        wide=wide,
        pods=pods,
        images=images,
        taints=taints,
        labels=labels,
        annotations=annotations,
        capacity=capacity,
        allocatable=allocatable,
        conditions=conditions,
        addresses=addresses,
        metrics=metrics,
        all=all,
    )

    if not flags.is_empty():
        for node in node_list:
            display_resources_node_details(node, flags)

    logging.info("Summary of all nodes:")
    display_nodes(node_list, wide=wide)
