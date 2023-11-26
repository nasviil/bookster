
$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '{{ url_for("auth.login") }}',
            data: $('#login-form').serialize(),
            success: function(response) {
                if (response.success) {
                    window.location.href = '{{ url_for("home.home_page") }}';
                } else {
                    // Display the error message in the flash message element
                    $('#error-message').html('<ul><li>' + response.message + '<span class="close" onclick="this.parentElement.style.display=\'none\'">&times;</span></li></ul>');
                    $('#error-message').show(); // Show the error message element
                }
            },		
            error: function() {
                $('#error-message').html('<li>An error occurred. Please try again.<span class="close" onclick="this.parentElement.style.display=\'none\'">&times;</span></li>');
                $('#error-message').show(); // Show the error message element
            }
        });
    });
});
