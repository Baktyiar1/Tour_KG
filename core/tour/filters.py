from django_filters import rest_framework as filters

from .models import Region, Date_tour, Tour

class RegionFilter(filters.FilterSet):
    class Meta:
        model = Region
        fields = ('title', )

class Date_tourFilter(filters.FilterSet):
    class Meta:
        model = Date_tour
        fields = ('start_date', )

class TourFilter(filters.FilterSet):
    regions = filters.ModelMultipleChoiceFilter(queryset=Region.objects.all(), field_name='regions__title',
                                                to_field_name='title', label='Регионы')
    date_tour = filters.ModelMultipleChoiceFilter(queryset=Date_tour.objects.all(), field_name='date_tour__start_date',
                                                  to_field_name='start_date', label='Даты тура')

    class Meta:
        model = Tour
        fields = (
            'regions',
            'date_tour'
        )















