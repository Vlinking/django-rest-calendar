
function change_month(year, month, offset) {
    var new_year = year;
    var new_month = month + offset;
    if (new_month > 12) {
        new_year++;
        new_month = 1;
    } else if (new_month < 1) {
        new_year--;
        new_month = 12;
    }
    current_year = new_year;
    current_month = new_month;
}

function load_month(year, month) {
    $.get('/calendars/api/get_calendar_monthly/'+ year + '/' + month + '/' + today, {}, function(data) {
           $('#little_calendar').html(data);
       });
}

$(document).ready(function() {
   $('.larrow').click(function() {
        change_month(current_year, current_month, -1);
        load_month(current_year, current_month, today);

    });

   $('.rarrow').click(function() {
        change_month(current_year, current_month, 1);
        load_month(current_year, current_month, today);
   });
});