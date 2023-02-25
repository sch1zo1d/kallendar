const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

fistForm.addEventListener("submit", (e) => e.preventDefault());
secondForm.addEventListener("submit", (e) => e.preventDefault());

$(document).ready(function () {
  // отслеживаем событие отправки формы
  $("#id_username").keyup(function () {
    // создаем AJAX-вызов
    $.ajax({
      data: $(this).serialize(), // получаяем данные формы
      url: "{% url 'cal:validate_username' %}",
      // если успешно, то
      success: function (response) {
        if (response.is_taken == true) {
          $("#id_username").removeClass("is-valid").addClass("is-invalid");
          $("#id_username").after(
            '<div class="invalid-feedback d-block" id="usernameError">Это имя пользователя недоступно!</div>'
          );
        } else {
          $("#id_username").removeClass("is-invalid").addClass("is-valid");
          $("#usernameError").remove();
        }
      },
      // если ошибка, то
      error: function (response) {
        // предупредим об ошибке
        console.log(response.responseJSON.errors);
      },
    });
    return false;
  });
});
