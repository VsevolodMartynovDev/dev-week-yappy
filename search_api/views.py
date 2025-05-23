from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from search_api.hashtag_parser import parse_hashtags
from search_api.semantic_search import SemanticSearch


class SearchAPIView(APIView):
    semantic_search = SemanticSearch()

    def get(self, request, *args, **kwargs):
        search_text = request.query_params.get('text')

        if not search_text:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        processed_text = parse_hashtags(search_text)
        results = self.semantic_search.get_combined_links(query=processed_text)
        
        return Response(results)
