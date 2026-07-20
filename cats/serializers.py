import base64
import datetime as dt
from typing import Any

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat


class Hex2NameColor(serializers.Field):
    """Serializer field that stores colors as CSS names but accepts hex input."""

    def to_representation(self, value: str) -> str:
        return value

    def to_internal_value(self, data: str) -> str:
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                "There is no CSS color name for this color value"
            )
        return data


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source="name")

    class Meta:
        model = Achievement
        fields = ("id", "achievement_name")


class Base64ImageField(serializers.ImageField):
    """Accepts images either as multipart uploads or as base64 data URIs."""

    def to_internal_value(self, data: Any) -> Any:
        if isinstance(data, str) and data.startswith("data:image"):
            image_format, imgstr = data.split(";base64,")
            ext = image_format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(required=False, many=True)
    color = Hex2NameColor()
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "color",
            "birth_year",
            "achievements",
            "owner",
            "age",
            "image",
        )
        read_only_fields = ("owner",)

    def get_age(self, obj: Cat) -> int:
        return dt.date.today().year - obj.birth_year

    def validate_birth_year(self, value: int) -> int:
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"birth_year cannot be in the future (got {value}, "
                f"current year is {current_year})"
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> Cat:
        if "achievements" not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        else:
            achievements = validated_data.pop("achievements")
            cat = Cat.objects.create(**validated_data)
            for achievement in achievements:
                current_achievement, _ = Achievement.objects.get_or_create(
                    **achievement
                )
                AchievementCat.objects.create(achievement=current_achievement, cat=cat)
            return cat

    def update(self, instance: Cat, validated_data: dict[str, Any]) -> Cat:
        instance.name = validated_data.get("name", instance.name)
        instance.color = validated_data.get("color", instance.color)
        instance.birth_year = validated_data.get("birth_year", instance.birth_year)
        instance.image = validated_data.get("image", instance.image)
        if "achievements" in validated_data:
            achievements_data = validated_data.pop("achievements")
            lst = []
            for achievement in achievements_data:
                current_achievement, _ = Achievement.objects.get_or_create(
                    **achievement
                )
                lst.append(current_achievement)
            instance.achievements.set(lst)

        instance.save()
        return instance
