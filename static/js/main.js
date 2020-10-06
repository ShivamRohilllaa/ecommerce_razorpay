function send_message(){
	var name=jQuery("#name").val();
	var email=jQuery("#email").val();
	var mobile=jQuery("#mobile").val();
	var comment=jQuery("#comment").val();
	
	if(name==""){
		alert('Please enter name');
	}else if(email==""){
		alert('Please enter email');
	}else if(mobile==""){
		alert('Please enter mobile');
	}else if(comment==""){
		alert('Please enter comment');
	}else{
		jQuery.ajax({
			url:'send_message.php',
			type:'post',
			data:'name='+name+'&email='+email+'&mobile='+mobile+'&comment='+comment,
			success:function(result){
				alert(result);
			}	
		});
	}
}

function user_register(){
	jQuery('.field_error').html('');
	var name=jQuery("#name").val();
	var email=jQuery("#email").val();
	var mobile=jQuery("#mobile").val();
	var password=jQuery("#password").val();
	var is_error='';
	if(name==""){
		jQuery('#name_error').html('Please enter name');
		is_error='yes';
	}if(email==""){
		jQuery('#email_error').html('Please enter email');
		is_error='yes';
	}if(mobile==""){
		jQuery('#mobile_error').html('Please enter mobile');
		is_error='yes';
	}if(password==""){
		jQuery('#password_error').html('Please enter password');
		is_error='yes';
	}
	if(is_error==''){
		jQuery.ajax({
			url:'register_submit.php',
			type:'post',
			data:'name='+name+'&email='+email+'&mobile='+mobile+'&password='+password,
			success:function(result){
				if(result=='email_present'){
					jQuery('#email_error').html('Email id already present');
//					alert(result);
				}
				if(result=='insert'){
					jQuery('.register_msg p').html('Thank you for registeration');
				}
			}
//			 setInterval('location.reload()', 5000);        // Using .reload() method.
		});
	}	
}


function user_login(){
	jQuery('.field_error').html('');
	var email=jQuery("#login_email").val();
	var password=jQuery("#login_password").val();
	var is_error='';
	if(email==""){
		jQuery('#login_email_error').html('Please enter email');
		is_error='yes';
	}if(password==""){
		jQuery('#login_password_error').html('Please enter password');
		is_error='yes';
	}
	if(is_error==''){
		jQuery.ajax({
			url:'login_submit.php',
			type:'post',
			data:'email='+email+'&password='+password,
			success:function(result){
				if(result=='wrong'){
					jQuery('.login_msg p').html('Please enter valid login details');
				}
				if(result=='valid'){
					window.location.href='index.php';
				}
			}	
		});
	}	
}


function manage_cart(pid,type){
	if(type=='update'){
		var qty=jQuery("#"+pid+"qty").val();
	}else{
		var qty=jQuery("#qty").val();
	}
	jQuery.ajax({
		url:'manage_cart.php',
		type:'post',
		data:'pid='+pid+'&qty='+qty+'&type='+type,
		success:function(result){
			if(type=='update' || type=='remove'){
				window.location.href=window.location.href;
			}
			jQuery('.number-cart').html(result);
		}	
	});	
}


$(document).ready(function() {
   var delay = 2000;
   $('.register-btn').click(function(e){
   e.preventDefault();
   var name = $('#name').val();
   if(name == ''){
   $('#name_error').html(
   '<span style="color:red;">Enter Your Name!</span>'
   );
   $('#name').focus();
   return false;
   }
   var mobile = $('#mobile').val();
   if(mobile == ''){
   $('#mobile_error').html(
   '<span style="color:red;">Enter Your Phone Number!</span>'
   );
   $('#mobile').focus();
   return false;
   }
 
   var email = $('#email').val();
   if(email == ''){
   $('#email_error').html(
   '<span style="color:red;">Enter Email Address!</span>'
   );
   $('#email').focus();
   return false;
   } 
   var password = $('#password').val();
   if(password == ''){
   $('#password_error').html(
   '<span style="color:red;">Enter Email Address!</span>'
   );
   $('#password').focus();
   return false;
   }
   $.ajax
   ({
   type: "POST",
   url: "register_submit.php",
   data:'name='+name+'&email='+email+'&mobile='+mobile+'&password='+password,
   success: function(data)
   {
   setTimeout(function() {
   $('.register_msg p').html(data);	   
   }, delay);
  var timeout = setTimeout("location.reload(true);",3000);
  function resetTimeout() {
    clearTimeout(timeout);
    timeout = setTimeout("location.reload(true);",3000);
  }
   }
   });
   });
 
});

