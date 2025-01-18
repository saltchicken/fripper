# Function to convert seconds to HH:MM:SS format
def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    # Include milliseconds
    return f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

