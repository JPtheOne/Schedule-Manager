from datetime import datetime, timedelta

def calculate_end_time(start_time, duration):
    start_time_dt = datetime.strptime(start_time, "%H:%M")
    duration_parts = duration.split(':')
    hours, minutes = int(duration_parts[0]), int(duration_parts[1])
    end_time_dt = start_time_dt + timedelta(hours=hours, minutes=minutes)
    end_time = end_time_dt.strftime("%H:%M")
    return end_time

start_date = "10:00"
duration = "1:15"
end_hour = calculate_end_time(start_date, duration)
print(end_hour)  # Output: 11:15
