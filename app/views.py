from django.shortcuts import render, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app import models


def paginate(object_list, request, per_page=3):
    paginator = Paginator(object_list, per_page)
    page = request.GET.get('page', 1)
    try:
        paginator.page(page)
    except PageNotAnInteger:
        raise Http404("Page not found")
    except EmptyPage:
        raise Http404("Page not found")
    else:
        return paginator.page(page)


def index(request):
    questions = paginate(models.Question.objects.get_new_questions(), request)
    return render(request, 'index.html',
                  context={'questions': questions, 'page_obj': questions,
                           'tags': models.Tag.objects.get_popular_tags(),
                           'members': models.Profile.objects.get_popular_profiles()})


def question(request, question_id):
    answers = paginate(models.Answer.objects.get_answers(question_id), request)
    try:
        question_item = models.Question.objects.get(id=question_id)
    except models.Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'question.html',
                  context={'question': question_item, 'answers': answers,
                           'page_obj': answers, 'tags': models.Tag.objects.get_popular_tags(),
                           'members': models.Profile.objects.get_popular_profiles()})


def login(request):
    return render(request, 'login.html', context={'tags': models.Tag.objects.get_popular_tags(),
                                                  'members': models.Profile.objects.get_popular_profiles()})


def signup(request):
    return render(request, 'signup.html', context={'tags': models.Tag.objects.get_popular_tags(),
                                                   'members': models.Profile.objects.get_popular_profiles()})


def settings(request):
    return render(request, 'settings.html', context={'tags': models.Tag.objects.get_popular_tags(),
                                                     'members': models.Profile.objects.get_popular_profiles()})


def ask(request):
    return render(request, 'ask.html', context={'tags': models.Tag.objects.get_popular_tags(),
                                                'members': models.Profile.objects.get_popular_profiles()})


def tag(request, tag_name):
    try:
        models.Tag.objects.get(name=tag_name)
    except models.Tag.DoesNotExist:
        raise Http404('Tag does not exist')
    questions = paginate(models.Question.objects.get_questions_by_tag(tag_name), request)
    return render(request, 'tag.html',
                  context={'tag_name': tag_name, 'questions': questions, 'page_obj': questions,
                           'tags': models.Tag.objects.get_popular_tags(),
                           'members': models.Profile.objects.get_popular_profiles()})


def hot(request):
    questions = paginate(models.Question.objects.get_hot_questions(), request)
    return render(request, 'index.html',
                  context={'questions': questions, 'page_obj': questions,
                           'tags': models.Tag.objects.get_popular_tags(),
                           'members': models.Profile.objects.get_popular_profiles()})

