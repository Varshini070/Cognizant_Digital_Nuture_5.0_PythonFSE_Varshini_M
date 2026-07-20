import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");

courses.forEach((course) => {
  const { name, code, credits } = course;

  const article = document.createElement("article");

  article.className = "course-card";

  article.innerHTML = `
        <h3>${name}</h3>
        <p>${code}</p>
        <span>Credits: ${credits}</span>
    `;

  courseGrid.appendChild(article);
});

const formattedCourses = courses.map(
  (course) => `${course.code} - ${course.name} (${course.credits} credits)`,
);

console.log(formattedCourses);

const heavyCourses = courses.filter((course) => course.credits >= 4);

console.log(heavyCourses);

console.log(heavyCourses.length);

const totalCredits = courses.reduce(
  (total, course) => total + course.credits,
  0,
);

console.log(totalCredits);

const totalCreditsElement = document.querySelector("#total-credits");

totalCreditsElement.textContent = `Total Credits: ${totalCredits}`;
