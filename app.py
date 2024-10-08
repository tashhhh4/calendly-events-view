from flask import Flask, jsonify
from flask_cors import CORS
import os, re, json
import calendar, datetime
import urllib.request

# Global
CALENDLY_LINK = os.environ.get('CALENDLY_LINK')
DATA_URL = os.environ.get('DATA_URL')
NAME = os.environ.get('NAME')

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/calendar')
def calendar_data():

    # Get data from URL
    url = DATA_URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept': 'application/json'
    }
    payload = {}

    request = urllib.request.Request(url, headers=headers)

    response = None
    try:
        response = urllib.request.urlopen(request)
        response_data = response.read()
        response_text = response_data.decode()
        data_obj = json.loads(response_text)

    finally:
        if response:
            response.close()

    def process_data(data_obj):
        
        output = {}

        # Name (from personal knowledge)
        output['name'] = NAME

        # Company name from Calendly
        pattern = r"https:\/\/calendly\.com\/([^\/]+)\/*"
        matches = re.search(pattern, CALENDLY_LINK)
        if matches:
            output['company'] = matches.group(1)
        else:
            output['company'] = None

        # Month
        month_number = int(data_obj['today'][5:7])
        month_name = calendar.month_name[month_number]
        output['month'] = month_name

        # Year
        year = int(data_obj['today'][:4])
        output['year'] = year

        # Total Days
        total_days = calendar.monthrange(year, month_number)[1]

        # Original Data
        original_days = {entry['date']: entry['spots'] for entry in data_obj['days']}

        # Processed Data
        processed_days = []
        for day in range(1, total_days + 1):

            # Utils
            date_obj = datetime.datetime(year, month_number, day)
        
            # Date Full
            date_full = f"{year}-{month_number:02d}-{day:02d}"

            # Weekday
            weekday = date_obj.strftime('%A')

            processed_days.append({
                "date_full": date_full,
                "date": day,
                "weekday": weekday,
                "is_bookable": False,
                "is_weekend": False,
                "is_past": False,
                "events": []
            })

        for day in processed_days:            

            # Utils
            date_obj = datetime.datetime(year, month_number, day['date'])
        
            # Past
            today = datetime.datetime.now()
            if date_obj < today:
                day['is_past'] = True

            # Weekend
            if day['weekday'] in ["Saturday", "Sunday"]:
                day['is_weekend'] = True

            # Bookable
            if day['date_full'] in original_days:
                day['is_bookable'] = True

                # Events!
                def spots_to_events(spots):

                    # 1. Create a dictionary of all bookable times
                    booked_times = {
                        f"{hour:02d}:{minute:02d}": False
                        for hour in range(8, 22)
                        for minute in (0,30)
                        if not (hour == 12) and not (hour == 13)
                    }

                    # 2. Create a dictionary of the real available times
                    available_times = {
                        datetime.datetime.fromisoformat(spot['start_time'][:-6]).strftime("%H:%M"): True
                        for spot in spots if spot['status'] == 'available'
                    }

                    # 3. Set items in booked_times to True if that time DOESN'T appear in available_times
                    for bookable_time in booked_times.keys():
                        if bookable_time not in available_times:
                            booked_times[bookable_time] = True

                    # 4. Convert booked times into event intervals
                    events = []
                    for time, is_booked in booked_times.items():
                        if is_booked:
                            start_time = datetime.datetime.strptime(time, "%H:%M")
                            end_time = start_time + datetime.timedelta(minutes=30)
                            
                            base_time = datetime.datetime.strptime("08:00", "%H:%M")
                            start_offset = (start_time - base_time).total_seconds() / 3600

                            events.append({
                                'start_time': start_time.strftime("%-H:%M"),
                                'start_offset': start_offset,               
                                'end_time': end_time.strftime("%-H:%M"),
                                'length': 30
                            })

                    # 5. Merge consectutive events
                    if events:
                        merged_events = []
                        current_event = events[0]

                        for next_event in events[1:]:
                            if current_event['end_time'] == next_event['start_time']:
                                current_event['end_time'] = next_event['end_time']
                                current_event['length'] += 30
                            else:
                                merged_events.append(current_event)
                                current_event = next_event
                        merged_events.append(current_event)

                        events = merged_events

                    return events

                # Skip Past days
                if not day['is_past']:
                    spots = original_days[day['date_full']]
                    events = spots_to_events(spots)
                    day['events'] = events

        output['days'] = processed_days

        return output

    processed_data = process_data(data_obj)

    return jsonify(processed_data)
    
@app.route('/TEST/calendar')
def TEST_calendar_data():
    response = calendar_data()
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)