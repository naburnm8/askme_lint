from django.contrib.auth.models import User
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404


class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.order_by('created_at')

    def get_hot_questions(self):
        return self.order_by('-likes')

    def get_questions_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)


class AnswerManager(models.Manager):

    def get_answers(self, question):
        return self.filter(question=question).order_by('-created_at')


class TagManager(models.Manager):

    def get_popular_tags(self):
        return self.annotate(num_question=models.Count('question')).order_by('-num_question')[:9]


class ProfileManager(models.Manager):

    def get_popular_profiles(self):
        return self.all()[:9]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    avatar = models.ImageField(null=True, upload_to='avatar/', blank=True, default='profile.jpg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=32)

    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=512)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, default="")
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.IntegerField(default=0)
    amount_of_answers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default="")
    content = models.TextField(max_length=512)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, default="")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()


class QuestionLike(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    like = models.BooleanField(default=0)

    class Meta:
        unique_together = ('question', 'author')

    def __str__(self):
        return self.author.user.username


class AnswerLike(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    like = models.BooleanField(default=0)

    class Meta:
        unique_together = ('answer', 'author')

    def __str__(self):
        return self.author.user.username


