from __future__ import annotations

from typing import Any, Dict, Optional

from x17_container.dockers.base.structured import Structured


class Configuration(Structured):
    """
    Represents manual defined configuration to create Docker resources.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def describe(
        self,
        fields: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        data = self.to_dict()
        if fields:
            return {k: data[k] for k in fields if k in data}
        else:
            return data
