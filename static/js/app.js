const searchInput = document.querySelector("#globalSearch");
const searchResults = document.querySelector("#searchResults");

if (searchInput && searchResults) {
  let timer;
  searchInput.addEventListener("input", () => {
    clearTimeout(timer);
    const q = searchInput.value.trim();
    if (!q) {
      searchResults.style.display = "none";
      searchResults.innerHTML = "";
      return;
    }
    timer = setTimeout(async () => {
      const response = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const rows = await response.json();
      searchResults.innerHTML = rows.length
        ? rows.map((r) => `<a href="${r.url}"><strong>${r.kind}</strong> ${escapeHtml(r.title || "")}</a>`).join("")
        : `<a>没有找到结果</a>`;
      searchResults.style.display = "block";
    }, 180);
  });
  document.addEventListener("click", (event) => {
    if (!searchResults.contains(event.target) && event.target !== searchInput) {
      searchResults.style.display = "none";
    }
  });
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  }[char]));
}

const aiModelSelect = document.querySelector("#aiModelSelect");
const aiProviderInput = document.querySelector("#aiProvider");
const aiBaseUrlInput = document.querySelector("#aiBaseUrl");
const aiApiKeyInput = document.querySelector("#aiApiKey");
const testAiButton = document.querySelector("#testAiButton");
const testAiResult = document.querySelector("#testAiResult");

function syncAiPreset() {
  if (!aiModelSelect || !aiProviderInput || !aiBaseUrlInput) return;
  const option = aiModelSelect.selectedOptions[0];
  const provider = option?.dataset.provider || "";
  const baseUrl = option?.dataset.baseUrl || "";
  aiProviderInput.value = provider;
  if (baseUrl) {
    aiBaseUrlInput.value = baseUrl;
  }
}

if (aiModelSelect) {
  aiModelSelect.addEventListener("change", syncAiPreset);
  syncAiPreset();
}

if (testAiButton && testAiResult) {
  testAiButton.addEventListener("click", async () => {
    testAiResult.textContent = "正在测试...";
    testAiResult.className = "muted-text";
    try {
      const response = await fetch("/settings/test-ai", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          ai_model: aiModelSelect?.value || "",
          ai_api_url: aiBaseUrlInput?.value || "",
          ai_api_key: aiApiKeyInput?.value || "",
        }),
      });
      const payload = await response.json();
      testAiResult.textContent = payload.message;
      testAiResult.className = payload.ok ? "muted-text success-text" : "muted-text error-text";
    } catch (error) {
      testAiResult.textContent = `连接失败：${error}`;
      testAiResult.className = "muted-text error-text";
    }
  });
}
