function updateSelectForm(schedule_id, user_id, start_id, end_id, max_tickets) {
    document.getElementById('schedule_id').value = schedule_id;
    document.getElementById('user_id').value = user_id;
    document.getElementById('startleg_id').value = start_id;
    document.getElementById('endleg_id').value = end_id;
    document.getElementById('ticket_number').value = 1;
    document.getElementById('ticket_number').setAttribute('max', max_tickets);
}

function updateBookingSidebar(designation, date, dep_airport, dep_time, arr_airport, arr_time, aircraft, created, status, book_id, related_id) {
    document.getElementById('book-sidebar').style.visibility = 'visible';
    document.getElementById('book-sidebar-dsg').innerText = designation;
    document.getElementById('book-sidebar-date').innerText = date;
    document.getElementById('book-sidebar-dpt-ap').innerText = dep_airport;
    document.getElementById('book-sidebar-dpt-tm').innerText = dep_time;
    document.getElementById('book-sidebar-arr-ap').innerText = arr_airport;
    document.getElementById('book-sidebar-arr-tm').innerText = arr_time;
    document.getElementById('book-sidebar-aircraft').innerText = aircraft;
    document.getElementById('book-sidebar-created').innerText = created;
    document.getElementById('book-sidebar-status').innerText = status;
    document.getElementById('conf-link').setAttribute('href', '/dashboard/booking/confirm/' + book_id)
    document.getElementById('booking_id').value = book_id;
    document.getElementById('related_id').value = related_id;
}