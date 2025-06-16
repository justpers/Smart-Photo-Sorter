document.addEventListener("DOMContentLoaded", () => {
  const dropzone       = document.getElementById("dropzone");
  const fileInput      = document.getElementById("file-input");
  const progressWrap   = document.getElementById("progress-wrapper");
  const progressBar    = document.getElementById("progress-bar");
  const loginModal     = document.getElementById("loginModal");

  // 실제 업로드 실행 함수
  function uploadFile(file) {
    // 1) 로그인 체크
    if (!isLoggedIn) {
      alert("사진 업로드 전에 로그인 해주세요.");
      loginModal.style.display = "flex";
      return;
    }

    // 2) 진행률 UI 초기화
    progressBar.style.width = "0%";
    progressWrap.style.display = "block";

    // 3) XHR 로 파일 전송
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);

    // 업로드 진행 이벤트
    xhr.upload.onprogress = e => {
      if (e.lengthComputable) {
        const pct = Math.round(e.loaded / e.total * 100);
        progressBar.style.width = pct + "%";
      }
    };

    xhr.onload = () => {
      if (xhr.status === 200) {
        // 업로드 성공
        alert("업로드 완료됐습니다!");
      } else {
        alert("업로드 실패: " + xhr.responseText);
      }
      // UI 리셋
      progressWrap.style.display = "none";
      fileInput.value = "";          // 선택 초기화
    };
    xhr.onerror = () => {
      alert("업로드 중 오류가 발생했습니다.");
      progressWrap.style.display = "none";
    };

    // FormData에 담아서 전송
    const formData = new FormData();
    formData.append("file", file);
    xhr.send(formData);
  }

  // —— 클릭으로 파일선택
  dropzone.addEventListener("click", e => {
    if (!isLoggedIn) {
      e.preventDefault();
      alert("사진 업로드 전에 로그인 해주세요.");
      loginModal.style.display = "flex";
      return;
    }
    // 로그인 됐으면 기본 라벨 동작: 파일 대화상자 열림
  });

  // —— 파일 선택(브라우저 다이얼로그) 후
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
      uploadFile(fileInput.files[0]);
    }
  });

  // —— 드래그앤드롭 지원(optional)
  ["dragenter","dragover"].forEach(evt => {
    dropzone.addEventListener(evt, e => e.preventDefault());
  });
  dropzone.addEventListener("drop", e => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (!isLoggedIn) {
      alert("사진 업로드 전에 로그인 해주세요.");
      loginModal.style.display = "flex";
      return;
    }
    if (files.length) {
      uploadFile(files[0]);
    }
  });
});
