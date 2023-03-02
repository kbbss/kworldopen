



def makeImage(model_id,prompt):
    #!pip install --upgrade -qq git+https://github.com/huggingface/diffusers.git transformers accelerate scipy xformers
    from diffusers import StableDiffusionPipeline
    import torch
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(prompt).images[0]
    return image

def makeImagePipe(model_id):
    #!pip install --upgrade -qq git+https://github.com/huggingface/diffusers.git transformers accelerate scipy xformers
    from diffusers import StableDiffusionPipeline
    import torch
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.to("cuda")
    return pipe

def makeRandom(model_id):
    #!pip install --upgrade -qq git+https://github.com/huggingface/diffusers.git transformers accelerate scipy xformers
    from diffusers import StableDiffusionPipeline
    from ..klsworld.shapeword import randomText
    import torch
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    randomtext =randomText()
    print("randomtext",randomtext)
    image = pipe(randomtext).images[0]
    return image
