from datetime import timedelta
# Function to convert seconds to HH:MM:SS format
def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    # Include milliseconds
    return f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

def calculate_inner_thumbnail_positions(duration, num_positions):
    dutation = round(duration)
    positions = []
    for i in range(num_positions + 1):
        position = (i * duration) / (num_positions + 1)
        positions.append(round(position))
    return positions[1:]

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

# TODO: This is just a copy of subtract seconds and the sign changed for "Subtract the specific number of seconds"
def add_seconds(timestamp: str, seconds_to_subtract: int) -> str:
    # Convert the timestamp to timedelta
    time_obj = timedelta(hours=int(timestamp[:2]), minutes=int(timestamp[3:5]), seconds=int(timestamp[6:8]), milliseconds=int(timestamp[9:12]))

    # Subtract the specified number of seconds
    new_time_obj = time_obj + timedelta(seconds=seconds_to_subtract)

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


def add_timestamps(timestamp1: str, timestamp2: str) -> str:
    # Convert both timestamps to timedelta objects
    time_obj1 = timedelta(hours=int(timestamp1[:2]), minutes=int(timestamp1[3:5]), seconds=int(timestamp1[6:8]), milliseconds=int(timestamp1[9:12]))
    time_obj2 = timedelta(hours=int(timestamp2[:2]), minutes=int(timestamp2[3:5]), seconds=int(timestamp2[6:8]), milliseconds=int(timestamp2[9:12]))

    # Add the two timedelta objects
    total_time = time_obj1 + time_obj2

    # Convert the total timedelta back to HH:MM:SS.mmm format
    total_seconds = int(total_time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = total_time.microseconds // 1000

    # Format the new timestamp as HH:MM:SS.mmm
    new_timestamp = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    return new_timestamp
