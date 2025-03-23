import vertexai
from vertexai.vision_models import Image, MultiModalEmbeddingModel
from django.conf import settings
from vertexai.preview.matching_engine import MatchingEngineIndex


# Initialize Vertex AI
PROJECT_ID= settings.GOOGLE_PROJECT_ID
REGION= settings.GOOGLE_REGION
vertexai.init(project=PROJECT_ID, location=REGION)

# TODO(developer): Try different dimenions: 128, 256, 512, 1408
embedding_dimention= 1408

model= MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

INDEX_ID= settings.VECTOR_INDEX_ID
ENDPOINT= f"projects/{PROJECT_ID}/locations/{REGION}/index/{INDEX_ID}"

def genarate_image_embedding(image_path):
    """genareate embedding for images"""
    image= Image.load_from_file(image_path)
    embeddings= model.get_embeddings(image=image).image_embedding
    return embeddings

def store_photo_embedding(photo_id, photographer_id, image_path):
    """Store image embedding in Vertex AI Matching Engine."""
    embedding = genarate_image_embedding(image_path)
    
    index= MatchingEngineIndex(index_name=ENDPOINT)
    
    vector = {
        "id": str(photo_id),
        "embedding": embedding,
        "metadata": {"photographer_id": str(photographer_id)}
    }
    
    # Upload embedding to Vertex AI Matching Engine
    index.upsert(datapoints=[vector]) 