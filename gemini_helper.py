import json
import logging
import os
from google import genai
from google.genai import types
from pydantic import BaseModel

# Based on blueprint:python_gemini integration
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def generate_storybook(character_info: dict, uploaded_images: list) -> dict:
    """Generate a 10-page storybook with alternating images and text."""
    
    character_name = character_info.get('name', 'the character')
    character_age = character_info.get('age', '')
    character_interests = character_info.get('interests', '')
    story_theme = character_info.get('theme', '')
    art_style = character_info.get('art_style', 'anime art style')
    
    age_info = f", age {character_age}" if character_age else ""
    interests_info = f" who likes {character_interests}" if character_interests else ""
    theme_info = f" The story theme is: {story_theme}." if story_theme else ""
    
    image_context = ""
    if uploaded_images:
        image_context = " Use the uploaded photos as reference for how the character should look."
    
    story_prompt = f"""Create a 10-page children's storybook about {character_name}{age_info}{interests_info}.{theme_info}{image_context}

The storybook should have:
- 10 pages total
- Each odd page (1, 3, 5, 7, 9) should have a detailed visual scene description for image generation
- Each even page (2, 4, 6, 8, 10) should have the story text for that scene
- The story should be engaging, age-appropriate, and have a clear beginning, middle, and end

Return your response as a JSON array with this structure:
[
  {{"page": 1, "type": "image", "description": "Detailed scene description for image generation"}},
  {{"page": 2, "type": "text", "content": "Story text for this page"}},
  ...
]

Make the image descriptions very detailed, including the character's appearance, setting, mood, lighting, and specific actions happening in the scene. Use {art_style} for all images."""

    parts = []
    
    if uploaded_images:
        for img_bytes in uploaded_images:
            parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))
    
    parts.append(story_prompt)
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=parts,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    if response.text:
        pages = json.loads(response.text)
        return {"pages": pages}
    
    return {"pages": []}


def generate_storybook_image(description: str, page_number: int, output_path: str) -> bool:
    """Generate an image for a storybook page using Gemini."""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=description,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        if not response.candidates:
            return False
        
        content = response.candidates[0].content
        if not content or not content.parts:
            return False
        
        for part in content.parts:
            if part.inline_data and part.inline_data.data:
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)
                print(f"Image generated for page {page_number}: {output_path}")
                return True
        
        return False
    except Exception as e:
        print(f"Error generating image for page {page_number}: {e}")
        return False
