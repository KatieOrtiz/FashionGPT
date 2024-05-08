from gradio_client import Client, file

# Assuming you have the gradio_client installed and set up.
client = Client("https://levihsu-ootdiffusion.hf.space/--replicas/eldt3/")

# Replace the URLs with your custom image URLs
custom_vton_img_url = '/Users/charitha/Documents/GitHub/FashionGPT/m.webp'
custom_garm_img_url = '/Users/charitha/Documents/GitHub/FashionGPT/g.jpeg'

result = client.predict(
    file(custom_vton_img_url),
    file(custom_garm_img_url),
    1,  # adjust if needed
    20,  # adjust if needed
    2,  # adjust if needed
    -1,  # adjust if needed
    api_name="/process_hd"
)

print(result)
