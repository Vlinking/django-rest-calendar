
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

function load_month_detailed(year, month) {
    $.get('/calendars/api/get_calendar_monthly_detailed/'+ year + '/' + month + '/' + today, {}, function(data) {
           $('#large_calendar').html(data);
       });
}

function load_day_detailed(year, month) {
    $.get('/calendars/api/get_day_detailed/'+ year + '/' + month + '/' + today, {}, function(data) {
           $('#day_detailed').html(data);
       });
}

function select_view_mode(mode) {
    $('.upper .view').each(function() {
        $(this).removeClass('selected');
    })
    mode.addClass('selected');
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

   $('#daily_view').click(function() {
        select_view_mode($(this));
   });

   $('#weekly_view').click(function() {
        select_view_mode($(this));
   });

   $('#monthly_view').click(function() {
        select_view_mode($(this));
        load_month_detailed(current_year, current_month, 0);
   });

   // load initial month
   load_month(current_year, current_month, today);
});