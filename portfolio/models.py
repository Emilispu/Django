from django.db import models
from django.utils import timezone



class Pages(models.Model):
    title = models.CharField('Title', max_length=300, null=False)
    author = models.CharField('Author', max_length=100, null=False)
    created_data = models.DateField(auto_created=True, default=timezone.now)
    content = models.TextField('Primary_text', null=False)
    text = models.TextField("Secondary_text", null=True)
    images = models.ImageField('Image', upload_to='media/img', null=True, blank=True)
    downloads = models.FileField(upload_to='download', null=True, blank=True)
    href_to_site = models.CharField('link to site', max_length=200, null=True)
    href_name = models.CharField('link', max_length=50, null=True)
    href_to_github = models.CharField('link to Github', max_length=200, null=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class PageReview(models.Model):
    title = models.ForeignKey('Pages', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.CharField('Reviewer', max_length=100, null=False)
    data_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Review', max_length=2000)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        sorted('data_created')

    def __str__(self):
        return f'{self.title}, {self.reviewer}, {self.data_created}'


