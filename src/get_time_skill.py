import datetime

class GetTimeSkill:
    def __init__(self):
        pass

    def process(self, input_text):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The current time is {current_time}."

    def trigger(self, command):
        time_keywords = ["time", "current time", "what time", "what's the time"]
        return any(keyword in command.lower() for keyword in time_keywords)
