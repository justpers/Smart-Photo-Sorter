document.addEventListener("DOMContentLoaded", () => {
  const dropzone  = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const form      = document.getElementById("upload-form");
  const loginModal = document.getElementById("loginModal");

  // 1) 드롭존 클릭
  dropzone.addEventListener("click", e => {
    if (!isLoggedIn) {
      e.preventDefault();
      alert("사진 업로드 전에 로그인 해주세요.");
      loginModal.style.display = "flex";
      return;
    }
    // 로그인된 경우: 아무것도 막지 않으면 <label for="file-input">가 파일창을 팝업시킵니다.
  });

  // 2) 파일 선택 시 자동 제출
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) form.submit();
  });

  // 3) 드래그&드롭 지원 (선택)
  ["dragenter","dragover"].forEach(evt =>
    dropzone.addEventListener(evt, e => e.preventDefault())
  );
  dropzone.addEventListener("drop", e => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      if (!isLoggedIn) {
        alert("사진 업로드 전에 로그인 해주세요.");
        loginModal.style.display = "flex";
        return;
      }
      // 드롭된 파일이 있으면 자동 제출
      form.upload.value = e.dataTransfer.files[0];
      form.submit();
    }
  });
});
