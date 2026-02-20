import prairielearn as pl
from theorielearn.shared_utils import (
    grade_question_tokenized,
    grade_question_parameterized,
    tokenize_string,
)

TRANSITION_NAMES = {
    "transition-0-0", "transition-0-1",
    "transition-1-0", "transition-1-1",
    "transition-2-0", "transition-2-1",
    "transition-3-0", "transition-3-1",
}


def grade_flex_transition(data: pl.QuestionData, question_name: str) -> None:
    """Grade a transition answer, accepting both with and without outer set braces."""
    correct = data["correct_answers"][question_name].strip()
    if correct.startswith("{") and correct.endswith("}"):
        correct = correct[1:-1]

    def grade_fn(student_ans: str):
        s = student_ans.strip()
        if s.startswith("{") and s.endswith("}"):
            s = s[1:-1]
        return set(tokenize_string(s)) == set(tokenize_string(correct)), None

    grade_question_parameterized(data, question_name, grade_fn)


def grade(data: pl.QuestionData) -> None:
    for question_name in data["correct_answers"].keys():
        if question_name in TRANSITION_NAMES:
            grade_flex_transition(data, question_name)
        else:
            grade_question_tokenized(data, question_name)
    pl.set_weighted_score_data(data)
