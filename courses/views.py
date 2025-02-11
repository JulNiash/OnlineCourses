from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TopicDocumentForm, CourseForm, CoursePartForm, CourseTopicForm, RegistrationForm
from .models import TopicDocument, Course, CoursePart, CourseTopic

# Main page

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")  # Или "register", если хочешь сразу регистрацию
    return render(request, "home.html")

# Registration / logout

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("course_list")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form":form})


def user_logout(request):
    logout(request)
    return redirect("login")  # После выхода перенаправляем на страницу входа



#Course functions
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {"courses" : courses})


def course_detail(request, course_id):
    courses = get_object_or_404(Course, id = course_id)
    return render(request, 'courses/course_detail.html', {"course" : courses})

@login_required
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            courses = form.save(commit=False)
            courses.save()
            return redirect("course_list")
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id = course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.delete()
        return redirect("course_list")
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


#CoursePart functions
def course_part_list(request, course_id):
    courses = get_object_or_404(Course, id = course_id)
    return render(request, "courses/course_part_list.html", {'course_parts': courses.parts.all(), 'course': courses})


def course_part_detail(request, course_id, part_id):
    part = get_object_or_404(CoursePart, id=part_id, course_id=course_id)
    course = part.course
    return render(request, 'courses/course_part_detail.html', {'part': part, 'course': course})

@login_required
def create_course_part(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CoursePartForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            part.course = course
            part.save()
            return redirect("course_part_list", course_id=course.id)
    else:
        form = CoursePartForm()

    return render(request, "courses/course_part_form.html", {"form": form, "course": course})

@login_required
def update_course_part(request, course_id, part_id):
    part = get_object_or_404(CoursePart, id = part_id, course_id=course_id)
    course = part.course

    if request.method == "POST":
        form = CoursePartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect("course_part_list", course_id = course_id)
    else:
        form = CoursePartForm(instance=part)

    return render(request, "courses/course_part_form.html", {"form": form, "part": part, "course":course})

@login_required
def delete_course_part(request, course_id, part_id):
    part = get_object_or_404(CoursePart, id=part_id, course_id=course_id)

    if request.method == "POST":
        part.delete()
        return redirect("course_part_list", course_id=course_id)

    return render(request, "courses/course_part_confirm_delete.html", {"part": part})


#CourseTopic functions
def course_topic_list(request, course_id, part_id):
    part = get_object_or_404(CoursePart, id=part_id, course_id=course_id)
    topics = part.topics.all()

    print("Part:", part)  # Должен показать часть курса
    print("Topics:", topics)  # Должен показать QuerySet топиков

    return render(request, "courses/course_topic_list.html", {"part": part, "topics": topics})


def course_topic_detail(request, course_id, part_id, topic_id):
    topic = get_object_or_404(CourseTopic, id=topic_id, part__id=part_id, part__course_id=course_id)
    part = get_object_or_404(CoursePart, id=part_id, course_id=course_id)
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_topic_detail.html", {"topic": topic, "part": part, "course": course})

@login_required
def course_topic_create(request, course_id, part_id):
    part = get_object_or_404(CoursePart, course_id=course_id, id=part_id)

    if request.method == "POST":
        form = CourseTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.part = part
            topic.save()
            return redirect("course_topic_list", course_id=course_id, part_id=part.id)
    else:
        form = CourseTopicForm()

    return render(request, "courses/course_topic_form.html", {"form": form, "part": part})

@login_required
def course_topic_update(request, topic_id, part_id, course_id):
    topic = get_object_or_404(CourseTopic, id = topic_id, part__id = part_id, part__course_id = course_id)
    part = get_object_or_404(CoursePart, id = part_id, course_id = course_id)

    if request.method == "POST":
        form = CourseTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("course_topic_list", course_id = course_id, part_id = part_id)
    else:
        form = CourseTopicForm(instance=topic)

    return render(request, "courses/course_topic_form.html", {'form': form, "part" : part})

@login_required
def course_topic_delete(request, topic_id, part_id, course_id):
    topic = get_object_or_404(CourseTopic, id = topic_id, part__id = part_id, part__course_id = course_id)

    if request.method == "POST":
        topic.delete()
        return redirect("course_topic_list", course_id=course_id, part_id=part_id)

    return render(request, "courses/course_topic_confirm_delete.html", {'topic' : topic})






#TopicDocument views
def document_list(request):
    if request.method == "POST":
        form = TopicDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = TopicDocumentForm()

    documents = TopicDocument.objects.all()
    return render(request, 'documents/document_list.html', {'form' : form, 'documents' : documents})

@login_required
def update_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        form = TopicDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = TopicDocumentForm(instance=document)

    return render(request, 'documents/update_document.html', {'form': form, 'document': document})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(TopicDocument, id=document_id)

    if request.method == 'POST':
        document.delete()
        return redirect('document_list')

    return render(request, 'documents/confirm_delete.html', {'document': document})


