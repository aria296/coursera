from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Question, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


def mock_exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(lesson__course=course).prefetch_related("choices")
    return render(request, "onlinecourse/mock_exam.html", {"course": course, "questions": questions})


@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = list(Question.objects.filter(lesson__course=course).prefetch_related("choices"))
    score = 0
    results = []
    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        selected_choice = next((c for c in question.choices.all() if str(c.id) == selected_id), None)
        correct_choice = next((c for c in question.choices.all() if c.is_correct), None)
        is_correct = bool(selected_choice and selected_choice.is_correct)
        if is_correct:
            score += 1
        results.append({
            "question": question,
            "selected_choice": selected_choice,
            "correct_choice": correct_choice,
            "is_correct": is_correct,
        })
    submission = Submission.objects.create(
        course=course,
        student_name=request.POST.get("student_name", "Student")[:100] or "Student",
        score=score,
        total_questions=len(questions),
    )
    request.session[f"results_{submission.id}"] = [
        {
            "question_id": r["question"].id,
            "selected_choice_id": r["selected_choice"].id if r["selected_choice"] else None,
            "correct_choice_id": r["correct_choice"].id if r["correct_choice"] else None,
            "is_correct": r["is_correct"],
        } for r in results
    ]
    return redirect("onlinecourse:show_exam_result", submission_id=submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    saved_results = request.session.get(f"results_{submission.id}", [])
    question_ids = [item["question_id"] for item in saved_results]
    questions = Question.objects.filter(id__in=question_ids).prefetch_related("choices")
    question_map = {q.id: q for q in questions}
    results = []
    for item in saved_results:
        question = question_map.get(item["question_id"])
        if not question:
            continue
        choices = {c.id: c for c in question.choices.all()}
        results.append({
            "question": question,
            "selected_choice": choices.get(item["selected_choice_id"]),
            "correct_choice": choices.get(item["correct_choice_id"]),
            "is_correct": item["is_correct"],
        })
    return render(request, "onlinecourse/exam_result.html", {"submission": submission, "results": results})
