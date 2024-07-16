from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question to django session.
    """
    answer_list = session.get("answer_list")
    if current_question_id is not None:
        answer_list.append({"id": current_question_id-1, "answer_text": str(answer)})
        session["answer_list"] = answer_list
        print(answer_list)
        print("session : ",session["answer_list"])
    return True, ""


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.   
    """
    if current_question_id is None:
        current_question_id = 1

    index = current_question_id - 1
    if 0 <= index < len(PYTHON_QUESTION_LIST):
        question = PYTHON_QUESTION_LIST[index]['question_text']
        options = PYTHON_QUESTION_LIST[index]['options']
        return f"{current_question_id}) Question : {question}, Options: {options}", current_question_id+1
    else:
        # return "Index out of range"
        return None, -1
    # return "dummy question", -1


def generate_final_response(session):
    """
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    """
    answer_list = session.get('answer_list')
    zipped_items = zip(PYTHON_QUESTION_LIST, answer_list)
    score = 0
    for item in zipped_items:
        if item[0]['answer'] == item[1]['answer_text']:
            score += 1

    session['score'] = score
    return f"Your Score is {score} out of {len(PYTHON_QUESTION_LIST)}"
