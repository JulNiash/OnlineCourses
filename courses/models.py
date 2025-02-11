from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)


class Course(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    @property
    def part_count(self):
        return self.parts.count()

    def __str__(self):
        return self.title


class CoursePart(BaseModel):
    course = models.ForeignKey(Course, related_name='parts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('course', 'title')

    def __str__(self):
        return f"{self.course.title}--{self.title}"


class CourseTopic(BaseModel):
    part = models.ForeignKey(CoursePart, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('part', 'title')

    def __str__(self):
        return f"{self.part.title}--{self.title}"


class TopicDocument(BaseModel):
    topic = models.ForeignKey(CourseTopic, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='topic_documents/')

    def __str__(self):
        return self.name


class TopicText(BaseModel):
    topic = models.ForeignKey(CourseTopic, related_name='text', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Text for {self.topic.title}"


class Quiz(BaseModel):
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ('course', 'title')

    def __str__(self):
        return f"{self.course.title}--{self.title}"


class QuizQuestion(BaseModel):
    quiz = models.ForeignKey(Quiz, related_name='question', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Question in {self.quiz.title}"


class QuizAnswer(BaseModel):
    question = models.ForeignKey(QuizQuestion, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Answer in {self.question.text}"


class UserProgress(BaseModel):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='user_postgress', on_delete=models.CASCADE)
    completed_quizzes = models.JSONField(default=dict)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"progress for {self.user.username} in {self.course.title}"


class Certificate(BaseModel):
    user = models.ForeignKey(User, related_name='certificates', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='certificates', null=True, on_delete=models.SET_NULL)
    certificate_body = models.TextField()

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"Certificate for {self.user.username} in {self.course.title}"