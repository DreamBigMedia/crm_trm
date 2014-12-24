	$().ready(function() {

		$("#orderform").validate({  
		focusCleanup: true,
        errorClass: "my-error-class",
        validClass: "my-valid-class",
			rules: {
                    fname: "required",
                    lname: "required",
                    ship_address1: "required",
                    ship_city: "required",
                    ship_state:"required",
                    ship_zipcode:
                        {
                            required: true,
                            minlength: 5,
                            maxlength: 5,
                            digits: true,
                     
                        },
                    ship_phone:
                        {
                        required: true,
                        phoneUS: true,
                    
                        },
                    email:
                        {
                           email: true,
                            required: true,
                        
                        }
            },
			messages: {
				fname: "Please enter your firstname",
				lname: "Please enter your lastname",
				ship_address1: {
					required: "Please enter a valid address",
				},
				ship_city: {
					required: "Please enter a valid city",
				},
				ship_state: {
						required: "Please choose a state"
				},
                ship_zipcode:{
                       required: "Please enter a valid zip code"
                },
                ship_phone:{
                     required: "Please enter a valid phone"
                    
                },
                email:{
                    required: "Please enter a valid email address",
                }
              }
           });
        });
