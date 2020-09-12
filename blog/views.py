from django.core.exceptions import ValidationError
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from blog.models import Post, Tag, Tagging
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from blog.forms import Registration
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

class TagDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        print('tag detail' + str(id))
        tags = Tag.objects.get(id=id)
        print(tags)
        posts = Post.objects.filter(tags__id=id)
        print(posts)
        return render(request, 'blog/tag_detail.html', {'tags': tags, 'post_list': posts})


class TagCreateView(CreateView):
    model = Tag
    fields = ['tag']


class PostConnectView(CreateView):
    model = Tagging
    fields = ['taggings']

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        id = self.kwargs['pk']
        object.posts_id=id
        object.save()
        print('finish')
        return super(CreateView, self).form_valid(form)




class PostDetailView(DetailView):
    model = Post

    def post(self, request):
        post = request.POST['post']
        tag = request.POST['tag']
        posts = Post.objects.create(post=post)
        tags, created = Tag.objects.get_or_create(tag=tag)
        tp = Tagging(posts=posts, taggings=tags)
        tp.save()
        return render(request, 'blog/post_detail.html')

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        print(id)
        post = Post.objects.get(id=id)
        tags = post.tags.all()
        return render(request, 'blog/post_detail.html', {'tags_list': tags, 'post' : post})


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'image']

    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        print(self.request.user)
        if self.request.user.is_authenticated:
            object.owner = self.request.user
        object.save()
        return super(CreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text', 'image']

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(UpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class PostDeleteView(DeleteView):
    model = Post

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(DeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        qs = super(ListView, self).get_queryset()
        return qs.order_by('created_at').reverse()[:10]

    def get(self, request, *args, **kwargs):
        post_list = Post.objects.all().order_by('created_at').reverse()
        paginator = Paginator(post_list, 10)  # Show 10 posts per page
        page = request.GET.get('page')
        stuff = paginator.get_page(page)
        return render(request, 'blog/post_list.html', {'post_list': stuff})


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = Registration
    success_url = 'posts'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        password = form.clean_password2()
        name = form.clean_name()
        user = authenticate(self.request, username=name, password=password)
        if user is None:
            us1 = User.objects.create_user(name, None, password)
            us1.save()
        else:
            print("User already exits!")
            raise ValidationError("User already exits!")
        return super().form_valid(form)
