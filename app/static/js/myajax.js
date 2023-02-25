// $(document).ready(function () {
//   $("#prev").click(function (e) {
//     // Stop form from sending request to server
//     e.preventDefault();
//     var btn = $(this);
//     $.ajax({
//       url: "{% url 'hello'%}",
//       type: 'get',
//       success: function(data) {
//         alert(data.res);
//       },
//       error: function(er) {
//         alert("ошибка");
//       },
//     });
//   });
// });
// $(document).ready(function () {
//   $.ajax({
//     url: "{% url 'cal:hello'%}",
//     type: "get", // This is the default though, you don't actually need to always mention it
//     success: function (data) {
//       alert(data.res);
//     },
//     failure: function (data) {
//       alert("Got an error dude");
//     },
//   });
// });
