import vertexai
from vertexai.vision_models import Image, MultiModalEmbeddingModel
from django.conf import settings
from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1.types import IndexDatapoint
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex
from django.http import JsonResponse




# Initialize Vertex AI
PROJECT_ID= settings.GOOGLE_PROJECT_ID
REGION= settings.GOOGLE_REGION
vertexai.init(project=PROJECT_ID, location=REGION)

# TODO(developer): Try different dimenions: 128, 256, 512, 1408
# embedding_dimention= 1408

# model= MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

INDEX_ID= settings.VECTOR_INDEX_ID
ENDPOINT= f"projects/{PROJECT_ID}/locations/{REGION}/indexes/{INDEX_ID}"

def genarate_image_embedding(image_path):
    # """genareate embedding for images"""
    # image= Image.load_from_file(image_path)
    # embeddings= model.get_embeddings(image=image).image_embedding
    # return embeddings
    return "embeddings"

def store_photo_embedding(photo_id, photographer_id, image_path):
    """Store image embedding in Vertex AI Matching Engine."""
    print("Generating image embedding...")
    # embedding = genarate_image_embedding(image_path)
    
    # index= MatchingEngineIndex(resource_name=ENDPOINT)
    
    # vector = IndexDatapoint(
    #     datapoint_id=str(photo_id),
    #     feature_vector=embedding,
    #     restricts=[{"namespace": "metadata", "allow": [str(photographer_id)]}]
    # )
    
    # # Upload embedding to Vertex AI Matching Engine
    # try:
    #     # Upload embedding to Vertex AI Matching Engine
    #     index.upsert(datapoints=[vector])
    #     return JsonResponse({"status": "success", "message": "Photo embedding stored successfully!"})
    # except Exception as e:
    #     return JsonResponse({"status": "error", "message": str(e)}, status=400)