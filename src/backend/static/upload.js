document.addEventListener("DOMContentLoaded", () => {
  // upload 전에 로그인 체크
  const form = document.getElementById("upload-form");
  form.addEventListener("submit", e => {
    if (!isLoggedIn) {
      e.preventDefault();
      alert("사진 업로드 전에 로그인 해주세요.");
      document.getElementById("loginModal").style.display = "flex";
    }
  });

  // 파일 고르면 자동으로 submit
  const fileInput = document.getElementById("file-input");
  fileInput.addEventListener("change", () => {
    form.submit();
  });
});