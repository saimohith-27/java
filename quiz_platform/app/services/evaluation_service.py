from collections import defaultdict


def evaluate_question(question, answer):
    selected = answer.selected_answer_json if answer else None
    if selected in (None, "", []):
        return "UNANSWERED", 0.0

    marks = float(question.marks)
    negative = float(question.negative_marks)

    if question.qtype == "single_choice":
        correct = selected == question.correct_answer_json
        return ("CORRECT", marks) if correct else ("INCORRECT", -negative)

    if question.qtype == "true_false":
        truth_value = selected is True if isinstance(selected, bool) else str(selected).lower() == "true"
        correct = truth_value == bool(question.correct_answer_json)
        return ("CORRECT", marks) if correct else ("INCORRECT", -negative)

    if question.qtype == "multiple_choice":
        selected_set = set(selected if isinstance(selected, list) else [selected])
        correct_set = set(question.correct_answer_json or [])
        incorrect_selected = selected_set - set(question.options_json or []) | (selected_set - correct_set)
        correct_selected = selected_set & correct_set
        if not selected_set:
            return "UNANSWERED", 0.0
        if selected_set == correct_set:
            return "CORRECT", marks
        if incorrect_selected:
            penalty = negative * len(incorrect_selected)
            partial = (len(correct_selected) / max(1, len(correct_set))) * marks - penalty
            return "INCORRECT" if partial <= 0 else "PARTIALLY_CORRECT", max(0.0, partial)
        partial = (len(correct_selected) / max(1, len(correct_set))) * marks
        return "PARTIALLY_CORRECT", max(0.0, partial)

    return "UNANSWERED", 0.0


def evaluate_attempt(attempt):
    totals = defaultdict(float)
    status_counts = defaultdict(int)
    for answer in attempt.answers:
        question = answer.question
        status, score = evaluate_question(question, answer)
        answer.status = status
        answer.marks_awarded = score
        totals["score"] += score
        totals["max_score"] += float(question.marks)
        status_counts[status] += 1

    unanswered = len(attempt.answers) - sum(status_counts.values())
    if unanswered > 0:
        status_counts["UNANSWERED"] += unanswered

    percentage = (totals["score"] / totals["max_score"] * 100) if totals["max_score"] > 0 else 0

    return {
        "score": round(totals["score"], 2),
        "max_score": round(totals["max_score"], 2),
        "percentage": round(percentage, 2),
        "status_counts": dict(status_counts),
    }
