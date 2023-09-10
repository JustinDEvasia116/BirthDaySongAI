$(document).ready(function () {

    $(function () {
        $("#btn_redeem").click(function () {
            $("#modal_coupon").fadeIn();
        });
        $("#btn_close_modal").click(function () {
            $("#modal_coupon").css("display", "none");
        });
    });

    $(function () {
        var cpnBtn = document.getElementById("cpnBtn");
        var cpnCode = document.getElementById("cpnCode");

        cpnBtn.onclick = function () {
            navigator.clipboard.writeText(cpnCode.innerHTML);
            cpnBtn.innerHTML = "COPIED";
            setTimeout(function () {
                cpnBtn.className = 'fa fa-copy'
                cpnBtn.innerHTML = "";
            }, 3000);
        }
    });

    $(function () {
        $(".group_block").slice(0, 1).show();
        $("#loadmore").click(function (e) {
            e.preventDefault();
            $(".group_block:hidden").slice(0, 1).fadeIn("slow");

            if ($(".group_block:hidden").length == 0) {
                $("#loadmore").attr("disabled", true);
            }
        });
    });
    $(function () {
        window.onload = function () {
            let player = document.getElementById("player"),
                play = document.getElementById("play");
            play.addEventListener("click", function () {
                player.play();
            });
        }
    });

    $(function () {
        $('#btn_openModal').click(function () {
            var phone = $('#phone').val();
            var name = $('#name').val();
            var email = $('#email').val();
            var termsChecked = $('#termsCheckbox').is(':checked'); // Check if the checkbox is checked

            // Regular expressions for validation
            var emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
            var nameRegex = /^[A-Za-z]+$/; // Single Name
            var phoneRegex = /^\d{10}$/; // 10-digit phone number

            if (phone === '' || !phone.match(phoneRegex)) {
                toastr.error('Phone should be 10 digits long');
                return false;
            }
            if (name === '' || !name.match(nameRegex)) {
                toastr.error('Enter a valid name');
                return false;
            }
            if (email === '' || !email.match(emailRegex)) {
                toastr.error('Email cannot be left blank and should be a valid email address');
                return false;
            }
            if (!termsChecked) {
                toastr.error('Please accept the Terms & Conditions');
                return false;
            }
            $.ajax({
                type: 'POST',
                url: '/generate_otp/', //  OTP generation view
                data: {
                    phone: phone,
                    name: name,
                    email: email,
                    csrfmiddlewaretoken: csrf_token
                },
                success: function (response) {
                    if (response.success) {
                        toastr.success('OTP generated successfully');
                        // Handle the generated OTP (e.g., display it to the user)
                        toastr.options = {
                            timeOut: 0, // Set timeOut to 0 to make it persistent
                            closeButton: true, // Allow the user to close the toast
                            progressBar: true, // Show a progress bar
                            positionClass: 'toast-top-center' // Adjust position as needed
                        };
                        toastr.success('OTP: ' + response.otp);

                        console.log('Generated OTP:', response.otp);
                    } else {
                        toastr.error('Failed to generate OTP');
                    }
                },
                error: function () {
                    toastr.error('Error sending request to generate OTP');
                }
            });

            $('#addEventModal').addClass('modal_active');
            return true;
        });
    });

    $(function () {
        $('#btnsubmit').click(function (event) {
            event.preventDefault(); // Prevent the default form submission behavior
            
            var otpFields = $('.modal_fill .field_input');
            var phone = $('#phone').val();
            
    
            // Check if all OTP fields are filled
            var isOtpValid = true;
            var otpValue = "";
    
            otpFields.each(function () {
                var fieldValue = $(this).val();
    
                if (fieldValue === '') {
                    toastr.options = {
                        timeOut: 2000, // Set timeOut to 0 to make it persistent
                        closeButton: false, // Allow the user to close the toast
                        progressBar: true, // Show a progress bar
                        positionClass: 'toast-top-center' // Adjust position as needed
                    };
                    toastr.error('OTP cannot be blank.');
                    isOtpValid = false;
                    return false; // Break out of the loop if any field is empty
                }
    
                otpValue += fieldValue;
            });
    
            if (isOtpValid) {
                // Set the value of the hidden input field
                $('#otpValue').val(otpValue);
                // Now otpValue contains the merged OTP as a single string
    
                // Send an AJAX request to verify the OTP on the server
                $.ajax({
                    type: 'POST',
                    url: '/verify_otp/', 
                    data: {
                        otpValue: otpValue,
                        phone: phone,
                        csrfmiddlewaretoken: csrf_token
                    },
                    success: function (response) {
                        if (response.success) {
                            // OTPs match, proceed with form submission or other actions
                            toastr.success('OTP verified successfully');
                            // Manually trigger form submission
                            window.location.href = '/addnew/';

                        } else {
                            // OTPs do not match, show an error message
                            toastr.options = {
                                timeOut: 2000, // Set timeOut to 0 to make it persistent
                                closeButton: false, // Allow the user to close the toast
                                progressBar: true, // Show a progress bar
                                positionClass: 'toast-top-center' // Adjust position as needed
                            };
                            toastr.error('Invalid OTP');
                        }
                    },
                    error: function () {
                        toastr.error('Error verifying OTP');
                    }
                });
            }
        });
    });
    
    $(function () {
        $('#submit_addnew').click(function (event) {
            event.preventDefault(); // Prevent the default form submission behavior
    
            // Get the values from the form fields
            var name = $('#name').val();
            var age = $('#age').val();
            var gender = $('#gender').val();
    
            // Regular expression to check if the name contains only alphabetical characters
            var nameRegex = /^[A-Za-z]+$/;
    
            // Flag to track validation result
            var validationPassed = true;
    
            // Check if the name field is empty or doesn't match the regex
            if (name === '' || !name.match(nameRegex)) {
                // Display a toast error message for the name field
                toastr.error('Enter a valid name');
                validationPassed = false;
            }
    
            // Check if the age field is empty
            if (age === '') {
                // Display a toast error message for the age field
                toastr.error('Age field cannot be empty');
                validationPassed = false;
            }
    
            // Check if the gender field is empty
            if (gender === '') {
                // Display a toast error message for the gender field
                toastr.error('Gender field cannot be empty');
                validationPassed = false;
            }
    
            // If validation passes, submit the form manually
            if (validationPassed) {
                console.log("validation passed")
                $('.fill_form').submit();
            }
        });
    });

    $(function () {
        $('#select_btn').click(function (event) {
            event.preventDefault(); // Prevent the default form submission behavior
    
            // Get the selected mood and genre values
            const selectedMood = $('input[name="mood"]:checked').val();
            const selectedGenre = $('input[name="genre"]:checked').val();
    
            // Check if at least one mood and one genre are selected
            if (!selectedMood || !selectedGenre) {
                // Display an error message with a toast
                toastr.error('Please select both a Mood and a Genre.');
                return false;
            }
    
            // Send the selected mood and genre to the server using AJAX
            $.ajax({
                type: 'POST',
                url: '/choices/', 
                data: {
                    mood: selectedMood,
                    genre: selectedGenre,
                    csrfmiddlewaretoken: csrf_token
                },
                success: function (response) {
                    if (response.success) {
                        // Redirect to the next page after successful submission
                        window.location.href = '/detail/';
                    } else {
                        // Handle errors with a toast message
                        toastr.error('Something went wrong.');
                    }
                },
                error: function () {
                    // Handle AJAX error with a toast message
                    toastr.error('Error while sending data to the server.');
                }
            });
        });
    }); 

    $(function () {
        $('#proceedBtn').click(function (event) {
            event.preventDefault(); // Prevent the default form submission behavior
    
            // Get the input field values
            var petName = $('#petname').val();
            var angry = $('#angry').val();
            var funny = $('#funny').val();
            var movie = $('#movie').val();
            var sport = $('#sport').val();
            var smile = $('#smile').val();
    
            // Check if any of the fields are empty
            if (petName === "" || angry === "" || funny === "" || movie === "" || sport === "" || smile === "") {
                // Display an error message
                toastr.error('Please fill in all fields before proceeding.');
    
                // Trigger the "Show More" button to reveal hidden questions
                $('#loadmore').click();
                return false;
                
            } else {
                // Send the data to the server using AJAX
                $.ajax({
                    type: 'POST',
                    url: '/detail/', // Replace with the actual server endpoint
                    data: {
                        petname: petName,
                        angry: angry,
                        funny: funny,
                        movie: movie,
                        sport: sport,
                        smile: smile,
                        csrfmiddlewaretoken: csrf_token // Include your CSRF token
                    },
                    success: function (response) {
                        if (response.success) {
                            toastr.success("done")
                            window.location.href = '/lyrics/';
                        } else {
                            toastr.error('Something went wrong.');
                        }
                    },
                    error: function () {
                        toastr.error('Error while sending data to the server.');
                    }
                });
            }
        });
    });
    $(function () {
        $("#recreate_btn").click(function () {
            $.ajax({
                type: "POST",
                url: "/detail/",
                data: {
                    csrfmiddlewaretoken: csrf_token // Include your CSRF token
                },
                success: function () {
                    window.location.href = "/lyrics/";
                },
                error: function () {
                    alert("An error occurred while sending the request.");
                }
            });
        });
    });
    $(function () {
        $("#btn_create").click(function () {
            // Send an AJAX request to the Django view to remove profiles
            $.ajax({
                type: "POST",
                url: "/create_again/",
                data: {
                    csrfmiddlewaretoken: csrf_token // Include your CSRF token
                },  // Replace with the actual URL for your view
                success: function () {
                    // Redirect to 'frame2.html' after successfully removing profiles
                    window.location.href = "/addnew/";
                },
                error: function () {
                    alert("An error occurred while sending the request.");
                }
            });
        });
    });


    $(function () {
        $(window).on("load", function () {
            $(".scroll_content").mCustomScrollbar({
                theme: "dark",
            });
        });
    });
    $(function () {
        $(window).on("load", function () {
            $(".list_content").mCustomScrollbar({
                theme: "dark",
            });
        });
    });

    $(function () {
        $("#btn_menuhamburger").click(function () {
            $(".right_sidebar").addClass('right_sidebar_active')
            $(".overlay").addClass('overlay_active')
        });
        $("#btn_close").click(function () {
            $(".right_sidebar").removeClass('right_sidebar_active')
            $(".overlay").removeClass('overlay_active')
        });
    });
    $(function () {
        AOS.init({
            duration: 1200,
        });
    });
})