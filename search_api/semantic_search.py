from collections import defaultdict

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json


class SemanticSearch:
    def __init__(
            self,
            model_name='paraphrase-multilingual-MiniLM-L12-v2',
            embeddings_path='/Users/vsevolodmartynov/repos/yappy/temp/embeddings_total.npy',
            metadata_path='/Users/vsevolodmartynov/repos/yappy/temp/metadata_total.json',
            source_json_path='/Users/vsevolodmartynov/repos/yappy/temp/merged_ordered_total.json',
            source_url_base='https://s3.ritm.media/hackaton-itmo/',
    ):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.ids = []
        self.texts = []
        self.embeddings_path = embeddings_path
        self.metadata_path = metadata_path
        self.source_json_path = source_json_path
        self.vectors = np.load(self.embeddings_path)
        self.vecs_norm = self.vectors / np.linalg.norm(self.vectors, axis=1, keepdims=True)
        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            self.meta = json.load(f)
        with open(self.source_json_path, 'r', encoding='utf-8') as f:
            self.source_data = json.load(f)
        self.source_by_filename = {item['filename']: item for item in self.source_data}
        self.source_url_base = source_url_base

    @staticmethod
    def build_faiss_index(vectors):
        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)
        return index

    def search_description(self, query_vector, top_k=10):
        desc_idxs = [i for i, m in enumerate(self.meta) if m['field'] == 'description']
        desc_vectors = self.vecs_norm[desc_idxs]
        index = self.build_faiss_index(desc_vectors)
        scores, top_ids = index.search(query_vector, top_k)
        results = []
        for score, idx in zip(scores[0], top_ids[0]):
            real_idx = desc_idxs[idx]
            m = self.meta[real_idx]
            description = self.source_by_filename[m['filename']].get('description', '[нет description]')
            results.append({
                'score': float(score),
                'id': m['id'],
                'filename': m['filename'],
                'description': description
            })
        return results

    def search_combined(self, query_vector, top_k=10):
        grouped = defaultdict(dict)
        for i, m in enumerate(self.meta):
            grouped[m['filename']][m['field']] = i

        combined_vectors = []
        combined_meta = []

        for filename, fields in grouped.items():
            if 'description' in fields and 'transcription' in fields:
                i1 = fields['description']
                i2 = fields['transcription']
                combined = self.vecs_norm[i1] + self.vecs_norm[i2]
                combined /= np.linalg.norm(combined)
                combined_vectors.append(combined)
                combined_meta.append({
                    'filename': filename,
                    'id': self.meta[i1]['id']
                })

        combined_vectors = np.vstack(combined_vectors)
        index = self.build_faiss_index(combined_vectors)
        scores, top_ids = index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], top_ids[0]):
            m = combined_meta[idx]
            description = self.source_by_filename[m['filename']].get('description', '[нет description]')
            results.append({
                'score': float(score),
                'id': m['id'],
                'filename': m['filename'],
                'description': description
            })
        return results

    def search_transcription(self, query_vector, top_k=10):
        trans_idxs = [i for i, m in enumerate(self.meta) if m['field'] == 'transcription']
        trans_vectors = self.vecs_norm[trans_idxs]
        index = self.build_faiss_index(trans_vectors)
        scores, top_ids = index.search(query_vector, top_k)
        results = []
        for score, idx in zip(scores[0], top_ids[0]):
            real_idx = trans_idxs[idx]
            m = self.meta[real_idx]
            description = self.source_by_filename[m['filename']].get('description', '[нет description]')
            transcription = self.source_by_filename[m['filename']].get('transcription', '[нет transcription]')
            results.append({
                'score': float(score),
                'id': m['id'],
                'filename': m['filename'],
                'description': description,
                'transcription': transcription
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
                combined_results.append({
                    'filename': filename,
                    'score': score_combined,
                    'score_description': score_desc,
                    'score_transcription': score_trans,
                    'description': self.source_by_filename[filename].get('description', '[Нет описания]'),
                    'transcription': self.source_by_filename[filename].get('transcription', '[Нет транскрипции]'),
                    'id': self.source_by_filename[filename]['id']
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
