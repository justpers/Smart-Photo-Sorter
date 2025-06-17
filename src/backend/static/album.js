document.addEventListener("DOMContentLoaded", () => {
  let offset = 0,
      limit = 20,
      currentTag = "",
      endOfList = false;

  const container    = document.querySelector(".photo-container");
  const totalCountEl = document.getElementById("totalCount");
  const searchInput  = document.getElementById("tag-input");
  const searchBtn    = document.getElementById("searchBtn");
  const dupBtn       = document.getElementById("dupBtn");
  const exampleTags  = document.querySelectorAll(".example-tag");

  // ───────────────────────── 데이터 로드
  async function loadMore() {
    if (endOfList) return;
    const url = `/api/photos?tag=${encodeURIComponent(currentTag)}&limit=${limit}&offset=${offset}`;
    const res = await fetch(url, { credentials: "include" });
    if (!res.ok) return alert("사진 목록을 불러오지 못했습니다.");

    const { photos, count } = await res.json();
    renderPhotos(photos);
    totalCountEl.textContent = `Total count: ${count}`;
    offset += photos.length;
    if (photos.length < limit) endOfList = true;
  }

  // ───────────────────────── 렌더링 (썸네일 = a + img)
  function renderPhotos(list) {
    list.forEach(p => {
      const date = p.inserted_at.split("T")[0];

      // 날짜 헤더 + 그리드 생성
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

      // ── 썸네일 (a > img)
      const link = document.createElement("a");
      link.href  = `/photo/${p.id}`;
      link.className = "thumb";           // (선택) :hover 스타일용

      const img  = document.createElement("img");
      img.src    = `${SUPABASE_URL}/storage/v1/object/public/photos/${p.file_path}`;
      img.alt    = p.file_path.split("/").pop();
      img.loading = "lazy";
      img.style.width     = "100%";
      img.style.height    = "160px";
      img.style.objectFit = "cover";

      link.appendChild(img);
      grid.appendChild(link);
    });
  }

  // ───────────────────────── 검색
  function doSearch() {
    currentTag    = searchInput.value.trim();
    offset        = 0;
    endOfList     = false;
    container.innerHTML = "";
    container.appendChild(sentinel);
    loadMore().then(() => {
      if (offset === 0) {
        container.textContent = "아직 해당 태그는 존재하지 않습니다.";
      }
    });
  }

  searchBtn.addEventListener("click", doSearch);
  searchInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      doSearch();
    }
  });

  // 추천 태그
  exampleTags.forEach(btn =>
    btn.addEventListener("click", () => {
      const tag = btn.textContent.replace(/^#/, "");
      searchInput.value = tag;
      doSearch();
    })
  );
    if (dupBtn) {
    dupBtn.addEventListener("click", removeDuplicates);
  } else {
    console.warn("dupBtn element not found");
  }

  // ───────────────────────── 무한 스크롤
  const sentinel = document.createElement("div");
  const io = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) loadMore();
  }, { rootMargin: "300px" });

  loadMore().then(() => {
    container.appendChild(sentinel);
    io.observe(sentinel);
  });

  // // 중복 정리
  // dupBtn.addEventListener("click", () =>
  //   alert("중복 사진 정리 기능은 아직 준비 중입니다.")
  // );
  // 기존에 alert만 띄우던 stub 함수를 교체합니다.
  async function removeDuplicates() {
    try {
      // 1) 중복 그룹 가져오기 (✅ 인증 포함)
      const resp = await fetch("/api/duplicates", {
        credentials: "include",
        headers: { "Accept": "application/json" }
      });
      if (!resp.ok) {
        console.error("중복 조회 응답:", resp.status, await resp.text());
        throw new Error("중복 조회 실패");
      }
      const groups = await resp.json();

      if (groups.length === 0) {
        alert("중복 사진이 없습니다.");
        return;
      }

      // 2) delete 호출에도 인증 포함
      for (const grp of groups) {
        const keep_id    = grp[0];
        const delete_ids = grp.slice(1);
        if (!delete_ids.length) continue;

        const res2 = await fetch("/api/duplicates/resolve", {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ keep_id, delete_ids })
        });
        if (!res2.ok) {
          const errText = await res2.text();
          console.error("삭제 오류:", res2.status, errText);
          throw new Error("중복 사진 삭제 중 오류 발생");
        }
      }

      alert("중복 사진을 정리했습니다.");
      window.location.reload();
    } catch (e) {
      console.error(e);
      alert(e.message);
    }
  }
});