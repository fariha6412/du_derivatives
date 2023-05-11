import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, ProjectForm, UserForm
from .models import Project, User, Photo, Review, Reply, ProjectType, Rating
from .utils import generate_token
from django.utils.safestring import mark_safe


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    if request.GET.get('Website') == 'Websites':
        type = 'Website'
    else:
        type = 'Application'
    projectType = ProjectType.objects.get(name=type)
    top_apps = {}
    if request.method == "POST":
        min_batch = request.POST['min-batch']
        max_batch = request.POST['max-batch']
        projects = Project.objects.none()
        try:
            users = User.objects.filter(csedu_batch__gte=min_batch, csedu_batch__lte=max_batch)
        except:
            try:
                users = User.objects.filter(csedu_batch__gte=min_batch)
            except:
                users = User.objects.filter(csedu_batch__lte=max_batch)

        for user in users:
            projects |= Project.objects.filter(type=projectType) & (Project.objects.filter(developer=user) | Project.objects.filter(collaborators=user)) & (
                    Project.objects.filter(title__icontains=q) | Project.objects.filter(
                tags__icontains=q) | Project.objects.filter(about__icontains=q))
        i = 0
        top_apps = []
        for pr in projects.order_by('-rate'):
            top_apps += [{'id': i + 1, 'app': pr}]
            i += 1
            if i == 10:
                break
    else:
        projects = Project.objects.filter(type=projectType) & (
                Project.objects.filter(title__icontains=q) | Project.objects.filter(
            tags__icontains=q) | Project.objects.filter(about__icontains=q))
        i = 0
        top_apps = []
        for pr in projects.order_by('-rate'):
            top_apps += [{'id': i + 1, 'app': pr}]
            i += 1
            if i == 10:
                break
    project_count = projects.count()
    return render(request, 'homepage.html',
                  {'top_chart_apps': top_apps, 'general_apps': projects,
                   'selected_text': type, 'project_count': project_count})


def profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.GET.get('Website') == 'Websites':
        type = 'Website'
    else:
        type = 'Application'

    projectType = ProjectType.objects.get(name=type)
    projects = Project.objects.filter(developer=user) & Project.objects.filter(
        type=projectType) | Project.objects.filter(collaborators=user)
    project_count = projects.count()
    apps = []
    for i, project in enumerate(projects):
        apps += [{'i': i + 1, 'app': project}]
    return render(request, 'profile.html',
                  {'apps': apps, 'selected_text': type, 'project_count': project_count, 'user': user})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    global user
    if request.method == "POST":
        post_data = request.POST or None
        if post_data is not None:
            username = request.POST['username']
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=username)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if not user.is_email_verified:
                        messages.error(request,
                                       'Please verify your email. Check your spam folder also')
                        return redirect('login')

                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'wrong password', extra_tags='timeout: 5000')
                    return redirect('login')
            except:
                messages.error(request, 'Username or password doesn\'t exist.', extra_tags='timeout:5000')
                return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.error(request, 'Email verified, you can login now.')
        return redirect('login')

    return render(request, 'activate-failed.html', {'user': user})


def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your CSEDU_derivatives account'
    email_body = render_to_string('activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
                         to=[user.email])

    email.send()


def signup(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            send_action_email(user, request)
            messages.error(request, 'Please go to your email to verify. Check your spam folder also')

            # login(request, user)
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, str(mark_safe(error)))
            return redirect('signup')

    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def addProject(request):
    developer = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.developer = developer
            project.save()
            return redirect('addProjectCtd', pk=project.id)
        else:
            messages.error(request, 'An error has occurred')

    form = ProjectForm()
    return render(request, 'addProject.html', {'form': form})


@login_required(login_url='login')
def userUpdate(request):
    user = request.user
    form = UserForm(instance=user)
    old_image = user.profile_picture
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if old_image != user.profile_picture:
                os.remove(old_image.path)
            return redirect('profile')

    return render(request, 'userUpdate.html', {'form': form})


