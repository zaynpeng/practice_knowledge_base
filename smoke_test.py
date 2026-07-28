import tempfile
from pathlib import Path

import app as app_module


def main() -> None:
    temp_dir = tempfile.TemporaryDirectory()
    app_module.DB_PATH = Path(temp_dir.name) / "knowledge_test.db"
    app_module.init_db()
    client = app_module.app.test_client()
    wechat_html = """
    <html><head>
      <meta property="og:title" content="公众号测试标题">
      <meta name="author" content="测试作者">
      <script>var publish_time = "2026-07-28";</script>
    </head><body>
      <div id="js_content">
        <p>这是公众号原文第一段，用来验证正文提取。</p>
        <p>这是公众号原文第二段，包含可执行的方法。</p>
      </div>
    </body></html>
    """
    extracted = app_module.extract_wechat_article("https://mp.weixin.qq.com/s/test", wechat_html)
    assert extracted["status"] == "读取成功"
    assert extracted["title"] == "公众号测试标题"
    assert "公众号原文第一段".encode("utf-8") in extracted["raw_text"].encode("utf-8")

    paths = ["/", "/capture", "/contents", "/experiments", "/books", "/notes", "/problems", "/export", "/settings"]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, f"{path} returned {response.status_code}"

    response = client.post("/settings/test-ai", json={"ai_model": "deepseek-chat", "ai_api_url": "https://api.deepseek.com", "ai_api_key": ""})
    assert response.status_code == 400
    assert "API Key".encode("utf-8") in response.data

    response = client.post(
        "/capture",
        data={
            "source_text": "https://example.com/article",
            "personal_note": "感想：这个思路提醒我要减少客户选择成本。为什么有用：它能解决报价后客户不回复的问题。打算怎么用：下次报价先给推荐方案，再给备选项。",
            "try_extract": "",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "减少客户选择成本".encode("utf-8") in response.data

    response = client.post(
        "/capture",
        data={
            "source_text": "旧正文第一句。旧正文第二句。",
            "personal_note": "感想：先保存一条内容。为什么有用：用于测试。打算怎么用：检查摘要刷新。",
            "summary": "旧摘要",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    content_id = int(response.request.path.rsplit("/", 1)[-1])
    response = client.post(
        f"/contents/{content_id}",
        data={
            "content_type": "article",
            "title": "摘要刷新测试",
            "url": "",
            "author": "",
            "source_platform": "",
            "published_at": "",
            "summary": "旧摘要",
            "tools": "",
            "methods": "",
            "suggested_category": "",
            "applicable_scenarios": "",
            "user_reflection": "先保存一条内容",
            "save_reason": "用于测试",
            "problem_statement": "",
            "intended_use": "检查摘要刷新",
            "status": "待判断",
            "raw_text": "新正文第一句，应该进入摘要。新正文第二句，继续作为摘取式摘要。",
            "refresh_summary": "1",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "新正文第一句".encode("utf-8") in response.data
    assert "旧摘要".encode("utf-8") not in response.data

    response = client.post(
        "/experiments",
        data={"title": "校验失败示例", "status": "已验证"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "实际结果".encode("utf-8") in response.data

    response = client.post(
        "/experiments",
        data={
            "title": "校验成功示例",
            "status": "已验证",
            "actual_result": "完成一次最小测试",
            "final_decision": "保留这个方法",
            "reusable_conclusion": "先做小范围验证，再扩大投入",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    print("smoke test ok")
    temp_dir.cleanup()


if __name__ == "__main__":
    main()
