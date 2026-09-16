import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleRAGEngine:
    """Simple open-source RAG engine for matching buyer leads with property listings."""
    def __init__(self, listings_df, leads_list):
        self.listings_df = listings_df
        self.leads = leads_list
        self._build_index()

    def _build_index(self):
        self.corpus = []
        self.corpus_metadata = []

        for idx, row in self.listings_df.iterrows():
            text = f"{row['title']} {row['zoning']} Cap Rate: {row['cap_rate']}% Price: ${row['price']} {row['description']}"
            self.corpus.append(text)
            self.corpus_metadata.append(row.to_dict())

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def search_properties(self, query, top_k=2):
        """Search top matching properties for a query."""
        if not query.strip():
            return self.listings_df.head(top_k).to_dict(orient='records')

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append(self.corpus_metadata[idx])
        return results

    def get_copilot_insights(self, lead_data, custom_query=""):
        """Returns clean, minimal buyer insights and matched properties."""
        search_prompt = f"{custom_query} {lead_data['preferred_zoning']} {lead_data['target_cap_rate']}".strip()
        matched_props = self.search_properties(search_prompt, top_k=2)

        return {
            "buyer_motivations": lead_data["latent_motivations"],
            "matched_properties": matched_props,
            "recommended_pitch": f"Highlight matching cap rate ({lead_data['target_cap_rate']}) and verified compliance for fast Q4 closing."
        }