@login_required(login_url='login')
def projectUpdate(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('addProjectCtd', pk=project.id)

    return render(request, 'addProject.html', {'form': form})


@login_required(login_url='login')
def addProjectCtd(request, pk):
    project = Project.objects.get(pk=pk)
    photos = Photo.objects.filter(project=project)
    collaborators = project.collaborators.all()
    tag_str = Project.objects.get(pk=pk).tags
    if tag_str is None or tag_str == '':
        tags = []
        tag_str = ''
    else:
        tags = tag_str.split(',')
        if '' in tags:
            tags.remove('')

    if request.method == 'POST':

        # for adding collaborator
        if request.POST.get('email', False):
            try:
                new_collaborator = User.objects.get(email=request.POST['email'])
                if new_collaborator != request.user:
                    if new_collaborator not in collaborators:
                        project.collaborators.add(new_collaborator)
                        project.save()
                        return redirect('addProjectCtd', pk)
                    else:
                        messages.error(request, 'Already in list')
                        return redirect('addProjectCtd', pk)
                else:
                    messages.error(request, 'You are the developer')
                    return redirect('addProjectCtd', pk)
            except:
                messages.error(request, 'No user found')
                return redirect('addProjectCtd', pk)
                # print("no user found")

        # for adding tag
        if request.POST.get('tag', False):
            tag_str += (',' + request.POST['tag'])
            project.tags = tag_str
            project.save()
            return redirect('addProjectCtd', pk)

        # for uploading images
        if request.FILES:
            files = request.FILES.getlist('files')

            for file in files:
                new_photo_file = Photo.objects.create(
                    project=project,
                    photo=file
                )
                new_photo_file.save()
            return redirect('addProjectCtd', pk)

        # for adding review

    return render(request, 'addProjectCtd.html',
                  {'project': project, 'photos': photos, 'tags': tags, 'collaborators': collaborators})


@login_required(login_url='login')
def deletePhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    photoPath = photo.photo.path
    photo.delete()
    os.remove(photoPath)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def deleteCollaborator(request, pk, collaborator):
    project = Project.objects.get(id=pk)
    project.collaborators.remove(collaborator)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def deleteTag(request, pk, tag):
    project = Project.objects.get(id=pk)
    tags = project.tags.split(',')
    tags.remove(tag)
    project.tags = ','.join(tags)
    project.save()
    return redirect(request.META.get('HTTP_REFERER'))


def retriveDetails(request, pk):
    project = Project.objects.get(pk=pk)
    ssimages = Photo.objects.filter(project=project)
    tag_str = project.tags
    if tag_str is None or tag_str == '':
        tags = []
        tag_str = ''
    else:
        tags = tag_str.split(',')
        if '' in tags:
            tags.remove('')
    if request.user.is_authenticated:
        old_rating = Rating.objects.filter(user=request.user) & Rating.objects.filter(project=project)
    else:
        old_rating = [0]
    try:
        user_rating = old_rating[0].star if old_rating is not None else 0
    except:
        user_rating = 0

    reviews_qs = Review.objects.filter(project=project)
    reviews = []
    for rqs in reviews_qs:
        replies = Reply.objects.filter(review=rqs)
        reviews += [{
            'id': rqs.id,
            'reviewer_profile_picture': rqs.reviewer.profile_picture,
            'reviewer': rqs.reviewer,
            'date': rqs.date_added,
            'comment': rqs.comment,
            'replies': replies,
        }]
    review_count = reviews_qs.count() if reviews_qs.count() is not None else 0

    return {'project':project, 'tags': tags, 'ssimages': ssimages, 'review_count': review_count,
            'reviews': reviews, 'range': range(5), 'user_rating': user_rating}


def projectDetails(request, pk):
    project = Project.objects.get(pk=pk)
    context = retriveDetails(request, pk)

    if request.method == 'POST':

        # for adding review
        if request.POST.get('review', False):
            try:
                Review.objects.create(
                    comment=request.POST['review'],
                    project=project,
                    reviewer=request.user)
                return redirect('projectDetails', pk)
            except:
                print("review error")

    return render(request, 'projectDetails.html', context)


@login_required(login_url='login')
def addReply(request, projectPK, reviewPK):
    if request.method == 'POST':

        # for adding reply
        if request.POST.get('reply', False):
            review = Review.objects.get(pk=reviewPK)
            try:
                Reply.objects.create(
                    details=request.POST['reply'],
                    review=review)
                return redirect('projectDetails', projectPK)
            except:
                print("reply error")


def update_rating(request):
    if request.method == 'POST':
        # Get the project object
        project_id = request.POST.get('project_id')
        project = Project.objects.get(pk=project_id)

        # Get the new rating value from the form
        new_rating = int(request.POST.get('rating'))
        old_rating = Rating.objects.filter(user=request.user) & Rating.objects.filter(project=project)
        if old_rating is not None:
            old_rating.delete()
        # Update the rating value for the project
        ratings = Rating.objects.filter(project=project)
        total_ratings_count = ratings.count() if ratings.count() is not None else 0
        total_rating = total_ratings_count * project.rate
        project.rate = (total_rating + new_rating) / (total_ratings_count + 1)
        Rating.objects.create(
            star=new_rating,
            user=request.user,
            project=project
        )
        project.save()

        # Render the project detail page
    return render(request, 'projectDetails.html', retriveDetails(request, project_id))

