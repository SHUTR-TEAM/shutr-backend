import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel
from django.conf import settings

# Initialize Vertex AI
PROJECT_ID = settings.GOOGLE_PROJECT_ID
REGION = settings.GOOGLE_REGION
vertexai.init(project=PROJECT_ID, location=REGION)

# Load multimodal embedding model
model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

DEPLOYED_INDEX_ID = settings.DEPLOYED_INDEX_ID
ENDPOINT = f"projects/{PROJECT_ID}/locations/{REGION}/indexEndpoints/{DEPLOYED_INDEX_ID}"

def search_similar_photos(search_query):
    """Find similar photos based on customer search input."""
    text_embedding = model.get_embeddings(text=search_query).text_embedding