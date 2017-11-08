from django.db import models

# Create your models here.
class MontrealGazetteArticle(models.Model):
    url = models.URLField()
    original_text = models.TextField(blank = True)
    modified_text = models.TextField(blank = True)

    def __str__(self):
        return self.url