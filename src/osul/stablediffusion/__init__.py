



def makeImage(model_id,prompt):
    #!pip install --upgrade -qq git+https://github.com/huggingface/diffusers.git transformers accelerate scipy xformers

    from diffusers import StableDiffusionPipeline
    import torch

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(prompt).images[0]


    return image
