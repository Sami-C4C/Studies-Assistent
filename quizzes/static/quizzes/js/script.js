// JavaScript for showing/hiding the mobile menu
const menuToggle = document.querySelector(".menu-toggle");
const mobileMenu = document.querySelector(".mobile-menu ul");

menuToggle.addEventListener("click", () => {
  // Toggle the visibility of the mobile menu
  if (mobileMenu.style.display === "block") {
    mobileMenu.style.display = "none";
  } else {
    mobileMenu.style.display = "block";
  }
});
