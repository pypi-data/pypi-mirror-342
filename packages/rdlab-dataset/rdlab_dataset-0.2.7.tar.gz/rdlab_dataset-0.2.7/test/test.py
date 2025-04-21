from rdlab_dataset.module import KhmerWordLoader, KhmerAddressLoader, KhmerSentencesLoader
from rdlab_dataset.module import TextArrayListImageGenerator

# Load data
khmerwordloaders = KhmerWordLoader()
khmeraddressloaders = KhmerAddressLoader()
khmersentencesloaders = KhmerSentencesLoader()

# Get data
word = khmerwordloaders.get_all_words()
address = khmeraddressloaders.get_all_addresses()
sentences = khmersentencesloaders.get_all_sentences()

# Combine into one array
combined_texts = word + address + sentences

# Optional: print or inspect
print(f"Total combined items: {len(combined_texts)}")
print("Amount of address is: ", len(address))

# Create the generator instance
text_image_gen = TextArrayListImageGenerator(
    customize_font=True,
    folder_limit=10,  # Number of image folders per outer folder (data_0_20, etc.)
    output_count=4,   # Number of images per text item
    num_threads=4
)

# Generate images from address list
text_image_gen.generate_images(
    text_list=address,
    font_folder="/home/vitoupro/code/rdlab-dataset/test_font"
)
