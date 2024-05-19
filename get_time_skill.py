import datetime

class GetTimeSkill: 
    def process(self, input_text):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The current time is {current_time}."

    def trigger(self, input_text):
        trigger_phrases = ["what time is it", "what's the time", "tell me the time", "time"] # No need for "assistant" here
        print(f"Checking triggers in GetTimeSkill for: {input_text}")  #
        return any(phrase in input_text.lower() for phrase in trigger_phrases)
