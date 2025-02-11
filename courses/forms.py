from django import forms
from django.contrib.auth.models import User

from .models import TopicDocument, CourseTopic, Course, CoursePart


class TopicDocumentForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset = CourseTopic.objects.all(),
        empty_label="Select a Topic",
        required=True
    )

    class Meta:
        model = TopicDocument
        fields = ['name', 'file', 'topic']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CoursePartForm(forms.ModelForm):
    class Meta:
        model = CoursePart
        fields = ['title']

class CourseTopicForm(forms.ModelForm):
    class Meta:
        model = CourseTopic
        fields = ['title']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match")

        return cleaned_data
