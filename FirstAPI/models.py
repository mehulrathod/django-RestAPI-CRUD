from django.db import models


# superuser name: rathod pw: akhil@1996
# https://www.youtube.com/watch?v=EEF3C2ymvTw&list=PLL2hlSFBmWwyYlQWXaZso8xlXlr5PsKj_&index=10

class Person(models.Model):
    Name = models.CharField(max_length=30)
    Birthday = models.DateField()
    Age = models.IntegerField()

    def __str__(self):
        return " {}".format(self.Name)
