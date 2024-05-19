from get_time_skill import GetTimeSkill

def handle_skills(question, chat_history, available_skills):
    print(f"Question received in handle_skills(): {question}")  #
    for skill in available_skills:
        if skill.trigger(question):
            response = skill.process(question)
            return response  # Return the response from the executed skill
    return False  # No skill was triggered
