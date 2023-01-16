import datetime
import random

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from math import ceil
import time
import datetime
from app import models


# требование к заполнению - изначально база пустая
class Command(BaseCommand):
    help = 'Command to do........'
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, help='ratio of filling db')

    def handle(self, *args, **kwargs):
        try:
            ratio = kwargs["ratio"]
            print("Filling...")
            start_time = datetime.datetime.now()
            self.fill_tags(ratio * 1)
            self.fill_users(ratio * 1)
            self.fill_questions(ratio * 10)
            self.fill_answers(ratio * 100)
            self.fill_likes(ratio * 200)
            print("End of filling!")
            print('Total time: {}'.format(datetime.datetime.now() - start_time))

        except Exception as e:
            print("Exception")
            CommandError(repr(e))
            
    # 1
    def fill_tags(self, n):
        start_time = datetime.datetime.now()
        
        tags = []
        for i in range(1, n + 1):
            tags.append(models.Tag(id = i, title=f'tag{i}'))
        models.Tag.objects.bulk_create(tags)
        
        print('Duration fill_tags: {}'.format(datetime.datetime.now() - start_time))
    
    # 1
    def fill_users(self, n):
        start_time = datetime.datetime.now()
        
        profiles = []
        users = []
        for i in range(1, n + 1):
            users.append(models.User(id = i, username=f'username{i}', password='1Q2w3e4r5t_'))
        models.User.objects.bulk_create(users)
        for i in range(1, n + 1):
            
            profiles.append(models.Profile(id = i, user_id=i))
        models.Profile.objects.bulk_create(profiles)
        
        print('Duration fill_users: {}'.format(datetime.datetime.now() - start_time))
      
    # 10
    def fill_questions(self, n):
        start_time = datetime.datetime.now()
        
        questions = []
        profiles = models.Profile.objects.all();
        for i in range(1, n + 1):
            author = random.choice(profiles)
            questions.append(models.Question(
                id = i,
                title = f'Question tittle {i}', 
                text = f'How can I drink {i} liters of milk?', 
                author = author, 
                date = self.fake.date_time_between(start_date='-5y', end_date='now', tzinfo=datetime.timezone.utc)
                ))
        models.Question.objects.bulk_create(questions)
        
        list_tags = list(models.Tag.objects.all())
        for q in models.Question.objects.all():
            # от 1 до 10 тегов на вопрос
            list_random_tags = random.sample(list_tags, random.randint(1, 10))
            # вроде, add эффективнее, чем set
            q.tags.add(*list_random_tags)
        
        print('Duration fill_questions: {}'.format(datetime.datetime.now() - start_time))

    # 100
    def fill_answers(self, n):
        start_time = datetime.datetime.now()
        
        answers = []
        authors = models.Profile.objects.all()
        questions = models.Question.objects.all()
        for i in range(1, n + 1):
            answers.append(models.Answer(
                id = i,
                text = f'Answer text number {i}',
                date = self.fake.date_time_between(start_date='-5y', end_date='now', tzinfo=datetime.timezone.utc),
                is_correct = False,
                author = random.choice(authors),
                question = random.choice(questions),
                ))
        models.Answer.objects.bulk_create(answers)
        
        print('Duration fill_answers: {}'.format(datetime.datetime.now() - start_time))

    # 200
    def fill_likes(self, n):
        start_time = datetime.datetime.now()
        likes = []
        count_likes_for_user = ceil(n / models.Profile.objects.all().count())
        profiles = models.Profile.objects.all()
        list_questions = list(models.Question.objects.all())
        i = 1
        for p in profiles:
            qs = random.sample(list_questions, count_likes_for_user)
            for q in qs:
                likes.append(models.Like(id = i, question = q, author = p))
                i += 1
        models.Like.objects.bulk_create(likes)
        likes = []        
        print('Duration fill_likes: {}'.format(datetime.datetime.now() - start_time))