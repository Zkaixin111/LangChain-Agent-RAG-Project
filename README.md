# 智扫通 · 扫地机器人智能客服

基于 **LangChain + LangGraph** 构建的智能客服机器人：以 RAG 检索回答产品使用问题，通过 ReAct 工具调用获取用户上下文，并借助中间件实现「使用报告生成」的动态提示词切换。

## 功能特性

- **RAG 检索问答**：扫地机器人说明书语料（选购指南 / 故障排除 / 维护保养等）经切分后入库 Chroma，检索结果与提问一起交给通义千问总结回答
- **ReAct 智能体**：基于 LangGraph 的 Agent 循环，支持流式输出；内置 7 个工具（RAG 检索、天气查询、用户身份 / 所在城市 / 当前月份、外部数据拉取、报告上下文填充）
- **中间件机制**：工具调用监控（`wrap_tool_call`）、模型调用前后日志（`before_model`）、动态提示词（`dynamic_prompt`）——当工具填充报告上下文后，自动将系统提示词切换为"报告生成"模式
- **模型工厂**：抽象工厂统一创建 Chat 模型（ChatTongyi / qwen）与 Embedding 模型（text-embedding-v4），便于更换模型供应商
- **配置分层**：`config/` 下 agent / rag / chroma / prompt 四份 YAML，`utils/config_handler` 统一加载；密钥一律从环境变量 `DASHSCOPE_API_KEY` 注入
- **Streamlit 对话界面**：聊天窗口 + 打字机式流式输出

## 项目结构

```
├── agent/
│   ├── react_agent.py        # ReAct 智能体主体（LangGraph 流式）
│   └── tools/
│       ├── agent_tools.py    # 7 个 @tool 工具集
│       └── middleware.py     # 工具监控 / 模型日志 / 动态提示词
├── config/                   # agent / rag / chroma / prompt 四份 YAML
├── data/                     # 产品语料（txt / pdf）
├── model/factory.py          # Chat / Embedding 模型工厂
├── prompts/                  # 系统提示词 / RAG 总结 / 报告模板
├── rag/
│   ├── vector_store.py       # Chroma 向量库封装
│   └── rag_service.py        # 检索 + PromptTemplate + 输出解析链
├── utils/                    # 配置 / 日志 / 文件 / 路径 / 提示词加载
├── app.py                    # Streamlit 入口
└── test.py                   # 模型连通性冒烟测试
```

## 快速开始

```bash
pip install -r requirements.txt

# 配置通义千问 API Key
export DASHSCOPE_API_KEY=your-api-key   # Windows: set DASHSCOPE_API_KEY=your-api-key

streamlit run app.py
```

## 技术栈

LangChain 0.2 · LangGraph 0.2 · Chroma 0.5 · DashScope（qwen / text-embedding-v4）· Streamlit · Pydantic · PyYAML
