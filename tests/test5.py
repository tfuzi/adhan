def find_closest_time(time_list):
    from datetime import datetime, timedelta

    current_time = datetime.now().time()

    # Convert current_time to a datetime object with today's date
    current_datetime = datetime.combine(datetime.now().date(), current_time)

    # Initialize variables to track the closest time and its difference
    closest_time = None
    min_difference = timedelta.max

    # Iterate over the time_list and find the closest time
    for time_str in time_list:
        # Parse the time string to a datetime object
        time_obj = datetime.strptime(time_str, "%I:%M %p").time()

        # Convert the time_obj to a datetime object with today's date
        time_datetime = datetime.combine(datetime.now().date(), time_obj)

        # Calculate the difference between current_datetime and time_datetime
        difference = abs(current_datetime - time_datetime)

        # Update closest_time and min_difference if a closer time is found
        if difference < min_difference:
            closest_time = time_str
            min_difference = difference

    return closest_time

