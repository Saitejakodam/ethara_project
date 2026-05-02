from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Project, Task
from datetime import date


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    projects = Project.objects.filter(members=request.user)

    my_tasks = Task.objects.filter(assigned_to=request.user)

    overdue_tasks = Task.objects.filter(
        assigned_to=request.user,
        due_date__lt=date.today()
    ).exclude(status='Completed')

    context = {
        'profile': profile,
        'projects': projects,
        'my_tasks': my_tasks,
        'overdue_tasks': overdue_tasks,
    }

    return render(request, 'tasksystem/dashboard.html', context)


@login_required
def create_project(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != 'Admin':
        return redirect('/dashboard/')

    users = User.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        member_ids = request.POST.getlist('members')

        project = Project.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )

        project.members.add(request.user)

        for member_id in member_ids:
            member = User.objects.get(id=member_id)
            project.members.add(member)

        return redirect('/dashboard/')

    return render(request, 'tasksystem/create_project.html', {'users': users})


@login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    tasks = Task.objects.filter(project=project)

    return render(request, 'tasksystem/project_details.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    members = project.members.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=User.objects.get(id=assigned_to),
            due_date=due_date
        )

        return redirect(f'/project/{project.id}/')

    return render(request, 'tasksystem/create_task.html', {
        'project': project,
        'members': members
    })


@login_required
def my_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'tasksystem/my_tasks.html', {
        'tasks': tasks
    })


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()

        return redirect('/mytasks/')

    return render(request, 'tasksystem/edit_task.html', {
        'task': task
    })