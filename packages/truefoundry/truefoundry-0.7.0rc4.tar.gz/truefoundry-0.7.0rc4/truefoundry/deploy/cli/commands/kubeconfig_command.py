from typing import Any, Dict, Optional
from urllib.parse import urljoin

import rich_click as click
from rich.console import Console

from truefoundry.cli.const import COMMAND_CLS
from truefoundry.cli.util import handle_exception_wrapper
from truefoundry.common.session import Session
from truefoundry.deploy.cli.commands.utils import (
    CONTEXT_NAME_FORMAT,
    add_update_cluster_context,
    get_cluster_server_url,
    get_kubeconfig_content,
    get_kubeconfig_path,
    save_kubeconfig,
)

console = Console()


def construct_k8s_proxy_server(host: str, cluster: str) -> str:
    """Construct the Kubernetes proxy server URL."""
    return urljoin(host, f"api/svc/v1/k8s/proxy/{cluster}")


@click.command(
    name="kubeconfig",
    cls=COMMAND_CLS,
    help="Update kubeconfig with TrueFoundry cluster context",
)
@click.option(
    "-c",
    "--cluster",
    type=str,
    required=True,
    help="The cluster id from TrueFoundry",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    show_default=True,
    help="Overwrite if cluster entry already exists",
)
@handle_exception_wrapper
def kubeconfig_command(cluster: str, overwrite: bool = False) -> None:
    """
    Execute kubectl commands with authentication through the TrueFoundry CLI.
    """
    session = Session.new()

    path = get_kubeconfig_path()
    kubeconfig: Dict[str, Any] = get_kubeconfig_content(path=path)
    server_url: Optional[str] = get_cluster_server_url(kubeconfig, cluster)
    if server_url is not None and not overwrite:
        should_update = click.confirm(
            text=f"Context `{CONTEXT_NAME_FORMAT.format(cluster=cluster)}` for cluster `{cluster}` already exists in kubeconfig.\nDo you want to update the context?",
            default=False,
            err=True,
        )
        if not should_update:
            console.print(
                "Existing context found. Use --overwrite to force update the context."
            )
            return

    k8s_proxy_server: str = construct_k8s_proxy_server(session.tfy_host, cluster)

    context_name: str = add_update_cluster_context(
        kubeconfig,
        cluster,
        k8s_proxy_server,
        exec_command=[
            "tfy",
            "--json",
            "get",
            "k8s-exec-credential",
            "--cluster",
            cluster,
        ],
    )

    save_kubeconfig(kubeconfig, path=path)
    console.print(
        f"Updated kubeconfig at {str(path)!r} with context {context_name!r} for cluster {cluster!r}\n"
        f"Run `kubectl config use-context {context_name}` to use this context\n"
    )
