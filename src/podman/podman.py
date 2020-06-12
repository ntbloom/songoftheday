import subprocess
from typing import List


class Podman:
    """
    Manipulate podman from the command line to create and destroy disposable testing
    containers
    """

    @staticmethod
    def start_container(name: str, image: str, port: int) -> None:
        """
        Starts a container
        """
        args = [
            "podman",
            "run",
            "--rm",
            "--name",
            name,
            "-e",
            "POSTGRES_PASSWORD=docker",
            "-d",
            "-p",
            f"{port}:{port}",
            image,
        ]
        subprocess.run(args, capture_output=True).check_returncode()

    @staticmethod
    def force_rm_container(ident: str) -> None:
        """
        Kills the container
        """
        args = ["podman", "rm", "--force", ident]
        subprocess.run(args, capture_output=True).check_returncode()

    @staticmethod
    def get_containers() -> List[str]:
        args = ["podman", "ps", "--format", "{{.Names}}"]
        command = subprocess.run(args, capture_output=True)
        command.check_returncode()
        containers = command.stdout.decode().split("""\n""")
        return containers
