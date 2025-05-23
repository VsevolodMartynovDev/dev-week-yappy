from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SearchQuerySerializer
from .hashtag_parser import parse_hashtags
from .semantic_search import SemanticSearch


class SearchAPIView(APIView):
    semantic_search = SemanticSearch()

    def get(self, request, *args, **kwargs):
        serializer = SearchQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        search_text = serializer.validated_data['text']
        
        processed_text = parse_hashtags(search_text)
        results = self.semantic_search.get_combined_links(query=processed_text)
        
        return Response(results)
