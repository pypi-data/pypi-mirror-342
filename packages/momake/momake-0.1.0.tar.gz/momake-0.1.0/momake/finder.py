from importlib import import_module
from inspect import getmodule
from logging import getLogger
from pkgutil import walk_packages

from momake.task import Task

logger = getLogger(__name__)


def is_defined_in(element, module):
    return getmodule(element).__name__ == module.__name__


class TaskFinder:
    modules = ["momaketasks"]

    def find(self):
        elements = []
        for parent in self.modules:
            info = "Searching for all objects in %s"
            logger.info(info, parent)
            for package in self._get_all_packages(parent):
                elements += list(self._find_in_package(package))
        logger.info("")
        return elements

    def _get_all_packages(self, parent: str):
        try:
            parentpkg = import_module(parent)
        except Exception:
            logger.error("Can not import parent module: %s", parent)
            return

        prefix = f"{parentpkg.__name__}."
        modpath = getattr(parentpkg, "__path__", None)
        if not modpath:
            yield parentpkg
            return

        for module in walk_packages(modpath, prefix):
            try:
                yield import_module(module.name)
            except Exception:
                logger.warning("Can not import module: %s", module.name)
                continue

    def _find_in_package(self, package):
        intro = False
        for elementname in dir(package):
            element = getattr(package, elementname)

            if self.is_collectable(element) and is_defined_in(element, package):
                if not intro:
                    logger.debug("Module found: %s", package.__name__)
                    intro = True
                logger.debug(f"\tTask found: %s", elementname)
                yield element

    def is_collectable(self, element: object):
        try:
            return issubclass(element, Task)
        except TypeError:
            return False
