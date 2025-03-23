import vertexai
from vertexai.vision_models import Image, MultiModalEmbeddingModel
from django.conf import settings


# Initialize Vertex AI
PROJECT_ID= settings.GOOGLE_PROJECT_ID
REGION= settings.GOOGLE_REGION
vertexai.init(project=PROJECT_ID, location=REGION)

# TODO(developer): Try different dimenions: 128, 256, 512, 1408
embedding_dimention= 1408

model= MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

INDEX_ID= ""
ENDPOINT= f"projects/{PROJECT_ID}/locations/{REGION}/index/{INDEX_ID}"

def genarate_image_embedding(image_path):
    """genareate embedding for images"""
    image= Image.load_from_file(image_path)
    embeddings= model.get_embeddings(image=image).image_embedding
    return embeddings