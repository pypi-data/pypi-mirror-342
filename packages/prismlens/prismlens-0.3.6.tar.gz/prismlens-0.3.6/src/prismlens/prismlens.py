"""Control script for Prism and related services."""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from polykit.log import PolyLog

logger = PolyLog.get_logger(level="info")

# Define constants for container names and services
PROD_CONTAINERS = ["prismbot", "prism-db", "prism-redis"]
PROD_SERVICES = ["prism-db", "prism-redis"]
NGINX_CONTAINER = "nginx"


class PrismInstance(StrEnum):
    """Available Prism instances."""

    PROD = "prod"
    DEV = "dev"

    @property
    def path(self) -> Path:
        """Get the root path for this instance."""
        return Path(f"~/prism/{self}").expanduser()

    @property
    def container(self) -> str:
        """Get the container name for this instance."""
        if self == PrismInstance.DEV:
            return "prismbot-dev"
        return "prismbot"

    @property
    def description(self) -> str:
        """Get the container name for this instance."""
        description = str(self)
        if self == PrismInstance.PROD:
            description += " and associated services"
        return description


class PrismAction(StrEnum):
    """Valid actions for the Prism controller."""

    START = "start"
    RESTART = "restart"
    STOP = "stop"
    LOGS = "logs"
    SYNC = "sync"


@dataclass
class PrismConfig:
    """Configuration for Prism controller operations."""

    action: PrismAction
    instance: PrismInstance
    on_all: bool


def generate_config() -> PrismConfig:
    """Create a PrismConfig from command-line arguments."""
    # Define valid options
    actions = {name.lower() for name in PrismAction.__members__}
    modifiers = {"dev", "all"}

    # Find the action (default to logs if none specified)
    args = {arg.lower() for arg in sys.argv[1:]}
    action_str = next((arg for arg in args if arg in actions), "logs")
    try:
        action = PrismAction(action_str)
    except KeyError:
        action = PrismAction.LOGS  # Default to logs

    # Check for modifiers
    is_dev = "dev" in args
    is_all = "all" in args

    # Validate combinations
    if is_dev and is_all:
        logger.error("Cannot specify both 'dev' and 'all' at the same time")
        sys.exit(1)

    # Check for unknown arguments
    valid_args = actions | modifiers
    unknown_args = args - valid_args
    if unknown_args:
        logger.error("Unknown arguments: %s", ", ".join(unknown_args))
        sys.exit(1)

    instance = PrismInstance.DEV if is_dev else PrismInstance.PROD

    return PrismConfig(action=action, instance=instance, on_all=is_all)


# Generate config from arguments
config = generate_config()


def run(
    command: str | list[str], show_output: bool = False, cwd: str | None = None
) -> tuple[bool, str]:
    """Execute a shell command and optionally print the output."""
    try:
        with subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd
        ) as process:
            output, _ = process.communicate()
            decoded_output = output.decode("utf-8").strip()

            if show_output:
                print(decoded_output)

            return process.returncode == 0, decoded_output
    except subprocess.CalledProcessError as e:
        if show_output:
            print(e.output.decode("utf-8").strip())
        return False, e.output.decode("utf-8").strip()


def run_docker_compose_command(action: str, instance: PrismInstance) -> bool:
    """Run a Docker Compose command.

    Args:
        action: The Docker Compose action (up, down, etc.).
        instance: The Prism instance to operate on.
    """
    command = f"docker compose {action}"

    if action == "up":
        command += " -d"

    logger.debug("Running command in %s: %s", instance.path, command)
    try:
        result = subprocess.run(
            command, shell=True, cwd=str(instance.path), capture_output=True, text=True, check=False
        )

        if result.returncode != 0:
            logger.error(
                "Docker Compose command failed with exit code %d\nOutput: %s\nError: %s",
                result.returncode,
                result.stdout.strip(),
                result.stderr.strip(),
            )
            return False

        return True
    except Exception as e:
        logger.error("Docker Compose command failed: %s", str(e))
        return False


def build_image(instance: PrismInstance) -> bool:
    """Build the Docker image for Prism."""
    logger.info("Building Docker image...")

    commit_hash = _get_commit_hash()
    command = f"GIT_COMMIT_HASH={commit_hash} docker compose build"

    try:
        result = subprocess.call(command, shell=True, cwd=str(instance.path))
        if result == 0:
            logger.info("Docker image built successfully.")
            return True
        logger.error("Failed to build Docker image. Exit code: %d", result)
        return False
    except Exception as e:
        logger.error("An error occurred while building the Docker image: %s", str(e))
        return False


