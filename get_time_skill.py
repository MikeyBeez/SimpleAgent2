import datetime

class GetTimeSkill: 
    def process(self, input_text):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        return f"The current time is {current_time}."

    def trigger(self, input_text):
        trigger_phrases = ["what time is it", "what's the time", "tell me the time", "time"]
        print(f"Checking triggers in GetTimeSkill for: {input_text}") 
        # Check if any trigger phrase is at the beginning of the input
        return any(input_text.lower().startswith(phrase) for phrase in trigger_phrases) 
