def attempt_insights(attempt):
    category_totals = {}
    times = []
    for answer in attempt.answers:
        cat = answer.question.category
        item = category_totals.setdefault(cat, {"scored": 0.0, "max": 0.0, "count": 0})
        item["scored"] += float(answer.marks_awarded or 0.0)
        item["max"] += float(answer.question.marks)
        item["count"] += 1
        times.append((answer.question.external_id, answer.time_spent_seconds, answer.status, answer.marks_awarded or 0.0))

    category_percent = {
        cat: round((v["scored"] / v["max"] * 100), 2) if v["max"] else 0.0
        for cat, v in category_totals.items()
    }

    strongest = max(category_percent.items(), key=lambda i: i[1], default=("N/A", 0))
    weakest = min(category_percent.items(), key=lambda i: i[1], default=("N/A", 0))

    avg_time = round(sum(t[1] for t in times) / len(times), 2) if times else 0
    fastest = min(times, key=lambda t: t[1], default=(None, 0, None, 0))
    slowest = max(times, key=lambda t: t[1], default=(None, 0, None, 0))

    return {
        "category_percent": category_percent,
        "time_points": times,
        "strongest": strongest,
        "weakest": weakest,
        "avg_time": avg_time,
        "fastest": fastest,
        "slowest": slowest,
    }
