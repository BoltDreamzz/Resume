from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User

from .utils import get_client_ip
from .forms import CommentForm, MessageForm  # Import the CommentForm if you need a form for comments

from .models import Project, Comment, Like, SubProject, Message


def index(request):
    messages.success(request, "Welcome home")

    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})


def portfolio(request):
    messages.success(request, "Keep exploring 🥂")
    projects = Project.objects.all()
    return render(request, 'projects/portfolio.html', {'projects': projects})


# views.py


def project_detail(request, project_id):
    messages.success(request, "How it it going ?")

    project = get_object_or_404(Project, pk=project_id)
    sub_projects = SubProject.objects.all()
    # sub_projects = get_object_or_404(SubProject, pk=project_id)

    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(project=project, text=form.cleaned_data['text'])
            messages.info(request, "Your comment has been sent")
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(project=project)

    likes = Like.objects.filter(project=project, project_is_liked=True)

    likes_count = likes.count()
    comments_count = comments.count()

    liked_users = [like.user_ip for like in likes]

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'sub_projects': sub_projects,
        'comment_form': form,
        'comments': comments,
        'likes': likes,
        'likes_count': likes_count,
        'comments_count': comments_count,
        'liked_users': liked_users,
    })


def toggle_like(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_ip = get_client_ip(request)

    # Check if the user has already liked the project
    like, created = Like.objects.get_or_create(project=project, user_ip=user_ip)

    # Toggle the 'project_is_liked' field
    like.project_is_liked = not like.project_is_liked
    like.save()
    messages.success(request, "How it it going ?")

    

    # Get the count of likes for the project
    likes_count = Like.objects.filter(project=project, project_is_liked=True).count()

    # You can customize the response based on your needs
    response_data = {
        'project_id': project_id,
        'project_is_liked': like.project_is_liked,
        'likes_count': likes_count,
    }

    if not created:
        # If the like was not created (i.e., it already existed), delete it
        like.delete()

    # Redirect to the project detail page
    return redirect('projects:project_detail', project_id)


def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']

            # Create a new comment for the project
            Comment.objects.create(project=project, text=text)

            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = CommentForm()

    return render(request, 'projects/add_comment.html', {'form': form, 'project': project})


@login_required
def start_conversation(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)

    # Check if a conversation already exists
    existing_conversation = Message.objects.filter(
        sender=request.user,
        recipient=recipient
    ).exists()

    if existing_conversation:
        # Redirect to existing conversation
        return redirect('projects:conversation_detail', conversation_id=existing_conversation.id)
    else:
        # Create a new message instance and redirect to conversation detail
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content='Hi, I am interested in your services'
        )
        messages.success(request, "Message sent")
        return redirect('projects:conversation_detail', conversation_id=message.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Message, id=conversation_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=conversation.recipient) | Q(sender=conversation.recipient,
                                                                     recipient=request.user)).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(
                sender=request.user,
                recipient=conversation.recipient,
                content=content
            )
            # Set is_read to True for all existing messages in the conversation
            messages.update(is_read=True)

            # messages.success(request, "Message sent")

            return redirect('projects:conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    return render(request, 'projects/conversation_detail.html',
                  {'conversation': conversation, 'messages': messages, 'form': form})


@login_required
def inbox(request):
    user = request.user
    conversations = Message.objects.filter(Q(sender=user) | Q(recipient=user)).distinct('sender', 'recipient').order_by(
        '-timestamp')
    return render(request, 'projects/inbox.html', {'conversations': conversations})


def contact(request):
    messages.success(request, "Woo hoo, cheers fam !")
    return render(request, "projects/contact.html")
