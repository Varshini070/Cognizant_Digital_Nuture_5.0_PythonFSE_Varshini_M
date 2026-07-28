const menuButton = document.getElementById("menuButton");
const navigation = document.getElementById("mainNav");

menuButton.addEventListener("click", () => {
  const expanded = menuButton.getAttribute("aria-expanded") === "true";

  menuButton.setAttribute("aria-expanded", !expanded);

  navigation.classList.toggle("show");
});

const searchInput = document.getElementById("search");

const courseCards = document.querySelectorAll(".course-card");

const resultsCount = document.getElementById("resultsCount");

searchInput.addEventListener("input", function () {
  const value = this.value.toLowerCase();

  let visible = 0;

  courseCards.forEach((card) => {
    const title = card.querySelector("h3").textContent.toLowerCase();

    if (title.includes(value)) {
      card.style.display = "block";

      visible++;
    } else {
      card.style.display = "none";
    }
  });

  resultsCount.textContent = `${visible} course${visible !== 1 ? "s" : ""} found`;
});

document.querySelectorAll(".course-card button").forEach((button) => {
  button.addEventListener("click", () => {
    alert("Successfully enrolled!");
  });
});

courseCards.forEach((card) => {
  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      const enrollButton = card.querySelector("button");

      enrollButton.click();
    }
  });
});

document.querySelectorAll("button, a, input").forEach((element) => {
  element.addEventListener("focus", () => {
    console.log("Focused:", element.tagName);
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Tab") {
    console.log("Keyboard navigation active");
  }
});

window.addEventListener("load", () => {
  const visibleCourses = [...courseCards].filter(
    (card) => card.style.display !== "none",
  ).length;

  resultsCount.textContent = `${visibleCourses} courses found`;
});
