import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

import django

django.setup()

from articles.models import Article, Tag, Scope

article = Article.objects.all()
for item in article:
    print(item.scopes.all())
scopes = Scope.objects.all()
for item in scopes:
    print(item.tag.name)
print(Tag.objects.all())