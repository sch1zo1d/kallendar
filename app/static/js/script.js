function initCalendar() {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const prevLastDay = new Date(year, month, 0);
  const prevDays = prevLastDay.getDate();
  const lastDate = lastDay.getDate();
  const day = firstDay.getDay();
  const nextDays = 7 - lastDay.getDay() - 1;

  date.innerHTML = months[month] + " " + year;

  let days = "";

  for (let x = day; x > 0; x--) {
    days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDate; i++) {
    //check if event is present on that day
    let event = false;
    eventsArr.forEach((eventObj) => {
      if (
        eventObj.day === i &&
        eventObj.month === month + 1 &&
        eventObj.year === year
      ) {
        event = true;
      }
    });
    if (
      i === new Date().getDate() &&
      year === new Date().getFullYear() &&
      month === new Date().getMonth()
    ) {
      activeDay = i;
      getActiveDay(i);
      updateEvents(i);
      if (event) {
        days += `<div class="day today active event">${i}</div>`;
      } else {
        days += `<div class="day today active">${i}</div>`;
      }
    } else {
      if (event) {
        days += `<div class="day event">${i}</div>`;
      } else {
        days += `<div class="day ">${i}</div>`;
      }
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="day next-date">${j}</div>`;
  }
  daysContainer.innerHTML = days;
  addListner();
}

//function to add month and year on prev and next button
function prevMonth() {
  month--;
  if (month < 0) {
    month = 11;
    year--;
  }
  initCalendar();
}

function nextMonth() {
  month++;
  if (month > 11) {
    month = 0;
    year++;
  }
  initCalendar();
}

prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);

initCalendar();






<script>
$("#prev").click(function () {
var input = $('#user-input').val();

$.ajax({
	url: '{% url 'get_response' %}',
	data: {
		'inputValue': input
	},
	dataType: 'json',
	success: function (data) {
		document.getElementById('p-text').innerHTML = data["response"];
	}
	});
});

$("#next").click(function () {
    var input = $('#user-input').val();

    $.ajax({
        url: '{% url 'get_response' %}',
        data: {
          'inputValue': input
        },
        dataType: 'json',
        success: function (data) {
          document.getElementById('p-text').innerHTML = data["response"];
        }
      });
    });

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
                  $("#id_username")
                    .removeClass("is-valid")
                    .addClass("is-invalid");
                  $("#id_username").after(
                    '<div class="invalid-feedback d-block" id="usernameError">Это имя пользователя недоступно!</div>'
                  );
                } else {
                  $("#id_username")
                    .removeClass("is-invalid")
                    .addClass("is-valid");
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
</script>