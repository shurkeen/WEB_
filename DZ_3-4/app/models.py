from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
import random
from django.db.models import Count

class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.order_by('-date')
    
    def get_hot_questions(self):
        # сортировка по количеству лайков, при равном количестве по дате
        q_sort_by_likes = self.annotate(Count('like')).order_by('-like__count', '-date')
        return q_sort_by_likes
    
    def get_questions_by_tag(self, idx):
        return self.filter(tags__title=idx)
    
    
class TagManager(models.Manager):
    def get_popular_tags(self):
        t_sort_by_usage = self.annotate(Count('question')).order_by('-question__count')
        return t_sort_by_usage
    
class ProfileManager(models.Manager):
    def get_best_profiles(self):
        p_sort_by_questions = self.annotate(Count('question')).order_by('-question__count')
        return p_sort_by_questions

class AnswerManager(models.Manager):
    def get_sort_answers(self):
        return self.annotate(Count('likeanswer')).order_by('-is_correct', '-likeanswer__count', '-date')
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(blank=True, null=True, default='avatars/common_avatar.png', upload_to="avatars/%Y/%m/%d")

    objects = ProfileManager()
    
    def __str__(self):
        return f'Profile #{self.pk}. {self.user.username}'



class Tag(models.Model):
    title       = models.CharField(max_length=30, unique=False)
    objects = TagManager()
    
    def __str__(self):
        return f'Tag #{self.pk}. {self.title}'


class Question(models.Model):
    title       = models.CharField(max_length=200)
    text        = models.TextField(blank=True, null=True)
    date        = models.DateTimeField(auto_now_add=True) #auto_now_add=True
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags        = models.ManyToManyField(Tag)
    
    objects = QuestionManager()
    
    def __str__(self):
        return f'Question #{self.pk}. {self.title}'
    

class Answer(models.Model):
    text        = models.TextField()
    date        = models.DateTimeField(auto_now_add=True) # auto_now_add=True
    is_correct  = models.BooleanField(default=False)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    objects = AnswerManager()
    
    def __str__(self):
        return f'Answer #{self.pk}. {self.text[:10]}'
    
# Like for the Question
class Like(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('question', 'author')
    
    def __str__(self):
        return f'Like: {self.author.user.username} -> {self.question.title}'
                                                                
class LikeAnswer(models.Model):
    answer      = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('answer', 'author')
    
    def __str__(self):
        return f'Like: {self.author.user.username} -> {self.answer}'