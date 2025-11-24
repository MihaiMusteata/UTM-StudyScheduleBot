from typing import List

from patterns.composite.component import Component


class DayComposite(Component):
    def __init__(self, name: str):
        super().__init__()
        self._children: List[Component] = []
        self.name = name

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        results = [child.operation() for child in self._children]
        return f"{self.name} -> " + "; ".join(results)

class SemesterComposite(Component):
    def __init__(self, name: str):
        super().__init__()
        self._children: List[Component] = []
        self.name = name

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def operation(self) -> str:
        results = [child.operation() for child in self._children]
        return f"{self.name}\n" + "\n".join(results)