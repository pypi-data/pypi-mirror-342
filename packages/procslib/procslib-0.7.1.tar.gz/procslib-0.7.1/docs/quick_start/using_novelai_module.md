# Using NovelAI Generate Module with Procslib

## Setup

1. Get a persistent token:

   - Go to https://novelai.net/stories
   - Open top left tab (user settings) → Account
   - Click "Get Persistent API Token"

2. Save the token securely in a toml file:

   ```
   [tokens]
   persistent = "pst-hbRh6XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```

3. Load and set the environment variable:

   ```python
   import os
   import toml
   
   cred_file = toml.load("../data/creds.toml")
   pst = cred_file['tokens']['persistent']
   os.environ["NOVELAI_TOKEN"] = pst
   ```

## Basic Usage

1. Import the model:

   ```python
   from procslib.model_builder import get_model
   
   # Get model from registry
   novelai = get_model("novelai")
   ```

2. Apply prompt templates:

   ```python
   from procslib.models.novelai_wrapper import apply_template
   
   V4_FULL_DEFAULT = {
       "prompt": "no text, best quality, very aesthetic, absurdres",
       "negative_prompt": "blurry, lowres, error, film grain, scan artifacts, worst quality, bad quality, jpeg artifacts, very displeasing, chromatic aberration, multiple views, logo, too many watermarks",
   }
   
   curr_prompt = "a beautiful landscape"
   
   prompt, neg = apply_template(prompt=curr_prompt, negative_prompt="", template=V4_FULL_DEFAULT)
   ```

3. Generate an image:

   ```python
   image = novelai.generate_image(
       prompt=prompt,
       negative_prompt=neg,
       seed=12345
   )
   ```

4. Save the generated image:

   - The generated will contain same metadata as the website, and can be imported to website as well.

   ```python
   image.save("generated_image.png")
   ```