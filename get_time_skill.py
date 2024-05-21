import datetime

class GetTimeSkill:
    def __init__(self):
        pass  # Remove print_current_time() from __init__

    def process(self, input_text):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The current time is {current_time}."

    # Remove the trigger() method

    def print_current_time(self): # You can keep this for debugging
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        print(f"The current time is: {current_time}")

# Make similar changes to GetWeatherSkill
