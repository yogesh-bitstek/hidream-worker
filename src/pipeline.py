import torch
from transformers import PreTrainedTokenizerFast, LlamaForCausalLM
from diffusers import HiDreamImagePipeline

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_ID = "HiDream-ai/HiDream-I1-Full"  # or HiDream-ai/HiDream-I1-Fast
LLAMA_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"

def load_pipeline():
    print("Loading tokenizer & text encoder...")
    tokenizer_4 = PreTrainedTokenizerFast.from_pretrained(LLAMA_ID)
    text_encoder_4 = LlamaForCausalLM.from_pretrained(
        LLAMA_ID,
        output_hidden_states=True,
        output_attentions=True,
        torch_dtype=torch.bfloat16,
    )

    print("Loading HiDream pipeline...")
    pipe = HiDreamImagePipeline.from_pretrained(
        MODEL_ID,
        tokenizer_4=tokenizer_4,
        text_encoder_4=text_encoder_4,
        torch_dtype=torch.bfloat16,
    ).to(DEVICE)

    return pipe

# Load once at startup
pipe = load_pipeline()
