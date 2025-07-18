from __future__ import annotations

from typing import Any, Dict

from x17_base.particle.text import Text

from x17_container.dockers.base.structured import Structured


class Attributes(Structured):
    """
    Represents attributes that describe the real-time state of a Docker resource.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def describe(
        self,
    ) -> Dict[str, Any]:
        return self.to_dict()
