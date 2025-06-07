import fnmatch
import re
from typing import Any, Callable, Dict, List, Literal, Optional, Union

from x17_base.particle.terminal import Process


class ProcessSet:
    ALLOWED_ATTRS = ["cmdline", "name", "username", "cwd", "exe"]
    ALLOWED_OPTIONS = ["pid", "name", "cmdline", "username", "cpu_percent", "memory_percent"]

    @classmethod
    def from_list(
        cls,
        processes: List[Process],
    ):
        return cls(processes=processes)

    def __init__(
        self,
        processes: Optional[List[Process]] = None,
    ):
        self.processes = processes or []

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "processes": [p.dict for p in self.processes],
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(processes={len(self.processes)})"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.processes)

    def __iter__(self):
        return iter(self.processes)

    def __getitem__(self, idx):
        return self.processes[idx]
    
    def __add__(self, other: "ProcessSet") -> "ProcessSet":
        if not isinstance(other, ProcessSet):
            raise TypeError("Can only add another ProcessSet")
        return ProcessSet(self.processes + other.processes)

    def add(
        self,
        process: Process,
    ) -> None:
        self.processes.append(process)

    def remove(
        self,
        process: Process,
    ) -> None:
        if process in self.processes:
            self.processes.remove(process)
        else:
            rm_pid = getattr(process, "pid", None)
            for p in self.processes:
                if p.pid == rm_pid:
                    self.processes.remove(p)
                    break

    def sort_by(
        self,
        key: str,
        reverse: bool = False,
    ) -> "ProcessSet":
        return ProcessSet(
            sorted(
                self.processes,
                key=lambda p: getattr(p, key, 0),
                reverse=reverse,
            ),
        )

    def match(
        self,
        keyword: str,
        attributes: List[str] = ["cmdline"],
        ignore_case: bool = True,
    ) -> "ProcessSet":
        result = []
        for process in self.processes:
            for attr in attributes:
                if attr not in self.ALLOWED_ATTRS:
                    continue

                value = str(getattr(process, attr, ""))
                if ignore_case:
                    if str(keyword).lower() in str(value).lower():
                        result.append(process)
                        break
                else:
                    if keyword in value:
                        result.append(process)
                        break
        return ProcessSet(result)

    def match_regex(
        self,
        keyword: str,
        attributes: List[str] = ["cmdline"],
        ignore_case: bool = True,
    ) -> "ProcessSet":
        result = []
        flags = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(keyword, flags)
        for process in self.processes:
            for attr in attributes:
                if attr not in self.ALLOWED_ATTRS:
                    continue
                value = getattr(process, attr, "")
                if pattern.search(str(value)):
                    result.append(process)
                    break
        return ProcessSet(result)

    def match_wildcard(
        self,
        keyword: str,
        attributes: List[str] = ["cmdline"],
        ignore_case: bool = True,
    ) -> "ProcessSet":
        result = []
        for process in self.processes:
            for attr in attributes:
                if attr not in self.ALLOWED_ATTRS:
                    continue

                value = getattr(process, attr, "")
                if ignore_case:
                    value = str(value).lower()
                    keyword = str(keyword).lower()
                if fnmatch.fnmatch(str(value), keyword):
                    result.append(process)
                    break
        return ProcessSet(result)
