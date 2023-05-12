$(document).ready(function() {
  $('#login-form').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    var url = form.attr('');
    var data = form.serialize();
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      success: function(response) {
        window.location.href = response.redirect_url;
      },
      error: function(response) {
        console.log(response)
        $('.error-message').innerHTML = "Usuário ou senha incorretos"
      }
    });
  });
});