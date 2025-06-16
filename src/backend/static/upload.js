// upload.js
document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.getElementById("dropzone");

  dropzone.addEventListener("click", e => {
    if (!isLoggedIn) {
      // 비로그인: 기본 동작(파일창) 막고, 모달 띄우기
      e.preventDefault();
      alert("사진 업로드 전에 로그인 해주세요.");
      document.getElementById("loginModal").style.display = "flex";
    }
    // 로그인 상태면 preventDefault 없이 기본 동작(파일창 오픈)이 자동으로 일어남
  });

  // 파일 선택되면 폼 제출
  const fileInput = document.getElementById("file-input");
  const form = document.getElementById("upload-form");
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) form.submit();
  });
});