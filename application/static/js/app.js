$(document).ready(function () {

	var $confirmation = $('#confirmation');
	var $submit = $('input[type="submit"]');
	var $email = $('input[type="submit"]');

	align();

	//$confirmation.css("transform", "translateY(" + toPx($confirmation.outerHeight() * -1) + ")");

	// Validate first

	/* $submit.click(function () {
			var emailValue = $email.value();
			$confirmation.velocity({
				translateY: "0px"
			}, {
				easing: [20, 10]
			});
		}); */

});

function align() {

	$('#line__top').css({
		'margin-top': nudge($('#line__top').height() / 2, '-')
	});
	$('#line__bottom').css({
		'margin-bottom': nudge($('#line__bottom').height() / 2, '-')
	});

}

function validateEmail(email) {
	var reg = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
	return reg.test(email);
}

function toPx(value) {
	return value + 'px';
}

function nudge(e, s) {
	switch (s) {
	case '-':
		return (e * -1).toString() + 'px';
		break;
	case '+':
		return e.toString() + 'px';
		break;
	default:
		return e.toString() + 'px';
		break;

	}

}