def _get_commit_hash() -> str:
    success, output = run("git rev-parse HEAD")
    return output.strip() if success else "unknown"


def verify_prod_before_nginx(max_attempts: int = 10) -> None:
    """Ensure that prod services are available before proceeding."""
    logger.info("Waiting for prod services to be ready...")

    for attempt in range(max_attempts):
        all_ready = True

        for container in PROD_CONTAINERS:  # Check if container is running and healthy
            cmd = f"docker inspect --format='{{{{.State.Status}}}}' {container} 2>/dev/null || echo 'not_found'"
            _, status = run(cmd)

            if status.strip() != "running":
                all_ready = False
                logger.debug(
                    "Container %s is not ready yet (status: %s)", container, status.strip()
                )
                break

        if all_ready:
            return

        logger.debug("Waiting for prod services (attempt %d/%d)...", attempt + 1, max_attempts)
        time.sleep(2)  # Short wait between checks

    logger.warning("Timed out waiting for prod services to be ready, continuing anyway.")


def verify_nginx() -> None:
    """Verify that nginx is running and configured correctly."""
    # Check if nginx container is running
    command = f'docker ps --filter "name={NGINX_CONTAINER}" --format "{{{{.Names}}}}"'
    _, output = run(command)
    running_containers = output.splitlines()

    if not any(NGINX_CONTAINER in container for container in running_containers):
        logger.error("%s container is not running.", NGINX_CONTAINER)
        sys.exit(1)

    # Check if nginx configuration is valid
    command = f"docker exec {NGINX_CONTAINER} nginx -t"
    success, output = run(command)

    if not (success and "syntax is ok" in output and "test is successful" in output):
        logger.error("nginx config check failed:\n%s", output)
        sys.exit(1)


def restart_nginx() -> None:
    """Restart the nginx container."""
    # Wait for prod services to be ready
    verify_prod_before_nginx()

    success, output = run(f"docker restart {NGINX_CONTAINER}")

    if not success:
        logger.warning("Failed to restart %s: %s", NGINX_CONTAINER, output)


def start_prism(instance: PrismInstance, stop_first: bool = True) -> None:
    """Start the Prism service."""
    if stop_first:
        stop_and_remove_containers(instance)

    logger.info("Starting %s...", instance.description)

    try:
        command = "docker compose up -d"
        logger.debug("Running command in %s: %s", instance.path, command)
        subprocess.call(command, shell=True, cwd=str(instance.path))
    except KeyboardInterrupt:
        logger.error("Start process interrupted.")


def stop_and_remove_containers(instance: PrismInstance) -> None:
    """Stop and remove Docker containers."""
    logger.info("Stopping and removing %s...", instance.container)

    # First try the normal docker compose down
    run_docker_compose_command("down", instance)

    # Verify containers are actually gone
    verify_container_removal(instance)


def verify_container_removal(instance: PrismInstance, max_attempts: int = 5) -> None:
    """Verify that containers are properly removed, with retries if needed."""
    containers_to_check = [instance.container]
    if instance == PrismInstance.PROD:
        containers_to_check.extend(PROD_SERVICES)

    for container in containers_to_check:
        ensure_container_removed(container, max_attempts)


def ensure_container_removed(container: str, max_attempts: int = 5) -> None:
    """Ensure a specific container is removed, with retries if needed."""
    for attempt in range(max_attempts):
        # Check if container exists
        check_cmd = f"docker ps -a --filter name=^/{container}$ --format '{{{{.Names}}}}'"
        success, output = run(check_cmd)

        if not success or not output.strip():
            return  # Container is gone, so we're done here

        # Last attempt - force remove
        if attempt == max_attempts - 1:
            logger.warning(
                "Container %s still exists after %d checks, forcing removal...",
                container,
                max_attempts,
            )
            run(f"docker rm -f {container}")

            # Final check after force removal
            success, output = run(check_cmd)
            if success and output.strip():
                logger.error("Failed to remove container %s even when forced.", container)
            return

        # Container exists but we have more attempts, so check its status
        logger.debug(
            "Container %s still exists, waiting for removal (attempt %d/%d)...",
            container,
            attempt + 1,
            max_attempts,
        )

        # Check container status
        status_cmd = f"docker inspect --format='{{{{.State.Status}}}}' {container} 2>/dev/null || echo 'removed'"
        _, status = run(status_cmd)
        status = status.strip()

        if status in {"removing", "exited"}:  # Container being removed
            logger.debug("Container %s is in state: %s", container, status)

        else:  # Container is not being removed, try to stop it
            logger.debug("Attempting to stop container %s.", container)
            run(f"docker stop {container}")

        # Wait before next attempt
        time.sleep(1)


