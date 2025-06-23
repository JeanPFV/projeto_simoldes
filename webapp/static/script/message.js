document.addEventListener("DOMContentLoaded", function () {
  const popup = document.getElementById('popup-msg');
  if (popup) {
    setTimeout(function () {
      popup.classList.add("fade-out");
    }, 2500);

    setTimeout(function () {
      popup.style.display = 'none';
    }, 3000);
  }
});