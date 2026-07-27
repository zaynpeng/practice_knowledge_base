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
