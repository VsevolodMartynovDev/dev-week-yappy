from rest_framework import serializers


class SearchQuerySerializer(serializers.Serializer):
    text = serializers.CharField(required=True, help_text="Search text or hashtags")

class SearchResultItemSerializer(serializers.Serializer):
    id = serializers.CharField(help_text="Video ID")
    text = serializers.CharField(help_text="Video description")
    score = serializers.FloatField(help_text="Relevance score")
