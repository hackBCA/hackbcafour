$(document).ready(function () {
	align();
});

function align() {

	$('#line_top').css({
		'margin-top': nudge($('#line_top').height() / 2, '-')
	});
	$('#line_bottom').css({
		'margin-bottom': nudge($('#line_bottom').height() / 2, '-')
	});

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