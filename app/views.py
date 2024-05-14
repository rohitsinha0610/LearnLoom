from django.shortcuts import render, redirect, get_object_or_404
from .forms import signupform, AnnouncementForm, UserUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import logging
from django.contrib.auth.models import User
from .models import Announcement, Classroom, Enrollment, Submission
from django.utils import timezone


@login_required
def assignment_view(request):
    user = request.user
    classroom_obj = get_object_or_404(Classroom)

    context = {
        'class_obj': classroom_obj
    }

    return render(request, 'assignment_page.html', context)




@login_required
def settings_view(request):
    user = request.user  # Retrieve current user
    form = UserUpdateForm(instance=user)  # Create form instance with current user data

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings') 

    return render(request, 'settings.html', {'form': form, 'user': user})



@login_required
def classroom_view(request, pk):
    user = request.user
    classroom_obj = get_object_or_404(Classroom, pk=pk)

    # Check if the user is the teacher of this classroom
    is_teacher = user in classroom_obj.teacher.all()

    # Check if the user is enrolled as a student in this classroom
    is_student = Enrollment.objects.filter(student=user, course=classroom_obj).exists()

    context = {
        'class_obj': classroom_obj,
        'is_teacher': is_teacher,
        'is_student': is_student
    }

    return render(request, 'class_page.html', context)


@login_required
def create_class_view(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        subject_name = request.POST.get('subject_name')
        class_creator = request.user  # Assuming the logged-in user is creating the class
        # Create a new Classroom object
        new_class = Classroom.objects.create(
            class_name=class_name,
            subject_name=subject_name,
            class_creator=class_creator
        )
        # Add the creator as a teacher of the class
        new_class.teacher.add(class_creator)
        return redirect('dashboard')  # Redirect to dashboard after creating the class
    return render(request, 'create_class.html')

@login_required
def join_class_view(request):
    if request.method == 'POST':
        code = request.POST.get('class_code')
        try:
            classroom = Classroom.objects.get(code=code)
            
            # Check if the user is already enrolled in the class
            if Enrollment.objects.filter(student=request.user, course=classroom).exists():
                error_message = 'You are already enrolled in this class.'
                return render(request, 'join_class.html', {'error_message': error_message})
            
            # If user is not already enrolled, create Enrollment object
            Enrollment.objects.create(student=request.user, course=classroom)
            
            # Optionally add success message
            messages.success(request, f'You have successfully joined the class: {classroom.class_name}')
            return redirect('classroom_page', pk=classroom.pk)  # Redirect to class detail page
        
        except Classroom.DoesNotExist:
            error_message = 'Class with the provided code does not exist.'
            return render(request, 'join_class.html', {'error_message': error_message})
    
    return render(request, 'join_class.html')

@login_required
def create_announcement_view(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            creator = request.user
            announcement = Announcement.objects.create(title=title, content=content, classroom=classroom, creator=creator)
            return redirect('classroom_view', pk=classroom_id)  # Redirect to class detail page
    else:
        form = AnnouncementForm()
    
    return render(request, 'create_announcement.html', {'form': form, 'classroom': classroom})


@login_required
def calendar_view(request):
    submits = Submission.objects.all()  # Fetch all events from the database

    # Prepare data in a format suitable for FullCalendar
    event_data = []
    for event in submits:
        event_data.append({
            'title': event.assignment.title, 
            'end': event.end_date.isoformat() if event.end_date else None,   
        })

    return render(request, 'calendar.html', {'events': event_data})


def add_people_view(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    
    if request.method == 'POST':
        teacher_ids = request.POST.getlist('teachers')  # Assuming you have a form to select teachers
        teachers_to_add = User.objects.filter(pk__in=teacher_ids)
        classroom.teachers.add(*teachers_to_add)
        return render(request, 'add_people.html', {'classroom': classroom})
    
    available_teachers = User.objects.exclude(classes_taught=classroom)
    return render(request, 'add_people.html', {'classroom': classroom, 'available_teachers': available_teachers})


def register_view(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
       
    else:
        form = signupform()
    return render(request, 'auth/register.html',{'form':form})


#logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the 'dashboard' URL name
        else:
            # Authentication failed, render the login form with an error message
            return render(request, 'auth/login.html', {'error_message': 'Invalid credentials'})

    else:
        # If it's not a POST request, render the login form
        return render(request, 'auth/login.html')



@login_required
def dashboard_view(request):
    # Retrieve all classrooms created by the logged-in user
    created_classrooms = Classroom.objects.filter(class_creator=request.user)

    # Retrieve all classrooms where the logged-in user is enrolled as a student
    enrolled_classrooms = Classroom.objects.filter(enrollment__student=request.user)

    context = {
        'created_classrooms': created_classrooms,
        'enrolled_classrooms': enrolled_classrooms,
    }

    return render(request, 'dashboard.html', context)


# def dashboard_view(request):
#     return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    pass


def landing_view(request):
    return render(request, 'landing.html')