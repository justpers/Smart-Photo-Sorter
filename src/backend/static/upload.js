document.addEventListener("DOMContentLoaded", () => {
  const dropzone     = document.getElementById("dropzone");
  const fileInput    = document.getElementById("file-input");
  const progressWrap = document.getElementById("progress-wrapper");
  const progressBar  = document.getElementById("progress-bar");
  const loginModal   = document.getElementById("loginModal");

  function uploadFiles(files) {
    if (!isLoggedIn) {
      alert("사진 업로드 전에 로그인 해주세요.");
      loginModal.style.display = "flex";
      return;
    }

    // 진행률 UI 초기화
    progressBar.style.width = "0%";
    progressWrap.style.display = "block";

    const formData = new FormData();
    for (let file of files) {
      formData.append("files", file);
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/upload", true);
    xhr.withCredentials = true;

    xhr.upload.onprogress = e => {
      if (e.lengthComputable) {
        const pct = Math.round((e.loaded / e.total) * 100);
        progressBar.style.width = pct + "%";
      }
    };

    xhr.onload = () => {
      progressWrap.style.display = "none";
      if (xhr.status === 200) {
        alert("업로드 완료됐습니다!");
      } else {
        let msg = xhr.responseText;
        try{
          const err = JSON.parse(xhr.responseText);
          msg = err.detail || JSON.stringify(err);
        } catch {}
        alert("업로드 실패:" + msg);
      }
      fileInput.value = "";  // 선택 리셋
    };

    xhr.onerror = () => {
      alert("업로드 중 오류가 발생했습니다.");
      progressWrap.style.display = "none";
    };

    xhr.send(formData);
  }

  // 클릭으로 다이얼로그 열기 (라벨 기본동작)
  dropzone.addEventListener("click", e => {
    if (!isLoggedIn) {
      e.preventDefault();
      alert("사진 업로드 전에 로그인 해주세요.");
      loginModal.style.display = "flex";
    }
    // 로그인 시엔 preventDefault() 없이 라벨 기본동작으로 파일창 open
  });

  // 파일 선택
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
      uploadFiles(fileInput.files);
    }
  });

  // 드래그앤드롭
  ;["dragenter","dragover"].forEach(evt =>
    dropzone.addEventListener(evt, e => e.preventDefault())
  );
  dropzone.addEventListener("drop", e => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      uploadFiles(e.dataTransfer.files);
    }
  });
});
