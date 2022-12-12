document.addEventListener("DOMContentLoaded", () => {
  const theme = localStorage.getItem("theme") ? localStorage.theme : "light";

  switch (theme) {
    case "light":
      setLight();
      break;
    case "dark":
      setDark();
      break;
  }
});
// ===================================================================================

function setDark() {
  document.body.classList.add("dark");
  document.querySelector("#sun").classList.remove("hidden");
  document.querySelector("#moon").classList.add("hidden");
}
function setLight() {
  document.body.classList.remove("dark");
  document.querySelector("#sun").classList.add("hidden");
  document.querySelector("#moon").classList.remove("hidden");
}

function toggleTheme() {
  if (localStorage.getItem("theme") == "light") {
    localStorage.setItem("theme", "dark");
    setDark();
  } else {
    localStorage.setItem("theme", "light");
    setLight();
  }
}
