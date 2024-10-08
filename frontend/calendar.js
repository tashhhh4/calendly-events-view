// Calendar

APP_URL = 'http://localhost:5000'

function renderMustacheTemplate(templateId, data, targetId) {
    const template = document.getElementById(templateId).innerHTML;
    const rendered = Mustache.render(template, data);
    document.getElementById(targetId).innerHTML = rendered;
}

function fillCalendar(dataObj) {

    // Title
    titleData = {
        company: dataObj['company']
    };

    // Header
    console.log(dataObj);
    headerData = {
        month_name: dataObj['month'],
        year: dataObj['year'],
        name: dataObj['name']
    };

    // Rest of the Calendar
    BG_HOURS = Array();
    for (i=8; i<=22; i++) {
        BG_HOURS.push({'hour': i});
    }

    calendarData = {
        days: dataObj['days'],
        BG_HOURS: BG_HOURS,
        name: dataObj['name']
    };

    renderMustacheTemplate('title_template', titleData, 'title_target');
    renderMustacheTemplate('header_template', headerData, 'header_target');
    renderMustacheTemplate('calendar_template', calendarData, 'calendar_target');
}

function getCalendarData() {
    fetch(APP_URL + '/calendar')
    .then(response => response.json())
    .then(data => fillCalendar(data))
    .catch(error => console.error('Error fetching data:', error));
}