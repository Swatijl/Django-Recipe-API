from rest_framework import serializers
from recipe_app.models import Tag,Ingredient,Recipe

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    class Meta:
        model = Recipe
        fields = ('id','title','ingredient','tag','time_minutes','link','price')
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
    ingredient = IngredientSerializer(many=True,read_only=True)
    tag = TagSerializer(many=True, read_only=True)

class RecipeImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id','image')
        read_only_fields = ('id',)