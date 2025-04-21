#!/usr/bin/env python3

import logging
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import click

from k8ops.types import (
    Node,
    NodeList,
    Pod,
    Resource,
    node_selector_matches_node_list,
    pod_tolerates_node_taints,
)
from k8ops.utils.table import tabulate

from .summary import SummaryFlags, collect_node_list, display_resources_node_details


@dataclass
class AnalysisResult:
    """Represents the result of an analysis"""

    message: str
    severity: str = "low"  # none, low, medium, high

    def __str__(self) -> str:
        return f"{self.severity}: {self.message}"


@dataclass
class Reporter:
    """Represents a reporter for analysis results"""

    results: List[AnalysisResult] = field(default_factory=list)

    def add_result(self, result: AnalysisResult):
        self.results.append(result)

    def print_report(self):
        """Print the analysis report"""
        if not self.results:
            logging.info("No issues found")
            return

        logging.info("Analysis Report:")
        logging.info(
            tabulate(
                ["Severity", "Message"],
                [[result.severity, result.message] for result in self.results],
                lineprefix="  ",
                showindex=False,
            )
        )

        logging.info("")
        logging.info("Summary:")
        severity_count = {"none": 0, "low": 0, "medium": 0, "high": 0}
        for result in self.results:
            severity_count[result.severity] += 1

        logging.info(
            tabulate(
                ["Severity", "Count"],
                [[severity, count] for severity, count in severity_count.items()],
                lineprefix="  ",
                showindex=False,
            )
        )

        logging.info("")
        logging.info("Conclusions:")
        conclusion = ""
        if severity_count["high"] > 0:
            conclusion = "🚫 High severity issues found. Please review the report carefully."
        elif severity_count["medium"] > 0:
            conclusion = "❗️ Medium severity issues found. Please review the report."
        elif severity_count["low"] > 0:
            conclusion = "⚠️ Low severity issues found. Please review the report."
        else:
            conclusion = "✅ No issues found. All nodes are safe to drain."
        logging.info("  " + conclusion)


def group_pods_by_namespace(pod_list: List[Pod]) -> str:
    """Group pods by their namespace and return a formatted string"""
    namespace_dict: Dict[str, List[str]] = {}
    for pod in pod_list:
        namespace = pod.namespace
        if namespace not in namespace_dict:
            namespace_dict[namespace] = []
        namespace_dict[namespace].append(pod.name)

    grouped_info: List[str] = []
    for namespace, pods in namespace_dict.items():
        grouped_info.append(f"{namespace} ({', '.join(pods)})")

    return ", ".join(grouped_info)


def retrieve_node_pressure(node: Node) -> Tuple[bool, str]:
    """Retrieve the pressure status of a node"""
    # find pressure conditions
    pressure_conditions = [
        condition for condition in node.conditions.items if "Pressure" in condition.type and condition.status == "True"
    ]
    if pressure_conditions:
        pressure_types = [condition.type for condition in pressure_conditions]
        return True, ", ".join(pressure_types)
    return False, ""


