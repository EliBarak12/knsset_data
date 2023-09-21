let webText = document.querySelector(".webText");
let loginBox = document.getElementById("login-box");
let registerButton = document.querySelector(".register-button");
let loginButton = document.querySelector(".login-button");
let registrationForm = document.querySelector(".registration-form");
let loginForm = document.querySelector(".login-form");
let confirm = document.querySelector("#Confirm-password")

webText.style.animationPlayState = "running";

registerButton.addEventListener("click", showRegistrationForm);
loginButton.addEventListener("click", showLoginForm);

function showRegistrationForm() {
    registrationForm.style.display = "flex";
    loginForm.style.display = "none";
    registerButton.style.display = "none";
    loginButton.style.display = "none";
    
}

function showLoginForm() {
    loginForm.style.display = "flex";
    registrationForm.style.display = "none";
    registerButton.style.display = "none";
    loginButton.style.display = "none";
}

