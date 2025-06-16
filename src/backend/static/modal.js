document.addEventListener("DOMContentLoaded", () => {
  const openButtons = [
    { btnId: "loginBtn", modalId: "loginModal" },
    { btnId: "signupBtn", modalId: "signupModal" }
  ];
  openButtons.forEach(({btnId, modalId}) => {
    document.getElementById(btnId).addEventListener("click", e => {
      e.preventDefault();
      document.getElementById(modalId).style.display = "flex";
    });
  });

  // 닫기 버튼
  document.querySelectorAll(".modal .close").forEach(span => {
    span.addEventListener("click", () => {
      const target = span.getAttribute("data-target");
      document.getElementById(target).style.display = "none";
    });
  });

  // 모달 바깥 클릭 시 닫기
  document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("click", e => {
      if (e.target === modal) modal.style.display = "none";
    });
  });
});
