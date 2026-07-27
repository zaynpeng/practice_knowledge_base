from app import init_db, now
import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "data" / "knowledge.db"
init_db()

with sqlite3.connect(db_path) as db:
    exists = db.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
    if exists:
        print("示例数据已存在，跳过。")
        raise SystemExit
    ts = now()
    db.execute(
        "INSERT INTO problems(name,description,problem_type,importance,status,current_conclusion,next_action,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
        ("客户报价后不回复", "报价后客户沉默，无法判断是无需求、方案太复杂，还是跟进方式不合适。", "销售推进", "高", "正在探索", "", "收集可测试的跟进方法", ts, ts),
    )
    db.execute(
        "INSERT INTO books(title,author,category,problem_statement,relationship_status,reading_status,priority,is_read,user_note,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        ("影响力", "罗伯特·西奥迪尼", "心理学", "理解客户决策和说服机制", "近期可读", "准备阅读", "高", 0, "先找和报价决策相关的章节。", ts, ts),
    )
    db.commit()
print("示例数据已写入。")
