



def make(model_id,prompt):
    #!pip install --upgrade -qq git+https://github.com/huggingface/diffusers.git
    from diffusers import StableDiffusionPipeline
    import torch

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    image = pipe(prompt).images[0]
    print("image",image)

    return image
