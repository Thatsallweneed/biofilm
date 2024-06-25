"use strict";

///////////////////////
// Selecting Elements
const form = document.querySelector("form");

const emailField = form.querySelector(".email-field");
const emailInput = emailField.querySelector(".email");

const passField = form.querySelector(".create-password");
const passInput = passField.querySelector(".Password");

const cpassField = form.querySelector(".confirm-password");
const cpassInput = cpassField.querySelector(".cPassword");

//////////////////////////
// Hide and Show Password
const eyeIcons = document.querySelectorAll(".show-hide");

eyeIcons.forEach((eyeIcon) => {
  eyeIcon.addEventListener("click", () => {
    // Get The Parent El
    const PInput = eyeIcon.parentElement.querySelector("input");

    if (PInput.type === "password") {
      eyeIcon.classList.replace("bx-hide", "bx-show");
      return (PInput.type = "text");
    } else {
      eyeIcon.classList.replace("bx-show", "bx-hide");
      PInput.type = "password";
    }
  });
});

///////////////////////
// Email Validation
function checkEmail() {
  const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

  if (!emailInput.value.match(emailPattern)) {
    // Add invalid class if does not match
    return emailField.classList.add("invalid");
  } else {
    // Remove invalid class if it does match
    emailField.classList.remove("invalid");
  }
}

///////////////////////////////
// Create Password Validation
function CreatePassword() {
  const passpattern =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

  if (!passInput.value.match(passpattern)) {
    // Add invalid class if does not match
    return passField.classList.add("invalid");
  } else {
    // Remove invalid class if it does match
    passField.classList.remove("invalid");
  }
}

///////////////////////////////
// Confirm Password Validation
function ConfirmPassword() {
  if (passInput.value !== cpassInput.value || cpassInput.value === "") {
    return cpassField.classList.add("invalid");
  } else {
    cpassField.classList.remove("invalid");
  }
}

///////////////////////////////////
// calling Function on Form Submit
form.addEventListener("submit", (e) => {
  e.preventDefault(); // Preventing Form Submitting

  checkEmail();
  CreatePassword();
  ConfirmPassword();

  // Calling Function on Keyup
  emailInput.addEventListener("keyup", checkEmail);
  passInput.addEventListener("keyup", CreatePassword);
  cpassInput.addEventListener("keyup", ConfirmPassword);

  if (
    !emailField.classList.contains("invalid") &&
    !passField.classList.contains("invalid") &&
    !cpassField.classList.contains("invalid")
  ) {
    location.href = form.getAttribute("action");
  }
});