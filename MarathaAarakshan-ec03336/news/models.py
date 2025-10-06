from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="शीर्षक")
    content = models.TextField(verbose_name="आशय")
    image_url = models.URLField(blank=True, null=True, verbose_name="प्रतिमा URL")
    date_posted = models.DateTimeField(default=timezone.now, verbose_name="प्रकाशन दिनांक")
    is_featured = models.BooleanField(default=False, verbose_name="वैशिष्ट्यपूर्ण")
    
    class Meta:
        verbose_name = "बातमी"
        verbose_name_plural = "बातम्या"
        db_table = "news"
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title