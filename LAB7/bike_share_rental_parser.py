def parse_ride_duration(text):
    """
    Converts a ride duration written as HH:MM into minutes.
    Handles invalid inputs gracefully by returning None.
    """
    if text is None:
        return None
    text = text.strip()
    if not text:
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
        if hours < 0 or minutes < 0 or minutes >= 60:
            return None
        return hours * 60 + minutes
    except ValueError:
        return None


def format_station_code(code):
    """
    Formats a station code as ZONE-NUMBER, e.g. 'a12' -> 'A-12'.
    Handles invalid inputs gracefully by returning None.
    """
    if code is None:
        return None
    code = code.strip().upper()
    if not code or len(code) < 2:
        return None
    if not code[0].isalpha():
        return None
    if not code[1:].isdigit():
        return None
    return code[0] + '-' + code[1:]


def parse_ride_log(line):
    """
    Parses 'bike_type,minutes,subscriber' into a tuple.
    Handles invalid inputs gracefully by returning None.
    """
    if line is None:
        return None
    line = line.strip()
    if not line:
        return None
    parts = line.split(',')
    if len(parts) != 3:
        return None
    try:
        bike_type = parts[0].strip()
        minutes = int(parts[1].strip())
        subscriber = parts[2].strip().lower() == 'yes'
        if minutes < 0:
            return None
        return bike_type, minutes, subscriber
    except ValueError:
        return None


def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    result = parse_ride_duration(value)
    if result is None:
        print("Invalid input format")
    else:
        print("Duration in minutes:", result)

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    result = format_station_code(value)
    if result is None:
        print("Invalid station code")
    else:
        print("Formatted station code:", result)

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    result = parse_ride_log(value)
    if result is None:
        print("Invalid ride log format")
    else:
        print("Parsed ride log:", result)


if __name__ == "__main__":
    main()