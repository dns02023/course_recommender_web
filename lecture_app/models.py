from django.db import models

class Lecture(models.Model):
    # 학수번호
    lectid = models.CharField(max_length=10)
    # lectname
    lectname = models.CharField(max_length=100)
    # professor
    professor = models.CharField(max_length=50)

    def __str__(self):
        return self.lectname

    class Meta:
        db_table = 'lectures'

