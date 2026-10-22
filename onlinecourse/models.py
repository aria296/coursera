from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions")
    student_name = models.CharField(max_length=100, default="Student")
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        if not self.total_questions:
            return 0
        return round(self.score / self.total_questions * 100)

    @property
    def passed(self):
        return self.percentage >= 70

    def __str__(self):
        return f"{self.student_name} - {self.score}/{self.total_questions}"
