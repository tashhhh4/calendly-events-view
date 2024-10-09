# Calendly Booking Calendar: Events View

This single-page web app takes the Calendly meeting scheduler of a Calendly user and reverses the display so that one easily sees which times are NOT available as existing events. This makes it much easier to see at a glance when the person is busy.

Some parameters have been assumed from personal knowledge and hard-coded into the app such as the user's opening and closing hours and their lunch break. The name of the user is removed from the code so the solution itself will not display any personal data.

*Limitations* - The data comes from a shared view in which the Calendly user has already chosen to expose specific calendar data. The app cannot show dates outside of that time frame. Since this view is based on available booking times, it cannot show you any information about events the user may have planned on days when they are not available for meetings such as weekends, and days in the past.

This is also only designed to be run from a local file in the web browser. To run it you open `frontend/calendar.html`.

## Screenshot
![calendar viewer running in firefox on my computer](/calendar_screenshot_01.png "Calendly Event Viewer")

## Views
### Main view
Open `frontend/calendar.html` in a web browser.

### Testing view
After starting up the project, go to `localhost:5000/TEST/calendar` in a web browser.
This lets you view the JSON data that gets sent to `frontend/calendar.html`.

## How to run
You need docker installed.
Create a file called .env with the following values:

    NAME=[Your personal name for the person whose calendar you want to view]
    CALENDLY_LINK=https://calendly.com/{COMPANY}/15-mins-urgent?month={YYYY-MM}
    DATA_URL=[...]

## How to get the DATA_URL

Go to Calendly link: https://calendly.com/{COMPANY}/15-mins-urgent?month={YYYY-MM}

Open the Network Tab and reload the page.

Scroll down to the following entry:
    Status: 200
    Method: GET
    Domain: calendly.com
    File: range?timezone=Europe/Berlin&diagnostics=false&range_start=2024-10-...

Right Click > "Open in New Tab"

Now you should see the API url in the browser's URL bar. Paste that into the `DATA_URL` variable. You can also see a preview of the JSON data that the app will be using.

## Profile Picture

To add a personal touch to the calendar, you can add a profile picture (of the Calendly user) at /frontend/images/profile.png

## Run with Docker Compose

    docker compose up -d --build
