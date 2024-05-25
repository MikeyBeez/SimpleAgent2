import logging
from get_time_skill import GetTimeSkill
from get_weather_skill import GetWeatherSkill

# Configure logging
logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def handle_skills(question, available_skills): # Removed chat_history
    logging.info(f"Skill Handler - Question received in handle_skills(): {question}")

    parts = question.lower().split("assistant")  

    if len(parts) > 1:
        skill_trigger = parts[1].strip()
        logging.info(f"Skill Handler - Skill trigger: {skill_trigger}") 

        for skill in available_skills:
            logging.info(f"Skill Handler - Checking skill: {skill.__class__.__name__}")
            if skill.trigger(skill_trigger):
                logging.info(f"Skill Handler - Skill triggered: {skill.__class__.__name__}")
                response = skill.process(question) # Only pass question
                logging.info(f"Skill Handler - Response from skill: {response}")
                return response

    logging.info("Skill Handler - No skill matched the command.")
    return False
