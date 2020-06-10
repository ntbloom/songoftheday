import subprocess
from src.podman.podman import Podman
from src import TEST_CONTAINER, POSTGRES, POSTGRES_PORT
import pytest


@pytest.mark.podman
class TestPodmanWrapper:
    def test_postgres_image_exists(self):
        """latest postgresql image is downloaded"""
        args = ["podman", "images", "--format", "{{.Repository}}"]
        command = subprocess.run(args, capture_output=True)
        command.check_returncode()
        actual = command.stdout.decode().split("""\n""")
        assert POSTGRES in actual

    def test_start_container_postgres(self):
        """podman_wrapper can run a new container"""
        if TEST_CONTAINER in Podman.get_containers():
            args = ["podman", "rm", "--force", TEST_CONTAINER]
            kill = subprocess.run(args, capture_output=True)
            kill.check_returncode()
        assert TEST_CONTAINER not in Podman.get_containers()

        Podman.start_container(TEST_CONTAINER, POSTGRES, POSTGRES_PORT)
        assert TEST_CONTAINER in Podman.get_containers()

    def test_kill_container_postgres(self):
        """podman can kill a container"""
        if TEST_CONTAINER not in Podman.get_containers():
            Podman.start_container(TEST_CONTAINER, POSTGRES, POSTGRES_PORT)
        Podman.stop_container(TEST_CONTAINER)

        assert TEST_CONTAINER not in Podman.get_containers()

    def test_get_containers(self):
        """podman returns a list of all running containers"""
        name = "disposable"
        Podman.start_container(name, POSTGRES, POSTGRES_PORT)

        actual = Podman.get_containers()
        try:
            assert name in actual
        finally:
            Podman.stop_container(name)
