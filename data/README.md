# CVD SOP 数据

## Neo4j 数据

文件：
- `neo4j_nodes.json` - 3132 个节点
- `neo4j_rels.json` - 2214 条关系

导入方法：
```bash
python3 import_neo4j.py
```

## Chroma SOP 向量库

文件：`chroma_sop_v3/` 目录（2.5MB）
- 193 个 chunk（CVD + 薄膜 SOP 文档）
- Embedding: herald/dmeta-embedding-zh (768维)

使用：直接指定路径即可，无需额外导入。