def analyze(remaining_node_list: NodeList, drain_node_list: NodeList, factor: float = 1.5):
    """Analyze the node list with a scale factor"""
    reporter = Reporter()
    # Check any remaining nodes have any pressure
    for node in remaining_node_list:
        has_pressure, pressure_types = retrieve_node_pressure(node)
        if has_pressure:
            reporter.add_result(
                AnalysisResult(
                    f"Node {node.name} has pressure conditions: {pressure_types}. Please check the node.",
                    "high",
                )
            )

    # Check for pods controlled by daemonsets
    daemonset_pods = [pod for pod in drain_node_list.podList.items if pod.controller_type == "DaemonSet"]
    if daemonset_pods:
        reporter.add_result(
            AnalysisResult(
                f"Pods controlled by DaemonSets will not be affected by node drain, they are {group_pods_by_namespace(daemonset_pods)}.",
                "none",
            )
        )

    # Check for running jobs/cronjobs
    job_pods = [
        pod
        for pod in drain_node_list.podList.items
        if pod.controller_type in ["Job", "CronJob"] and pod.status == "Running"
    ]
    if job_pods:
        reporter.add_result(
            AnalysisResult(
                f"Pods controlled by Jobs/CronJobs are running: {group_pods_by_namespace(job_pods)}. Please wait for them to finish.",
                "medium",
            )
        )

    # Check for pods with no controller
    no_controller_pods = [pod for pod in drain_node_list.podList.items if pod.controller_type is None]
    if no_controller_pods:
        reporter.add_result(
            AnalysisResult(
                f"Pods with no controller: {group_pods_by_namespace(no_controller_pods)}. Please check them.",
                "medium",
            )
        )

    # Check for pods with node selector
    node_selector_pods = [
        pod for pod in drain_node_list.podList.items if pod.node_selector and pod.controller_type != "DaemonSet"
    ]
    if node_selector_pods:
        for pod in node_selector_pods:
            if not node_selector_matches_node_list(pod.node_selector, remaining_node_list):
                reporter.add_result(
                    AnalysisResult(
                        f"Pod {pod.namespace}/{pod.name} has a node selector that does not match remaining nodes.",
                        "high",
                    )
                )

    # Check for pods with affinity/anti-affinity
    affinity_pods = [
        pod
        for pod in drain_node_list.podList.items
        if (pod.affinity or pod.anti_affinity) and pod.controller_type != "DaemonSet"
    ]
    if affinity_pods:
        for pod in affinity_pods:
            reporter.add_result(
                AnalysisResult(
                    f"Pods with affinity/anti-affinity: {pod.namespace}/{pod.name}. Please check if they can be scheduled on remaining nodes.",
                    "medium",
                )
            )

    # Check for taints and tolerations
    pods_to_reschedule = [pod for pod in drain_node_list.podList.items if pod.controller_type != "DaemonSet"]
    for pod in pods_to_reschedule:
        schedulable_nodes = []
        for node in remaining_node_list.items:
            if node.taints and len(node.taints) > 0:
                if not pod_tolerates_node_taints(pod.tolerations.items, node.taints.items):
                    continue
            schedulable_nodes.append(node.name)

        if not schedulable_nodes:
            reporter.add_result(
                AnalysisResult(
                    f"Pod {pod.namespace}/{pod.name} cannot be scheduled on any remaining nodes due to taints/tolerations.",
                    "high",
                )
            )

    # Check for resource constraints
    total_requests = Resource(0, 0)
    for pod in pods_to_reschedule:
        total_requests.cpu += int(pod.requests.cpu if pod.requests.cpu else pod.metrics.cpu * factor)
        total_requests.memory += int(pod.requests.memory if pod.requests.memory else pod.metrics.memory * factor)

    total_allocatable = Resource(0, 0)
    for node in remaining_node_list.items:
        total_allocatable.cpu += node.allocatable.cpu
        total_allocatable.memory += node.allocatable.memory

    if total_requests.cpu > total_allocatable.cpu:
        reporter.add_result(
            AnalysisResult(
                f"Insufficient CPU resources in remaining nodes. Required: {total_requests.cpu}m, Available: {total_allocatable.cpu}m",
                "high",
            )
        )

    if total_requests.memory > total_allocatable.memory:
        reporter.add_result(
            AnalysisResult(
                f"Insufficient memory resources in remaining nodes. Required: {math.ceil(total_requests.memory)}Mi, Available: {math.ceil(total_allocatable.memory)}Mi",
                "high",
            )
        )

    # Check for architecture and OS compatibility
    drain_architectures = {node.architecture for node in drain_node_list.items}
    drain_os = {node.operatingSystem for node in drain_node_list.items}

    remaining_architectures = {node.architecture for node in remaining_node_list.items}
    remaining_os = {node.operatingSystem for node in remaining_node_list.items}

    # Check for missing architectures using set operations
    missing_architectures = drain_architectures - remaining_architectures
    if missing_architectures:
        reporter.add_result(
            AnalysisResult(
                f"Architecture(s) {', '.join(missing_architectures)} from drain nodes not available in remaining nodes. Some pods may not be schedulable.",
                "high",
            )
        )

    # Check for missing operating systems using set operations
    missing_os = drain_os - remaining_os
    if missing_os:
        reporter.add_result(
            AnalysisResult(
                f"Operating system(s) {', '.join(missing_os)} from drain nodes not available in remaining nodes. Some pods may not be schedulable.",
                "high",
            )
        )

    # Check for allocatable pods
    total_allocatable_pods = sum(node.allocatable.pods for node in remaining_node_list.items) - sum(
        len(node.pods.items) for node in remaining_node_list.items
    )
    if total_allocatable_pods < len(pods_to_reschedule):
        reporter.add_result(
            AnalysisResult(
                f"Insufficient allocatable pods in remaining nodes. Required: {len(pods_to_reschedule)}, Available: {total_allocatable_pods}",
                "high",
            )
        )

    # Check pod distribution after drain
    # Calculate the average pod count per node before and after drain
    current_pod_count = sum(len(node.pods.items) for node in remaining_node_list.items) + sum(
        len(node.pods.items) for node in drain_node_list.items
    )
    current_node_count = len(remaining_node_list.items) + len(drain_node_list.items)

    future_pod_count = sum(len(node.pods.items) for node in remaining_node_list.items) + len(pods_to_reschedule)
    future_node_count = len(remaining_node_list.items)

    if current_node_count > 0 and future_node_count > 0:
        current_avg = current_pod_count / current_node_count
        future_avg = future_pod_count / future_node_count

        if future_avg > current_avg * 1.5:  # 50% increase in pod density
            reporter.add_result(
                AnalysisResult(
                    f"Pod density will increase significantly from {current_avg:.1f} to {future_avg:.1f} pods per node.",
                    "medium",
                )
            )

    # After a comprehensive analysis, summarize into overall recommendations
    reporter.print_report()


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
@click.option(
    "--factor",
    type=float,
    default=1.5,
    show_default=True,
    help="Factor to scale the requested resources based on metrics.",
)
@click.argument(
    "nodes",
    nargs=-1,
    type=click.STRING,
    required=True,
)
@click.pass_context
def drain(
    ctx: click.Context,
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
    factor: float,
    nodes: List[str],
):
    """Drain a node in the cluster."""
    if not nodes:
        logging.warning("No nodes specified. Please provide node names to drain.")
        ctx.exit(1)

    remaining_node_list = collect_node_list()
    drain_node_list = NodeList()
    for node in nodes:
        node = remaining_node_list.remove_node(node)
        if node is None:
            logging.error(f"Node {node} not found")
            continue
        drain_node_list.add_node(node)

    if len(drain_node_list) == 0:
        logging.info("❓ No nodes to drain")
        ctx.exit(0)

    if len(remaining_node_list) == 0:
        logging.info("⚠️ No remaining nodes")
        # ctx.exit(0)

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
    # display resources summary
    if not flags.is_empty():
        # display resources summary first
        for node in remaining_node_list:
            display_resources_node_details(node, flags)

        for node in drain_node_list:
            display_resources_node_details(node, flags, namesuffix="*")

    # analyze the node list
    analyze(remaining_node_list, drain_node_list, factor)
