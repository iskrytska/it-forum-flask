document.addEventListener('DOMContentLoaded', () => {
  const loginSection = document.getElementById('login-section');
  const registerSection = document.getElementById('register-section');

  const showRegisterForm = document.getElementById('show-register-form');
  const showLoginForm = document.getElementById('show-login-form');

  showRegisterForm.addEventListener('click', (e) => {
    e.preventDefault();
    loginSection.style.display = 'none';
    registerSection.style.display = 'block';
  });

  showLoginForm.addEventListener('click', (e) => {
    e.preventDefault();
    registerSection.style.display = 'none';
    loginSection.style.display = 'block';
  });
  // Проста взаємодія: показати alert при завантаженні
window.addEventListener("DOMContentLoaded", () => {
    console.log("Сторінка завантажена успішно!");
});

});
