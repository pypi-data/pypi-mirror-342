#!/usr/bin/env python3

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from k8ops.utils.table import table_view


@table_view
@dataclass
class Condition:
    """Represents Kubernetes node condition"""

    type: str = field(metadata={"column": "Type"})
    status: str = field(metadata={"column": "Status"})
    reason: Optional[str] = field(default=None, metadata={"column": "Reason"})
    message: Optional[str] = field(default=None, metadata={"column": "Message"})


@dataclass
class ConditionList:
    """Represents a list of Kubernetes node conditions"""

    items: List[Condition] = field(default_factory=list)

    def add_condition(self, condition: Condition):
        self.items.append(condition)

    def remove_condition(self, condition: Condition):
        self.items.remove(condition)

    def __str__(self) -> str:
        return ", ".join(str(condition) for condition in self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


@dataclass
class Taint:
    """Represents Kubernetes node taint"""

    key: str
    value: Optional[str] = None
    effect: str = "NoSchedule"

    def __str__(self) -> str:
        return f"{self.key}={self.value}:{self.effect}" if self.value else f"{self.key}:{self.effect}"


@dataclass
class TaintList:
    """Represents a list of Kubernetes node taints"""

    items: List[Taint] = field(default_factory=list)

    def add_taint(self, taint: Taint):
        self.items.append(taint)

    def remove_taint(self, taint: Taint):
        self.items.remove(taint)

    def __str__(self) -> str:
        return ", ".join(str(taint) for taint in self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


@dataclass
class Toleration:
    """Represents Pod toleration"""

    key: str
    operator: str = "Equal"  # 'Exists' or 'Equal'
    value: Optional[str] = None
    effect: Optional[str] = None
    toleration_seconds: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.key}={self.value}:{self.effect}" if self.value else f"{self.key}:{self.effect}"


@dataclass
class TolerationList:
    """Represents a list of Pod tolerations"""

    items: List[Toleration] = field(default_factory=list)

    def add_toleration(self, toleration: Toleration):
        self.items.append(toleration)

    def remove_toleration(self, toleration: Toleration):
        self.items.remove(toleration)

    def __str__(self) -> str:
        return ", ".join(str(toleration) for toleration in self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


def toleration_matches_taint(toleration: Toleration, taint: Taint) -> bool:
    """Check if toleration matches taint"""
    # Special case 1: If toleration.key is empty and operator is Exists, it matches all keys
    if toleration.key == "" and toleration.operator == "Exists":
        # But effect still needs to match
        return toleration.effect == taint.effect or toleration.effect == ""

    # General case: key must match
    if toleration.key != taint.key:
        return False

    # Special case 2: If effect is empty, it matches all effects with the same key
    if toleration.effect == "":
        # Only check operator and value
        pass
    # General case: effect needs to match
    elif toleration.effect != taint.effect:
        return False

    # Check operator and value
    if toleration.operator == "Exists":
        # Exists operator does not care about value
        return True
    elif toleration.operator == "Equal":
        # Equal operator requires value to match
        return toleration.value == taint.value

    # Default case does not match
    return False


def pod_tolerates_node_taints(tolerations: List[Toleration], taints: List[Taint]) -> bool:
    """Check if Pod tolerations allow it to be scheduled to a node with taints"""
    if not taints:
        return True

    for taint in taints:
        if not any(toleration_matches_taint(toleration, taint) for toleration in tolerations):
            return False

    return True


@dataclass
class Resource:
    cpu: int
    memory: int

    def __add__(self, other: "Resource") -> "Resource":
        return Resource(self.cpu + other.cpu, self.memory + other.memory)

    def __sub__(self, other: "Resource") -> "Resource":
        return Resource(self.cpu - other.cpu, self.memory - other.memory)

    def __str__(self) -> str:
        return f"{self.cpu}m/{math.ceil(self.memory)}MiB"


@table_view
@dataclass
class Pod:
    namespace: str = field(metadata={"column": "Namespace"})
    name: str = field(metadata={"column": "Name"})
    requests: Resource = field(default_factory=lambda: Resource(0, 0), metadata={"column": "Requests"})
    limits: Resource = field(default_factory=lambda: Resource(0, 0), metadata={"column": "Limits"})
    metrics: Resource = field(default_factory=lambda: Resource(0, 0), metadata={"column": "Metrics"})
    priority: Optional[int] = field(default=None, metadata={"column": "Priority"})
    node: Optional[str] = field(default=None, metadata={"column": "Node"})
    tolerations: TolerationList = field(default_factory=TolerationList, metadata={"column": "Tolerations"})
    controller_type: Optional[str] = field(default=None, metadata={"column": "ControlledBy"})
    node_selector: Dict[str, str] = field(default_factory=dict, metadata={"column": "NodeSelector"})
    status: Optional[str] = field(default=None, metadata={"column": "Status"})
    affinity: Optional[str] = None
    anti_affinity: Optional[str] = None


@dataclass
class PodList:
    items: List[Pod] = field(default_factory=list)
    requests: Resource = field(default_factory=lambda: Resource(0, 0))
    limits: Resource = field(default_factory=lambda: Resource(0, 0))
    metrics: Resource = field(default_factory=lambda: Resource(0, 0))

    def add_pod(self, pod: Pod):
        self.items.append(pod)
        self.requests += pod.requests
        self.limits += pod.limits
        self.metrics += pod.metrics

    def remove_pod(self, pod: Pod):
        self.items.remove(pod)
        self.requests -= pod.requests
        self.limits -= pod.limits
        self.metrics -= pod.metrics

    def get_pods_by_namespace(self, namespace: str) -> "PodList":
        pods_in_namespace = PodList()
        for pod in self.items:
            if pod.namespace == namespace:
                pods_in_namespace.add_pod(pod)
        return pods_in_namespace

    def get_pods_by_node(self, node: str) -> "PodList":
        pods_on_node = PodList()
        for pod in self.items:
            if pod.node == node:
                pods_on_node.add_pod(pod)
        return pods_on_node

    def __len__(self) -> int:
        return len(self.items)

    def __add__(self, other: "PodList") -> "PodList":
        combined = PodList()
        combined.items = self.items + other.items
        combined.requests = self.requests + other.requests
        combined.limits = self.limits + other.limits
        combined.metrics = self.metrics + other.metrics
        return combined

    def __sub__(self, other: "PodList") -> "PodList":
        combined = PodList()
        combined.items = [pod for pod in self.items if pod not in other.items]
        combined.requests = self.requests - other.requests
        combined.limits = self.limits - other.limits
        combined.metrics = self.metrics - other.metrics
        return combined

    def __iter__(self):
        return iter(self.items)


def image_name_format(names: List[str], _: Any) -> str:
    """Format image names for display"""
    if not names:
        return "-"

    if len(names) == 1:
        return names[0]

    # Prefer the name like "name:tag" or "name" if available
    preferred_name = next((name for name in names if "@" not in name), None)
    return (preferred_name if preferred_name else names[0]) + f" (+{len(names) - 1} more)"


@table_view
@dataclass
class Image:
    names: List[str] = field(default_factory=list, metadata={"column": "Name", "formatter": image_name_format})
    sizeBytes: int = field(default=0, metadata={"column": "Size", "formatter": lambda x, _: f"{x / (1024 * 1024):.2f}"})


@dataclass
class ImageList:
    items: List[Image] = field(default_factory=list)

    def add_image(self, image: Image):
        self.items.append(image)

    def remove_image(self, image: Image):
        self.items.remove(image)

    def size(self) -> int:
        return sum(image.sizeBytes for image in self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return "\n".join(str(image) for image in self.items)

    def __iter__(self):
        return iter(self.items)


@dataclass
class NodeResource:
    cpu: int
    ephemeralStorage: int
    memory: int
    pods: int

    def __add__(self, other: "NodeResource") -> "NodeResource":
        return NodeResource(
            self.cpu + other.cpu,
            self.ephemeralStorage + other.ephemeralStorage,
            self.memory + other.memory,
            self.pods + other.pods,
        )

    def __sub__(self, other: "NodeResource") -> "NodeResource":
        return NodeResource(
            self.cpu - other.cpu,
            self.ephemeralStorage - other.ephemeralStorage,
            self.memory - other.memory,
            self.pods - other.pods,
        )

    def __str__(self) -> str:
        # format: cpu/memory/ephemeralStorage/pods
        return f"{self.cpu}m/{math.ceil(self.memory / (1024 * 1024))}MiB/{math.ceil(self.ephemeralStorage/1024)}GiB/{self.pods}Pods"


@table_view
@dataclass
class Address:
    address: str = field(metadata={"column": "Address"})
    type: Optional[str] = field(default=None, metadata={"column": "Type"})

    def __str__(self) -> str:
        return f"{self.type}={self.address}" if self.type else self.address


@dataclass
class AddressList:
    items: List[Address] = field(default_factory=list)

    def add_address(self, address: Address):
        self.items.append(address)

    def remove_address(self, address: Address):
        self.items.remove(address)

    def __str__(self) -> str:
        return ", ".join(str(address) for address in self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


@table_view
@dataclass
class Node:
    name: str = field(metadata={"column": "Node"})
    labels: Dict[str, str] = field(default_factory=dict, metadata={"column": "Labels"})
    annotations: Dict[str, str] = field(default_factory=dict, metadata={"column": "Annotations"})
    architecture: str = field(default="", metadata={"column": "Architecture"})
    operatingSystem: str = field(default="", metadata={"column": "OperatingSystem"})
    allocatable: NodeResource = field(
        default_factory=lambda: NodeResource(0, 0, 0, 0), metadata={"column": "Allocatable"}
    )
    capacity: NodeResource = field(default_factory=lambda: NodeResource(0, 0, 0, 0), metadata={"column": "Capacity"})
    taints: TaintList = field(default_factory=TaintList, metadata={"column": "Taints"})
    images: ImageList = field(default_factory=ImageList, metadata={"column": "Images"})
    pods: PodList = field(default_factory=PodList, metadata={"column": "Pods"})
    metrics: Resource = field(default_factory=lambda: Resource(0, 0), metadata={"column": "Metrics"})
    conditions: ConditionList = field(default_factory=ConditionList, metadata={"column": "Conditions"})
    addresses: AddressList = field(default_factory=AddressList, metadata={"column": "Addresses"})


@dataclass
class NodeList:
    items: List[Node] = field(default_factory=list)
    allocatable: NodeResource = field(default_factory=lambda: NodeResource(0, 0, 0, 0))
    capacity: NodeResource = field(default_factory=lambda: NodeResource(0, 0, 0, 0))
    podList: PodList = field(default_factory=PodList)

    def add_node(self, node: Node):
        self.items.append(node)
        self.allocatable += node.allocatable
        self.capacity += node.capacity
        self.podList += node.pods

    def remove_node(self, name: str) -> Optional[Node]:
        node = next((n for n in self.items if n.name == name), None)
        if node:
            self.items.remove(node)
            self.allocatable -= node.allocatable
            self.capacity -= node.capacity
            self.podList -= node.pods
            return node
        return None

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)


def node_selector_matches(node_selector: Dict[str, str], node: Node) -> bool:
    """Check if node selector matches node labels"""
    for key, value in node_selector.items():
        if key not in node.labels or node.labels[key] != value:
            return False
    return True


def node_selector_matches_node_list(node_selector: Dict[str, str], node_list: NodeList) -> bool:
    """Check if node selector matches any node in the node list"""
    for node in node_list.items:
        if node_selector_matches(node_selector, node):
            return True
    return False
