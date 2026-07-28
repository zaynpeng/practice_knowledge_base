# 实践型知识库

本项目是一个本地运行的 Flask + SQLite 网页工具，用来把收藏、书籍和读书感悟推进到最小实践，并把有效结论导出到 Obsidian Markdown。

## 安装方法

需要 Windows 和 Python 3.10 或更新版本。进入 `practice_knowledge_base` 目录后运行：

```bat
start.bat
```

脚本会创建 `.venv`、安装依赖并启动服务。

## 启动方法

启动后访问：

```text
http://127.0.0.1:5000
```

也可以手动运行：

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 数据保存位置

SQLite 数据库保存在：

```text
data/knowledge.db
```

上传附件保存在：

```text
attachments/
```

## 备份方法

进入“导出与备份”页面，点击“一键备份 SQLite”。备份文件会生成在：

```text
backups/knowledge_backup_YYYYMMDD_HHMMSS.db
```

## 恢复方法

进入“导出与备份”页面上传 `.db` 文件。恢复前系统会自动备份当前数据库，随后覆盖 `data/knowledge.db`。

## Obsidian 导出方法

在内容详情、实践详情、读书感悟列表点击“导出 Markdown”。导出文件会生成在：

```text
exports/markdown/
```

系统只为已关联的真实问题生成 Obsidian 双链，不会虚构文件。

## AI 配置方法

进入“设置”页面填写服务商、API URL、API Key 和模型名称。API URL 使用 OpenAI-compatible 的聊天接口地址，例如服务根地址或 `/chat/completions` 地址。

快速收藏支持“一体化输入”：用户只需要填写链接或原文，以及一段个人想法。未配置 AI 时，系统会用本地关键词规则做基础拆分；配置 AI 后，系统会调用 API 将个人想法拆成“我的感触、为什么收藏、可能解决的问题、准备怎么用”等字段，并将摘要、工具、方法、场景作为 AI 建议保存。

AI 只作为可选建议模块，不会覆盖已手动填写的字段；未配置时所有核心功能可正常使用。

## 常见错误处理

链接读取失败：内容仍可保存，页面会显示“读取失败”并保留你填写的感触、收藏原因和手动正文。

Excel 导入失败：确认文件是 `.xlsx`，并已安装 `openpyxl`。CSV 建议使用 UTF-8 或 UTF-8 BOM。

端口被占用：修改 `app.py` 最后一行的 `port=5000` 为其他端口。

## 功能清单

- 首页行动看板
- 快速收藏链接和手动正文
- 基础网页标题与正文提取
- 内容库搜索筛选
- 内容详情、附件上传、问题关联
- 内容转实践
- 实践看板和状态校验
- 问题地图聚合
- 书籍手动录入
- CSV / Excel 书籍导入
- 读书感悟记录和转实践
- Markdown / JSON / CSV 导出
- SQLite 备份与恢复
- AI 可选配置入口
- 软删除

## 已知限制

- 不支持 OCR、浏览器插件、云同步和多用户。
- 动态网页、登录页、反爬页面可能无法提取正文。
- 第一版没有完整 AI 调用流程，只保留安全边界和配置入口。
- 删除是软删除，暂未提供独立回收站页面。
