document.addEventListener("DOMContentLoaded", () => {
  let offset = 0, limit = 20, currentTag = "", endOfList = false;
  const container    = document.querySelector(".photo-container");
  const totalCountEl = document.getElementById("totalCount");

  async function loadMore() {
    if (endOfList) return;
    const url = `/api/photos?tag=${encodeURIComponent(currentTag)}&limit=${limit}&offset=${offset}`;
    const res = await fetch(url, { credentials: "include" });
    if (!res.ok) return;
    const { photos, count } = await res.json();
    renderPhotos(photos);
    totalCountEl.textContent = `Total count: ${count}`;
    offset += photos.length;
    if (photos.length < limit) endOfList = true;
  }

  // ───────────────────────── 렌더링
  function renderPhotos(list) {
    list.forEach(p => {
      const date = p.inserted_at.split("T")[0];

      /* 날짜 헤더 + 그리드 생성 */
      let grid = document.querySelector(`#date-${date} + .grid`);
      if (!grid) {
        const h4 = document.createElement("h4");
        h4.id = `date-${date}`;
        h4.textContent = date;
        h4.style.margin = "24px 0 12px";
        h4.style.fontWeight = "600";
        container.appendChild(h4);

        grid = document.createElement("div");
        grid.className = "grid";
        grid.style.display = "grid";
        grid.style.gridTemplateColumns = "repeat(auto-fill, minmax(160px,1fr))";
        grid.style.gap = "10px";
        container.appendChild(grid);
      }

      /* 썸네일 이미지 */
      const img = document.createElement("img");
      img.src = `${SUPABASE_URL}/storage/v1/object/public/photos/${p.file_path}`;
      img.alt = p.file_path.split("/").pop();
      img.style.width = "100%";
      img.style.height = "160px";
      img.style.objectFit = "cover";
      img.loading = "lazy";
      grid.appendChild(img);
    });
  }
  
  // ───────────────────────── 초기 로드 및 무한 스크롤 세팅
  const sentinel = document.createElement("div");
  const io = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) loadMore();
  }, { rootMargin: "300px" });

  // **여기서만 한 번** loadMore() 호출 → 이후 스크롤 감지로 추가 로드
  loadMore().then(() => {
    container.appendChild(sentinel);
    io.observe(sentinel);
  });

  // ───────────────────────── 검색 & 중복정리
  document.getElementById("searchBtn").addEventListener("click", () => {
    currentTag = document.getElementById("tag-input").value.trim();
    offset = 0; endOfList = false;
    container.innerHTML = "";
    container.appendChild(sentinel);
    loadMore().then(() => {
      if (offset === 0) container.textContent = "아직 해당 태그는 존재하지 않습니다.";
    });
  });

  document.getElementById("dupBtn").onclick = () =>
    alert("중복 사진 정리 기능은 아직 준비 중입니다.");
});