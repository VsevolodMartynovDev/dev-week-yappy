from django.db import connection
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class SemanticSearch:
    def __init__(
            self,
            model_name='paraphrase-multilingual-MiniLM-L12-v2',
            source_url_base='https://s3.ritm.media/hackaton-itmo/',
    ):
        self.model = SentenceTransformer(model_name)
        self.source_url_base = source_url_base

        self.db_data = self._load_vectors_from_db()

        self.desc_index, self.desc_ids = self._build_description_index()
        self.trans_index, self.trans_ids = self._build_transcription_index()

    def _load_vectors_from_db(self):
        with connection.cursor() as cur:
            cur.execute("""
                SELECT id, filename, 
                       description_vector, transcription_vector
                FROM items
                WHERE description_vector IS NOT NULL OR transcription_vector IS NOT NULL
            """)

            results = []
            for row in cur.fetchall():
                desc_vector = self._parse_vector(row[2]) if row[2] else None
                trans_vector = self._parse_vector(row[3]) if row[3] else None

                results.append({
                    'id': row[0],
                    'filename': row[1],
                    'description_vector': desc_vector,
                    'transcription_vector': trans_vector
                })

            return results

    def _build_description_index(self):
        desc_items = [item for item in self.db_data if item['description_vector'] is not None]

        if not desc_items:
            return None, []

        vectors = np.array([item['description_vector'] for item in desc_items])
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)

        ids = [item['id'] for item in desc_items]

        return index, ids

    @staticmethod
    def _parse_vector(vector_string):
        if vector_string is None:
            return None

        if isinstance(vector_string, (list, np.ndarray)):
            return np.array(vector_string)

        if isinstance(vector_string, str):
            vector_string = vector_string.replace("np.str_('", "").replace("')", "")
            clean_string = vector_string.strip('[]{}()').replace(' ', '')
            try:
                vector_values = [float(x) for x in clean_string.split(',')]
                return np.array(vector_values)
            except ValueError:
                print(f"Error parsing vector: {vector_string[:100]}...")
                return None

        return None

    def _build_transcription_index(self):
        trans_items = [item for item in self.db_data if item['transcription_vector'] is not None]

        if not trans_items:
            return None, []

        vectors = np.array([item['transcription_vector'] for item in trans_items])
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)

        ids = [item['id'] for item in trans_items]

        return index, ids

    def _get_item_by_id(self, item_id):
        for item in self.db_data:
            if item['id'] == item_id:
                return item
        return None

    def search_description(self, query_vector, top_k=10):
        if self.desc_index is None:
            return []

        scores, indices = self.desc_index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            item_id = self.desc_ids[idx]
            item = self._get_item_by_id(item_id)

            if item:
                results.append({
                    'score': float(score),
                    'id': item['id'],
                    'filename': item['filename'],
                })

        return results

    def search_transcription(self, query_vector, top_k=10):
        if self.trans_index is None:
            return []

        scores, indices = self.trans_index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            item_id = self.trans_ids[idx]
            item = self._get_item_by_id(item_id)

            if item:
                results.append({
                    'score': float(score),
                    'id': item['id'],
                    'filename': item['filename'],
                })

        return results

    def search_combined_scores(self, query_vector, top_k=10, threshold=0.5):
        desc_results = self.search_description(query_vector, top_k=1000)
        trans_results = self.search_transcription(query_vector, top_k=1000)

        video_scores = {}

        for result in desc_results:
            filename = result['filename']
            video_scores[filename] = video_scores.get(filename, {})
            video_scores[filename]['description'] = result['score']

        for result in trans_results:
            filename = result['filename']
            video_scores[filename] = video_scores.get(filename, {})
            video_scores[filename]['transcription'] = result['score']

        combined_results = []
        for filename, scores in video_scores.items():
            score_desc = scores.get('description', 0)
            score_trans = scores.get('transcription', 0)
            score_combined = score_desc + score_trans

            if score_combined >= threshold:
                item = next((item for item in self.db_data if item['filename'] == filename), None)

                if item:
                    combined_results.append({
                        'filename': filename,
                        'score': score_combined,
                        'score_description': score_desc,
                        'score_transcription': score_trans,
                        'id': item['id']
                    })

        combined_results.sort(key=lambda x: x['score'], reverse=True)
        return combined_results[:top_k]

    def get_combined_links(self, query: str, top_k: int = 10, threshold: float = 0.6):
        vec = self.model.encode([query], normalize_embeddings=True)
        results = self.search_combined_scores(
            vec,
            top_k=top_k,
            threshold=threshold,
        )
        return [f"{self.source_url_base}{r['filename']}" for r in results]

    def reload_vectors(self):
        self.db_data = self._load_vectors_from_db()
        self.desc_index, self.desc_ids = self._build_description_index()
        self.trans_index, self.trans_ids = self._build_transcription_index()
