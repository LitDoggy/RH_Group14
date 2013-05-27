
function load_datepicker()
{
    var now = new Date();
    now = new Date(now.getFullYear(), now.getMonth(), now.getDate(),
		   0, 0, 0, 0);
    var checkin = $('#start').datepicker({
	onRender: function(date) {
	    return date.valueOf() < now.valueOf() ? 'disabled' : '';
	}
    }).on('changeDate', function(ev) {
	if (ev.date.valueOf() > checkout.date.valueOf()) {
	    var newDate = new Date(ev.date)
	    newDate.setDate(newDate.getDate() + 1);
	    checkout.setValue(newDate);
	}
	checkin.hide();
	$('#end')[0].focus();
    }).data('datepicker');

    var checkout = $('#end').datepicker({
	onRender: function(date) {
	    return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
	}
    }).on('changeDate', function (ev) {
	checkout.hide();
    }).data('datepicker');
}

function show_rooms()
{
    var count = $('#rooms').val();
    $('.mytr').remove();
    $('.btn').parent().parent().remove();
    for (var i = 1; i <= count; i++) {
	var str = '<tr class="mytr"><td>Room ' + i +
	    ':</td><td>Adults: <select>';
	for (var j = 1; j <= 5; j++) {
	    str += '<option name="room' + i + '_adults">'
		+ j + '</option>';
	}
	str += '</select></td><td>Children: <select>';
	for (var j = 1; j <= 5; j++) {
	    str += '<option name="room' + i + '_children">'
		+ j + '</option>';
	}
	str += '</select></td></tr>';
	$('#roomtb').append(str);
    }
    var str = '<tr><td></td><td></td><td><input type="submit" class="btn btn-large btn-primary" value="Continue" /></td></tr>';
    $('#roomtb').append(str);
}
