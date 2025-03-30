import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel
from django.conf import settings
from google.cloud import aiplatform
from django.http import JsonResponse

# Initialize Vertex AI
PROJECT_ID = settings.GOOGLE_PROJECT_ID
REGION = settings.GOOGLE_REGION
# vertexai.init(project=PROJECT_ID, location=REGION)

# Load multimodal embedding model
# model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

INDEX_ID = settings.VECTOR_INDEX_ID
ENDPOINT = f"projects/{PROJECT_ID}/locations/{REGION}/indexEndpoints/{INDEX_ID}"

def generate_text_embedding(text, top_k=30):
    print("Generating text embedding...")
    # text_embedding = model.get_embeddings(text=text).text_embedding
    
    # index_client = aiplatform.gapic.MatchingEngineClient()
    # response = index_client.find_neighbors(
    #     deployed_index_id=INDEX_ID,
    #     queries=[text_embedding],
    #     num_neighbors=1000 #number of similar photos
    # )
    
    # # Set to track unique photographers
    # unique_photographers = set()
    

    # for neighbor in response.nearest_neighbors[0].neighbors:
    #     metadata = neighbor.datapoint.datapoint_metadata
    #     photographer_id = metadata.get("photographer_id")
        
    #     if photographer_id:
    #         unique_photographers.add(photographer_id)
        
    #     if len(unique_photographers) >= top_k:
    #         break

    # return list(unique_photographers), JsonResponse({"photographer_ids": list(unique_photographers)})
