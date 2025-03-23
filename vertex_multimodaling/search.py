import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel
from django.conf import settings
from vertexai.preview.matching_engine import MatchingEngineIndexEndpoint

# Initialize Vertex AI
PROJECT_ID = settings.GOOGLE_PROJECT_ID
REGION = settings.GOOGLE_REGION
vertexai.init(project=PROJECT_ID, location=REGION)

# Load multimodal embedding model
model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

DEPLOYED_INDEX_ID = settings.DEPLOYED_INDEX_ID
ENDPOINT = f"projects/{PROJECT_ID}/locations/{REGION}/indexEndpoints/{DEPLOYED_INDEX_ID}"

def search_similar_photos(search_query, top_k=30 ):
    """Find similar photos based on customer search input."""
    text_embedding = model.get_embeddings(text=search_query).text_embedding
    index_client = MatchingEngineIndexEndpoint(endpoint_name=ENDPOINT)
    
    response = index_client.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[text_embedding],
        num_neighbors=top_k
    )
    
    photographers_ids = []
    for neighbor in response.nearest_neighbors[0].neighbors:
        metadata = neighbor.datapoint.datapoint_metadata
        photographer_id = metadata.get("photographer_id")
        photographers_ids.append(photographer_id)

    return photographers_ids