def ensure_prod_running_before_dev() -> None:
    """Ensure the prod instance is running before proceeding."""
    prod = PrismInstance.PROD
    command = ["docker", "ps", "--filter", f"name={prod.container}", "--format", "{{.Status}}"]
    _, output = run(command)
    if "Up" not in output:
        logger.info("Prod instance not running, starting...")
        start_prism(prod)


def handle_start() -> None:
    """Handle 'start' action."""
    if config.on_all:
        verify_nginx()
        start_prism(PrismInstance.PROD)
        start_prism(PrismInstance.DEV)
        restart_nginx()
        follow_logs(PrismInstance.DEV)
    elif config.instance == PrismInstance.DEV:
        ensure_prod_running_before_dev()
        start_prism(PrismInstance.DEV)
        follow_logs(PrismInstance.DEV)
    else:
        verify_nginx()
        start_prism(PrismInstance.PROD)
        restart_nginx()
        follow_logs(PrismInstance.PROD)


def handle_restart() -> None:
    """Handle 'restart' action."""
    if config.on_all:
        if not build_image(PrismInstance.PROD) or not build_image(PrismInstance.DEV):
            logger.error("Image build failed. Exiting...")
            sys.exit(1)
    elif not build_image(config.instance):
        logger.error("Image build failed. Exiting...")
        sys.exit(1)

    # Check nginx if we're dealing with prod
    if config.instance == PrismInstance.PROD or config.on_all:
        verify_nginx()

    if config.on_all:
        handle_all()
    else:
        stop_and_remove_containers(config.instance)
        start_prism(config.instance, stop_first=False)
        if config.instance == PrismInstance.PROD:
            restart_nginx()
        follow_logs(config.instance)


def handle_stop() -> None:
    """Handle 'stop' action."""
    if config.on_all:  # Stop dev first, then prod
        stop_and_remove_containers(PrismInstance.DEV)
        stop_and_remove_containers(PrismInstance.PROD)
    elif config.instance == PrismInstance.DEV:
        stop_and_remove_containers(PrismInstance.DEV)
        follow_logs(PrismInstance.PROD)
    else:
        stop_and_remove_containers(PrismInstance.PROD)


def handle_all() -> None:
    """Handle 'restart' action for both instances, ensuring proper order."""
    logger.info("Restarting both instances.")

    # Stop both instances (dev first, then prod)
    stop_and_remove_containers(PrismInstance.DEV)
    stop_and_remove_containers(PrismInstance.PROD)

    # Start prod and wait for it to be ready
    start_prism(PrismInstance.PROD, stop_first=False)

    # Restart nginx once everything is ready
    restart_nginx()

    # Start dev
    start_prism(PrismInstance.DEV, stop_first=False)

    # Follow logs after both restarts are complete
    follow_logs(config.instance)


def follow_logs(instance: PrismInstance) -> None:
    """Follow the logs of the specified instance."""
    try:
        subprocess.call(["docker", "logs", "-f", instance.container])
    except KeyboardInterrupt:
        logger.info("Ending log stream.")
        sys.exit(0)


def main() -> None:
    """Perform the requested action."""
    # Check if both prod and dev paths exist
    if not PrismInstance.PROD.path.exists() or not PrismInstance.DEV.path.exists():
        logger.error("Required paths for prod and dev instances not found.")
        sys.exit(1)

    if config.action is PrismAction.START:
        handle_start()
    elif config.action is PrismAction.RESTART:
        handle_restart()
    elif config.action is PrismAction.STOP:
        handle_stop()
    else:
        follow_logs(config.instance)


if __name__ == "__main__":
    main()
