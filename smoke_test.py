import tempfile
from pathlib import Path

import app as app_module


def main() -> None:
    temp_dir = tempfile.TemporaryDirectory()
    app_module.DB_PATH = Path(temp_dir.name) / "knowledge_test.db"
    app_module.init_db()
    client = app_module.app.test_client()
    paths = ["/", "/capture", "/contents", "/experiments", "/books", "/notes", "/problems", "/export", "/settings"]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, f"{path} returned {response.status_code}"

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
