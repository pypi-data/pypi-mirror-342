# test_protocol.py
from registry import Registry
from core import ProtocolEngine

def setup_engine():
    # Initialize with default prebuilt specialists
    registry = Registry()  # Automatically registers Transformers/Diffusers/etc.
    
    # Optional: Add custom tags if needed
    registry.AllowedTags.extend(["CodeGen"])  
    
    return ProtocolEngine(registry)

def test_specialists(engine):
    # LLM Test Prompts (will route to TransformersLLMExecutor)
    llm_prompts = [
        "Explain quantum computing to a 5-year-old",
        "Write a haiku about artificial intelligence"
    ]
    
    # Image Generation Prompts (will route to DiffusersImageGenExecutor)
    image_prompts = [
        "A cyberpunk cityscape at night, neon lights, 4k",
        "A realistic portrait of a dragon in medieval armor"
    ]
    
    print("=== Testing LLM Specialists ===")
    for prompt in llm_prompts:
        result = engine.Run(prompt)
        print(f"\nPrompt: {prompt}\nResponse: {result['Output'][:200]}...")
    
    print("\n=== Testing Image Generation Specialist ===")
    for prompt in image_prompts:
        result = engine.Run(prompt)
        print(f"\nPrompt: {prompt}\nResponse: {result['Output']}")

if __name__ == "__main__":
    engine = setup_engine()
    test_specialists(engine)