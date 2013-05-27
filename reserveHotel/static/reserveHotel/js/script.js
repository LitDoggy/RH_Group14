
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
