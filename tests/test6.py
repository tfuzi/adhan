
def find_next_time(time_list, current_time):
    from datetime import datetime, timedelta

    current_time_obj = current_time

    # Initialize variables to track the next time and its difference
    next_time = None
    min_difference = timedelta.max

    # Iterate over the time_list and find the next time
    for time_str in time_list:
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        # Calculate the difference between current_time_obj and time_obj
        difference = (datetime.combine(datetime.now().date(), time_obj) -
                      datetime.combine(datetime.now().date(), current_time_obj))

        # Ignore times that are equal to or before the current_time
        if difference <= timedelta(0):
            continue

        # Update next_time and min_difference if a closer time is found
        if difference < min_difference:
            next_time = time_str
            min_difference = difference

    return next_time

# Example usage
times = ["07:08 PM", "09:30 AM", "03:45 PM", "11:15 PM", "01:00 PM"]
current = datetime.now().time()
next_time = find_next_time(times, current)
print("Next time:", next_time)
