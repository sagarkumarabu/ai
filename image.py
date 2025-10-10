#python
from diffusers import StableDiffusionPipeline
import torch

#Load pre-trained Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32  # Use float32 for CPU
).to("cpu")  # Use CPU instead of GPU

#Prompt to generate image
prompt = "a girl swimming in a pool, photorealistic"

#Generate image
image = pipe(prompt).images[0]

#Save image
image.save("output.png")

print("Image saved as output.png")
