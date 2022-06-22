from rest_framework import serializers

from reviews.models import Categories, Genres, Titles



class CategoriesSerializer(serializers.ModelSerializer):


    class Meta:
        fields = ('name', 'slug')
        model = Categories