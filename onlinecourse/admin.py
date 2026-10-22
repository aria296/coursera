from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from .models import Course, Lesson, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "lesson")
    search_fields = ("text",)
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [QuestionInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [LessonInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student_name", "course", "score", "total_questions", "submitted_at")
    readonly_fields = ("submitted_at",)
