from datetime import timedelta
# Function to convert seconds to HH:MM:SS format
def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    # Include milliseconds
    return f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

def subtract_seconds(timestamp: str, seconds_to_subtract: int) -> str:
    # Convert the timestamp to timedelta
    time_obj = timedelta(hours=int(timestamp[:2]), minutes=int(timestamp[3:5]), seconds=int(timestamp[6:8]), milliseconds=int(timestamp[9:12]))

    # Subtract the specified number of seconds
    new_time_obj = time_obj - timedelta(seconds=seconds_to_subtract)

    # Convert the timedelta object back to HH:MM:SS.mmm format
    total_seconds = int(new_time_obj.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = new_time_obj.microseconds // 1000

    # Format the new timestamp as HH:MM:SS.mmm
    new_timestamp = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

    # This is needed because subtracting too close to start goes negative
    if new_timestamp.startswith("-"):
        new_timestamp = "00:00:00.000"
    return new_timestamp
