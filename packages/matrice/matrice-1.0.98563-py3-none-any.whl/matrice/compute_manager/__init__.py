from matrice.utils import dependencies_check
dependencies_check(["docker", "psutil"])

from matrice.compute_manager.instance_manager import InstanceManager  # noqa: E402
__all__ = ["InstanceManager"]
