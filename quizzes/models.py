from django.db import models


class Quiz(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"Quiz {self.id} - Category: {self.category}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Question {self.id} - Quiz {self.quiz.id}, Text: {self.text}"


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option {self.id} - Question {self.question.id}, Text: {self.text}"


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"UserAnswer - Question {self.question.id}, Selected Choice: {self.selected_choice.text}"
