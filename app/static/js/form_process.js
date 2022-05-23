function updateSelectForm(schedule_id, user_id, start_id, end_id, max_tickets) {
    document.getElementById('schedule_id').value = schedule_id;
    document.getElementById('user_id').value = user_id;
    document.getElementById('startleg_id').value = start_id;
    document.getElementById('endleg_id').value = end_id;
    document.getElementById('ticket_number').setAttribute('max', max_tickets);
}