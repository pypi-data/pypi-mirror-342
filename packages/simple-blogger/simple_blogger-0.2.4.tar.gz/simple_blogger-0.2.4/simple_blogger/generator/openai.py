from simple_blogger.generator import File, TextGenerator, ImageGenerator
from openai import OpenAI
from io import StringIO, BytesIO
import os, requests

class OpenAiTextGenerator(TextGenerator):
    def __init__(self, system_prompt, api_key_name ='OPENAI_API_KEY', model_name='chatgpt-4o-latest'):
        super().__init__(system_prompt=system_prompt)
        self.api_key = os.environ.get(api_key_name)
        self.model_name=model_name

    def generate(self, prompt, **_):
        client = OpenAI(api_key=self.api_key)
        text = client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        { "role": "system", "content": self.system_prompt },
                        { "role": "user", "content": prompt },
                    ]
                ).choices[0].message.content
        return File(self.ext(), StringIO(text))
    
class OpenAiImageGenerator(ImageGenerator):
    def __init__(self, api_key_name ='OPENAI_API_KEY', model_name='dall-e-3'):
        self.api_key = os.environ.get(api_key_name)
        self.model_name=model_name

    def generate(self, prompt, **_):
        client = OpenAI(api_key=self.api_key)
        image_url = client.images.generate(
            model = self.model_name,
            prompt = prompt,
            size = "1024x1024",
            quality = "standard",
            n = 1                
        ).data[0].url
        response = requests.get(image_url)
        return File(self.ext(), BytesIO(response.content))
    
    def ext(self):
        return 'png'