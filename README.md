# Online Course Django Final Project

This is a starter implementation for the Coursera-style "Add a New Assessment Feature" project.

## 1. Install and run

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and the admin site at http://127.0.0.1:8000/admin/.

## 2. Create demo data

After creating a superuser, run:

```bash
python manage.py shell
```

Then paste:

```python
from onlinecourse.models import Course, Lesson, Question, Choice
course = Course.objects.create(name="Introduction to Django", description="Learn the basics of Django.")
lesson1 = Lesson.objects.create(course=course, title="Django Models", content="Models define the data structure.")
lesson2 = Lesson.objects.create(course=course, title="Views and Templates", content="Views connect data to templates.")
q = Question.objects.create(lesson=lesson1, text="Which file defines Django models?")
Choice.objects.create(question=q, text="models.py", is_correct=True)
Choice.objects.create(question=q, text="urls.py", is_correct=False)
q2 = Question.objects.create(lesson=lesson2, text="Which function handles a web request?")
Choice.objects.create(question=q2, text="A view", is_correct=True)
Choice.objects.create(question=q2, text="A migration", is_correct=False)
exit()
```

## 3. URLs and screenshots

- Course list: `/`
- Course details: `/course/<course_id>/`
- Mock exam: `/course/<course_id>/exam/`
- Admin: `/admin/`

To create the requested screenshots, run the app locally and capture:
- `03-admin-site.png`: admin index showing Authentication and Authorization and OnlineCourse.
- `07-final.png`: complete the mock exam with correct answers and capture the Congratulations message, score, and results.

Do not upload a screenshot unless it shows your actual running app. Before submitting, push the project to a public GitHub repository you own and submit the actual file URLs from that repository.
