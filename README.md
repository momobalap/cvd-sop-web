# CVD SOP Assistant

CVD 薄膜机台异常处理智能问答系统，包含：
- 🎨 深色主题 Web UI（React + TypeScript + TailwindCSS）
- 🔍 Neo4j 图谱（实体关系查询）
- 📚 RAG 向量检索（SOP 文档理解）
- 🤖 LLM 智能润色回答

![界面预览](public/preview.png)

## 快速开始

### 1. 克隆

```bash
git clone https://github.com/momobalap/cvd-sop-web.git
cd cvd-sop-web
```

### 2. 安装依赖

```bash
# 前端
npm install

# 后端 Python 依赖
pip3 install flask flask-cors neo4j chromadb requests
```

### 3. 导入数据

```bash
# Neo4j（需要先启动 Neo4j）
python3 data/import_neo4j.py

# Chroma 向量库（已包含在 data/chroma_sop_v3/）
# 无需额外导入
```

### 4. 启动

```bash
# 终端 1：后端 API
python3 server.py

# 终端 2：前端
npm run dev
```

访问 http://localhost:5173

## 项目结构

```
cvd-sop-web/
├── src/                    # React + TypeScript 前端
│   ├── App.tsx             # 主界面
│   └── index.css           # 深色主题样式
├── tools/                  # 查询工具
│   ├── neo4j_query_tool.py # Neo4j 图谱查询
│   ├── rag_query_tool.py   # RAG 向量检索
│   └── polish_tool.py      # LLM 润色
├── server.py               # Flask API 服务
├── data/                   # 数据文件
│   ├── neo4j_nodes.json    # 3132 个节点
│   ├── neo4j_rels.json    # 2214 条关系
│   ├── import_neo4j.py     # Neo4j 导入脚本
│   └── chroma_sop_v3/       # SOP 向量库（193 chunks）
├── vite.config.ts
└── package.json
```

## 环境变量

```bash
# Neo4j
NEO4J_URI=bolt://localhost:17687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Ollama（embedding + LLM）
OLLAMA_URL=http://localhost:11434
LLM_MODEL=qwen3:4b
EMBED_MODEL=herald/dmeta-embedding-zh:latest

# Chroma 向量库
CHROMA_PATH=./data/chroma_sop_v3
```

## 数据来源

- **Neo4j**：CVD 设备管控作业指导书 + 薄膜产品异常处理作业指导书（三元组抽取）
- **Chroma SOP**：同文档，600字分块，overlap 100，193 个 chunk
