def find_previous_time(time_list, current_time):
    from datetime import datetime, timedelta
    # Convert current_datetime to a time object
    current_time_obj = current_time

    # Initialize variables to track the previous time and its difference
    previous_time = None
    min_difference = timedelta.max

    # Iterate over the time_list and find the previous time
    for time_str in time_list:
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        # Calculate the difference between current_time_obj and time_obj
        difference = (datetime.combine(datetime.now().date(), current_time_obj) -
                      datetime.combine(datetime.now().date(), time_obj))

        # Ignore times that are equal to or after the current_time
        if difference <= timedelta(0):
            continue

        # Update previous_time and min_difference if a closer time is found
        if difference < min_difference:
            previous_time = time_str
            min_difference = difference

    return previous_time

from datetime import datetime

# Example usage
times = ["07:08 PM", "09:30 AM", "03:45 PM", "11:15 PM", "01:00 PM"]
current = datetime.now().time()
previous_time = find_previous_time(times, current)
print("Previous time:", previous_time)
