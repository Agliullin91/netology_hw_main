from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True,)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if self.context["request"].method == "POST":
            user = self.context["request"].user
            advs = Advertisement.objects.filter(creator=user, status='OPEN')
            if len(advs) > 9:
                raise serializers.ValidationError('Too many opened ads!')
        elif self.context["request"].method == "PATCH" and self.context["request"].data["status"] == "OPEN":
            user = self.context["request"].user
            advs = Advertisement.objects.filter(creator=user, status='OPEN')
            if len(advs) > 9:
                raise serializers.ValidationError('Too many opened ads! Only 10 opened ads are allowed!')
        # TODO: добавьте требуемую валидацию

        return data
