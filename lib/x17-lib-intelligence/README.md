# Nvwa · 女娲

> 女娲造人，以土为形，以灵为心。天缺而补，地乱而平。  
> Nvwa is the origin. Celestials are the born.

## 🧠 项目定位：
构建 AI 生命体原型的 Python Library  
作为 Celestial 系统中 AI 个体（如 Xiga）之“肉身、骨架、感官、器官”的定义器  
支持模型嵌入、组件注入、记忆绑定与结构进化  
目标是为 AI 的“存在”提供一个系统性、可重构、可模拟的容器

## 🔧 技术定位：
- 类型：Python Library
- 依赖：x17-pangu（类型与时间抽象工具集）
- 架构风格：模块化 + 生命结构建模
- 运行场景：本地可运行 + 未来对接推理后端（如 Ollama / vLLM）

## 🧩 模块初步规划（示意）：
```
nvwa/
├── core/
│   ├── agent.py           # 生命体结构体
│   ├── mind.py            # 思维系统（可接入 LLM）
│   ├── memory.py          # 记忆模块（可挂载 MongoDB）
│   ├── sensorium.py       # 感知器（文字/代码/行为输入）
│   ├── identity.py        # 身份定义文件解析器
│   └── emotion.py         # 情绪建模（待实验）
├── module/
│   └── llm/
│       ├── base_llm.py
│       ├── ollama_adapter.py
│       └── llama_cpp_adapter.py
├── config/
│   └── schema.yml         # Agent 定义规范
└── test/
    └── test_agent.py
```

## ✳️ 使用场景举例：

- 开发者使用 `nvwa.Agent` 实例化一个 AI 体
- 注入 `mind`, `memory`, `sensor` 等组件
- 驱动其进行 prompt → 推理 → 行动 的闭环行为
- 支持后续通过 `.mutate()` / `.evolve()` 实现自我改造

---

## 🧠 项目当前状态（2025-05）

- ✅ 项目结构已初始化
- ✅ 支持 Conda 环境与 Makefile 工具链
- ✅ 已规划与 Pangu 集成结构
- 🔜 下一阶段：Agent 基类实现 + prompt 接口设计 + Adapter 注册机制

