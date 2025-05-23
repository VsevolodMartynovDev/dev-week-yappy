from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from search_api.hashtag_parser import parse_hashtags
from search_api.semantic_search import semantic_search


class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        search_text = request.query_params.get('text')

        if not search_text:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        processed_text = parse_hashtags(search_text)
        results = semantic_search.get_combined_links(query=processed_text)
        
        return Response(results)


def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        processed_query = parse_hashtags(query)
        
        vector = semantic_search.model.encode([processed_query], normalize_embeddings=True)
        search_results = semantic_search.search_combined_scores(vector, top_k=10)
        
        for result in search_results:
            results.append({
                'filename': result['filename'],
                'score': result['score'],
                'description': result.get('description', ''),
                'transcription': result.get('transcription', ''),
                'url': f"{semantic_search.source_url_base}{result['filename']}"
            })
    
    return render(request, 'search_api/search.html', {
        'query': query,
        'results': results
    })