$(document).ready(function() {
   var delay = 2000;
   $('.login-btn').click(function(e){
   e.preventDefault();
   var email = $('#login_email').val();
   if(login_email == ''){
   $('#login_email_error').html(
   '<span style="color:red;">Enter Your Name!</span>'
   );
   $('#login_email').focus();
   return false;
   }
   var password = $('#login_password').val();
   if(login_password == ''){
   $('#login_password_error').html(
   '<span style="color:red;">Enter Your Phone Number!</span>'
   );
   $('#login_password').focus();
   return false;
   }
   $.ajax
   ({
   type: "POST",
   url: "login_submit.php",
   data:'email='+email+'&password='+password,
   success: function(data)
   {
   setTimeout(function() {
   $('.login_msg p').html(data);	   
   }, delay);
  var timeout = setTimeout("location.reload(true);",3000);
  function resetTimeout() {
    clearTimeout(timeout);
    timeout = setTimeout("location.reload(true);",3000);
  }
   }
   });
   });
 
});

/*--------------*/


jQuery(document).ready(function($) {
	var galleryItems = $('.cd-gallery').children('li');

	galleryItems.each(function(){
		var container = $(this);

		// preview image hover effect - desktop only
		container.on('mouseover', '.move-right, .move-left', function(event){
			hoverItem($(this), true);
		});
		container.on('mouseleave', '.move-right, .move-left', function(event){
			hoverItem($(this), false);
		});

		// update slider when user clicks on the preview images
		container.on('click', '.move-right, .move-left', function(event){
			event.preventDefault();
			if ( $(this).hasClass('move-right') ) {
				var selectedPosition = container.find('.cd-item-wrapper .selected').index() + 1;
				nextSlide(container);
			} else {
				var selectedPosition = container.find('.cd-item-wrapper .selected').index() - 1;
				prevSlide(container);
			}
		});
	});


	function hoverItem(item, bool) {
		( item.hasClass('move-right') )
			? item.toggleClass('hover', bool).siblings('.selected, .move-left').toggleClass('focus-on-right', bool)
			: item.toggleClass('hover', bool).siblings('.selected, .move-right').toggleClass('focus-on-left', bool);
	}

	function nextSlide(container, dots, n){
		var visibleSlide = container.find('.cd-item-wrapper .selected');
		if(typeof n === 'undefined') n = visibleSlide.index() + 1;
		visibleSlide.removeClass('selected');
		container.find('.cd-item-wrapper li').eq(n).addClass('selected').removeClass('move-right hover').prevAll().removeClass('move-right move-left focus-on-right').addClass('hide-left').end().prev().removeClass('hide-left').addClass('move-left').end().next().addClass('move-right');
	}

	function prevSlide(container, dots, n){
		var visibleSlide = container.find('.cd-item-wrapper .selected');
		if(typeof n === 'undefined') n = visibleSlide.index() - 1;
		visibleSlide.removeClass('selected focus-on-left');
		container.find('.cd-item-wrapper li').eq(n).addClass('selected').removeClass('move-left hide-left hover').nextAll().removeClass('hide-left move-right move-left focus-on-left').end().next().addClass('move-right').end().prev().removeClass('hide-left').addClass('move-left');
	}

});

    function emeAccordion(){
        $('.accordion__title')
          .siblings('.accordion__title').removeClass('active')
          .first().addClass('active');
        $('.accordion__body')
          .siblings('.accordion__body').slideUp()
          .first().slideDown();
        $('.accordion').on('click', '.accordion__title', function(){
          $(this).addClass('active').siblings('.accordion__title').removeClass('active');
          $(this).next('.accordion__body').slideDown().siblings('.accordion__body').slideUp();
        });
        };
    emeAccordion();
