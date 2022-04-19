from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']
