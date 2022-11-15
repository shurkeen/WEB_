from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from . import models


def index(request):
    context = {'questions': pagination(request, models.QUESTIONS), 'pagination_item': pagination(request, models.QUESTIONS)}
    return render(request, 'index.html', context = context)

def index_hot(request):
    context = {'questions': pagination(request, models.QUESTIONS), 'pagination_item': pagination(request, models.QUESTIONS)}
    return render(request, 'index_hot.html', context = context)

def question(request, question_idx:int):
    if question_idx > len(models.QUESTIONS):
        return HttpResponse('Error 404')
    content_question_idx = models.QUESTIONS[question_idx - 1]
    context = {'question': content_question_idx, 'answers': pagination(request, models.ANSWERS), 'pagination_item': pagination(request, models.ANSWERS)}
    return render(request, 'question.html', context = context)

def ask(request):
    return render(request, 'ask.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def tag(request, question_tag:str):
    context = {'questions': models.QUESTIONS, 'tmp_tag': question_tag}
    return render(request, 'tag.html', context)

def pagination(request, contact_list):
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)
    return page_objs