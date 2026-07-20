import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.querySelector("#total-credits");
const loading = document.querySelector("#loading");

const postsContainer = document.querySelector("#posts");
const spinner = document.querySelector("#spinner");
const errorMessage = document.querySelector("#error-message");
const retryBtn = document.querySelector("#retry-btn");

function fetchUser(id) {
  return fetch("https://jsonplaceholder.typicode.com/users/" + id)
    .then((response) => response.json())
    .then((user) => {
      console.log("Promise User:", user.name);
    });
}

fetchUser(1);

async function fetchUserAsync(id) {
  try {
    const response = await fetch(
      "https://jsonplaceholder.typicode.com/users/" + id,
    );

    const user = await response.json();

    console.log("Async User:", user.name);
  } catch (error) {
    console.error(error);
  }
}

fetchUserAsync(2);

function fetchAllCourses() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(courses);
    }, 1000);
  });
}

function renderCourses(courseList) {
  courseGrid.innerHTML = "";

  courseList.forEach((course) => {
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

  const totalCredits = courseList.reduce(
    (sum, course) => sum + course.credits,
    0,
  );

  totalCreditsElement.textContent = `Total Credits: ${totalCredits}`;
}

loading.style.display = "block";

fetchAllCourses().then((courseList) => {
  loading.style.display = "none";

  renderCourses(courseList);
});

const formattedCourses = courses.map(
  ({ code, name, credits }) => `${code} - ${name} (${credits} credits)`,
);

console.log(formattedCourses);

const heavyCourses = courses.filter((course) => course.credits >= 4);

console.log(heavyCourses);

console.log("Courses with >=4 credits:", heavyCourses.length);

const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);

console.log("Total Credits:", totalCredits);

Promise.all([
  fetch("https://jsonplaceholder.typicode.com/users/1").then((res) =>
    res.json(),
  ),
  fetch("https://jsonplaceholder.typicode.com/users/2").then((res) =>
    res.json(),
  ),
]).then(([user1, user2]) => {
  console.log("Promise.all()");
  console.log(user1.name);
  console.log(user2.name);
});

async function apiFetch(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Error ${response.status}: Unable to fetch data`);
  }

  return response.json();
}

function renderPosts(posts) {
  postsContainer.innerHTML = "";

  posts.slice(0, 10).forEach((post) => {
    const card = document.createElement("article");

    card.className = "course-card";

    card.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.body}</p>
        `;

    postsContainer.appendChild(card);
  });
}

async function loadPosts() {
  spinner.style.display = "block";

  retryBtn.style.display = "none";

  errorMessage.textContent = "";

  postsContainer.innerHTML = "";

  try {
    const posts = await apiFetch("https://jsonplaceholder.typicode.com/posts");

    spinner.style.display = "none";

    renderPosts(posts);
  } catch (error) {
    spinner.style.display = "none";

    errorMessage.textContent = "Unable to load notifications.";

    retryBtn.style.display = "block";
  }
}

loadPosts();

async function simulate404() {
  try {
    await apiFetch("https://jsonplaceholder.typicode.com/nonexistent");
  } catch (error) {
    errorMessage.textContent = "404 Error! Resource not found.";
  }
}

simulate404();

retryBtn.addEventListener("click", () => {
  errorMessage.textContent = "";

  loadPosts();
});
