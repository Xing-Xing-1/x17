# Shuli Base 设计文档 (Element Layer)

## 1. Base概览

Shuli的 Base 层（base/）是全系统最根本的概念层，负责抽象、综合、统一表示类型、函数、参数、导入、注释、以及代码块等主要组成元素，实现统一分析、统一分组，为后续各种进阶操作托底。

---

## 2. 核心理念

- **一切元素均是Node**
- **Node分为Composite (组合型)和Leaf (变量型)**
- **Node是整个系统最小公维数**
- **通过children实现自循环接结，形成树状结构**


| 概念 | 说明 |
|----|----|
| 元素 (Element) | Class, Function, Argument, Import, Comment, CodeBlock |
| Node | 统一抽象的基本组成单元 |
| Composite Node | 可以拥有children的Node (Class, Function, Module) |
| Leaf Node | 不能拥有children的Node (Import, Comment, Argument, CodeBlock) |


---

## 3. Node结构设计

### NodeType

```python
class NodeType(Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    IMPORT = "import"
    COMMENT = "comment"
    CODEBLOCK = "codeblock"
    ARGUMENT = "argument"
```

### Node基础类

```python
class Node:
    def __init__(
        self,
        type: NodeType,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        children: Optional[List["Node"]] = None,
    ):
        self.type = type
        self.name = name
        self.attributes = attributes or {}
        self.children = []

        if type in {NodeType.CLASS, NodeType.FUNCTION, NodeType.MODULE}:
            self.children = children or []
        elif children:
            raise ValueError(f"Node of type {type.value} cannot have children.")

    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "name": self.name,
            "attributes": self.attributes,
            "children": [child.to_dict() for child in self.children],
        }

    def __repr__(self) -> str:
        return f"Node(type={self.type.value}, name={self.name})"
```


---

## 4. 设计原则总结

| 模块 | 原则 |
|----|----|
| 统一性 | 所有元素一开始就是Node，不需要后期作为特例处理 |
| 循环结构 | Node的children可以继续是Node，支持无限子类，子函数等 |
| 抽象缩小 | 将规范性元素抽象成简单结构，方便存储、导出、分析 |
| 清晰分层 | Composite（Class/Function/Module） vs Leaf（Import/Argument/Comment/CodeBlock）解耦分明 |
| 交互符合科学 | 符合组合设计模式（Composite Pattern），能表达复杂代码结构 |

---

## 5. 扩展性 
- Node作为Shuli的最基础单元
- 未来可自然扩展到其他语言（Java, C++, Go）
- 支持各类导出格式（JSON, Markdown, HTML）
- 为智能分析、文献系统、矩阵统计等功能托底







```

[Argument] 
    │
    ▼
[Function] ── [Comment]
    │
    ▼
[Class] ── [Comment]
    │
    ▼
[Import] ── [Comment]
    │
    ▼
[CodeBlock]

（所有粒子组合）
    │
    ▼
[Node] （模块/文件/系统）

```

Composite Pattern（组合模式）
	•	Class Node ➔ 可以children: [Function Node, Import Node, Comment Node, Inner Class Node]
	•	Function Node ➔ 可以children: [Import Node, Comment Node, Inner Class Node]