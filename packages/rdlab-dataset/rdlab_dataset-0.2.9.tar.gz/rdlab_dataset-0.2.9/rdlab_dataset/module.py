import gc
import io
import json
import os
import pickle
import random
import pkg_resources
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import List


class KhmerWordLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/wild_khmer_data.pkl')
        else:
            self.filepath = filepath
        self.words = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Word file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_words(self):
        return self.words

    def __len__(self):
        return len(self.words)

    def get_first_word(self):
        return self.words[0] if self.words else None

    def get_n_first_words(self, n=5):
        return self.words[:n]

    def find_word(self, word):
        return word in self.words

class KhmerCombinationLocationWord:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/khmer_location_combinations.pkl')
        else:
            self.filepath = filepath
        self.words = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Word file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all(self):
        return self.words

    def __len__(self):
        return len(self.words)

    def get_first_data(self):
        return self.words[0] if self.words else None

    def get_n_first_data(self, n=5):
        return self.words[:n]

    def find_word(self, word):
        return word in self.words

class KhmerAddressLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/address_kh_data.pkl')
        else:
            self.filepath = filepath
        self.addresses = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Address file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_addresses(self):
        return self.addresses

    def __len__(self):
        return len(self.addresses)

    def get_first_address(self):
        return self.addresses[0] if self.addresses else None

    def get_n_first_addresses(self, n=5):
        return self.addresses[:n]

    def find_address(self, address):
        return address in self.addresses


class KhmerSentencesLoader:
    def __init__(self, filepath=None):
        if filepath is None:
            self.filepath = pkg_resources.resource_filename('rdlab_dataset', 'data/wild_khmer_sentences.pkl')
        else:
            self.filepath = filepath
        self.sentences = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            print(f"Sentence file not found: {self.filepath}")
            return ["No Data Here!"]
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        return data if data else ["No Data Here!"]

    def get_all_sentences(self):
        return self.sentences

    def __len__(self):
        return len(self.sentences)

    def get_first_sentence(self):
        return self.sentences[0] if self.sentences else None

    def get_n_first_sentences(self, n=5):
        return self.sentences[:n]

    def find_sentence(self, sentence):
        return sentence in self.sentences


class ATextImageGenerator:
    def __init__(self, font_path="rdlab_dataset/font", background_path="rdlab_dataset/background", output_folder="generated_images", font_size=48, background_color=(255, 255, 255), text_color=(0, 0, 0), margin=20, customize_font=False):
        self.font_path = pkg_resources.resource_filename('rdlab_dataset', font_path)
        self.output_folder = output_folder
        self.background_path = pkg_resources.resource_filename('rdlab_dataset', background_path)
        self.font_size = font_size
        self.background_color = background_color
        self.text_color = text_color
        self.margin = margin
        self.customize_font = customize_font
        self.font = None

    def load_font(self, font_file=None):
        if font_file and os.path.isfile(font_file):
            self.font = ImageFont.truetype(font_file, self.font_size)
        else:
            default_fonts = [f for f in os.listdir(self.font_path) if f.lower().endswith(".ttf")]
            if not default_fonts:
                raise ValueError(f"No TTF font files found in {self.font_path}")
            default_font_path = os.path.join(self.font_path, default_fonts[0])
            self.font = ImageFont.truetype(default_font_path, self.font_size)

    def random_shift_text_left_right_0_to_10_pixels(self):
        return random.randint(0, 10)

    def random_rotate_sentence_minus_5_to_5_degree(self):
        return random.uniform(-3, 3)

    def add_noise(self, image):
        """Randomly apply one of five noise types with random moderate density."""
        noise_type = random.choice(['gaussian', 'salt_pepper', 'speckle', 'poisson', 'blur'])
        img_array = np.array(image)

        if noise_type == 'gaussian':
            mean = 0
            var = random.uniform(10, 30)
            sigma = var ** 0.5
            gaussian = np.random.normal(mean, sigma, img_array.shape)
            noisy_img = img_array + gaussian
            noisy_img = np.clip(noisy_img, 0, 255)
        
        elif noise_type == 'salt_pepper':
            amount = random.uniform(0.01, 0.05)
            noisy_img = np.copy(img_array)
            # Salt mode
            num_salt = np.ceil(amount * img_array.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img_array.shape]
            noisy_img[tuple(coords)] = 255
            # Pepper mode
            num_pepper = np.ceil(amount * img_array.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img_array.shape]
            noisy_img[tuple(coords)] = 0

        elif noise_type == 'speckle':
            speckle = np.random.randn(*img_array.shape)
            noisy_img = img_array + img_array * speckle * random.uniform(0.05, 0.15)
            noisy_img = np.clip(noisy_img, 0, 255)

        elif noise_type == 'poisson':
            vals = len(np.unique(img_array))
            vals = 2 ** np.ceil(np.log2(vals))
            noisy_img = np.random.poisson(img_array * vals) / float(vals)
            noisy_img = np.clip(noisy_img, 0, 255)

        elif noise_type == 'blur':
            # For blur we use PIL
            radius = random.uniform(1, 2)
            return image.filter(ImageFilter.GaussianBlur(radius))

        return Image.fromarray(noisy_img.astype(np.uint8))

    def generate_image(self, text, font_folder=None):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if self.customize_font and font_folder:
            font_files = [f for f in os.listdir(font_folder) if f.lower().endswith(".ttf")]
            if not font_files:
                raise ValueError(f"No TTF font files found in {font_folder}")
        else:
            font_folder = self.font_path
            font_files = [f for f in os.listdir(font_folder) if f.lower().endswith(".ttf")]
            if not font_files:
                raise ValueError(f"No TTF font files found in {font_folder}")

        background_files = [f for f in os.listdir(self.background_path) if f.lower().endswith(".jpg")]
        if not background_files:
            raise ValueError(f"No JPG background files found in {self.background_path}")

        for font_file in font_files:
            font_path = os.path.join(font_folder, font_file)
            self.load_font(font_path)

            for background_file in background_files:
                background_path = os.path.join(self.background_path, background_file)
                background_image = Image.open(background_path).convert('RGB')

                shift = self.random_shift_text_left_right_0_to_10_pixels()
                rotation = self.random_rotate_sentence_minus_5_to_5_degree()

                temp_image = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
                draw = ImageDraw.Draw(temp_image)

                bbox = draw.textbbox((0, 0), text, font=self.font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                image_width = text_width + self.margin * 2
                image_height = text_height + self.margin * 2

                text_layer = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 0))
                draw = ImageDraw.Draw(text_layer)

                text_x = self.margin + shift
                text_y = self.margin
                draw.text((text_x, text_y), text, font=self.font, fill=self.text_color+(255,))

                # Rotate the text layer
                rotated_text = text_layer.rotate(rotation, expand=True)

                # Resize background to match rotated text size
                bg_width, bg_height = rotated_text.size
                background = background_image.resize((bg_width, bg_height))

                # Composite text onto background
                combined = Image.alpha_composite(background.convert('RGBA'), rotated_text)

                # Randomly crop equally from top and bottom
                crop_amount = random.randint(5, 20)
                width, height = combined.size
                new_top = crop_amount
                new_bottom = height - crop_amount

                if new_bottom <= new_top:
                    cropped_image = combined
                else:
                    cropped_image = combined.crop((0, new_top, width, new_bottom))

                # Convert back to RGB and add random noise
                final_image = cropped_image.convert('RGB')
                final_image_with_noise = self.add_noise(final_image)

                font_name = os.path.splitext(font_file)[0]
                background_name = os.path.splitext(background_file)[0]
                output_filename = f"{font_name}_{background_name}_noisy_output_image.png"
                output_path = os.path.join(self.output_folder, output_filename)
                final_image_with_noise.save(output_path)
                print(f"Image saved to {output_path}")





class TextArrayListImageGenerator:
    def __init__(self, font_path="font", background_path="background", output_folder="generated_images",
                 font_size=48, background_color=(255, 255, 255), text_color=(0, 0, 0), margin=20,
                 customize_font=False, folder_limit=10, output_count=4, num_threads=2,
                 rotate_text=True):
        self.font_path = pkg_resources.resource_filename('rdlab_dataset', font_path)
        self.background_path = pkg_resources.resource_filename('rdlab_dataset', background_path)
        self.output_folder = output_folder
        self.font_size = font_size
        self.background_color = background_color
        self.text_color = text_color
        self.margin = margin
        self.customize_font = customize_font
        self.folder_limit = folder_limit
        self.output_count = output_count
        self.num_threads = num_threads
        self.rotate_text = rotate_text

    def add_noise(self, image):
        noise_type = random.choice(['gaussian', 'salt_pepper', 'speckle', 'poisson', 'blur'])
        img_array = np.array(image)

        if noise_type == 'gaussian':
            mean = 0
            var = random.uniform(10, 30)
            sigma = var ** 0.5
            gaussian = np.random.normal(mean, sigma, img_array.shape)
            noisy_img = np.clip(img_array + gaussian, 0, 255)
        elif noise_type == 'salt_pepper':
            amount = random.uniform(0.01, 0.05)
            noisy_img = np.copy(img_array)
            num_salt = np.ceil(amount * img_array.size * 0.5).astype(int)
            coords = [np.random.randint(0, i - 1, num_salt) for i in img_array.shape]
            noisy_img[tuple(coords)] = 255
            num_pepper = np.ceil(amount * img_array.size * 0.5).astype(int)
            coords = [np.random.randint(0, i - 1, num_pepper) for i in img_array.shape]
            noisy_img[tuple(coords)] = 0
        elif noise_type == 'speckle':
            speckle = np.random.randn(*img_array.shape)
            noisy_img = np.clip(img_array + img_array * speckle * random.uniform(0.05, 0.15), 0, 255)
        elif noise_type == 'poisson':
            vals = len(np.unique(img_array))
            vals = 2 ** np.ceil(np.log2(vals))
            noisy_img = np.clip(np.random.poisson(img_array * vals) / float(vals), 0, 255)
        elif noise_type == 'blur':
            return image.filter(ImageFilter.GaussianBlur(radius=random.uniform(1, 2)))

        return Image.fromarray(noisy_img.astype(np.uint8))

    def _generate_batch(self, text_batch: List[str], batch_index: int,
                        font_files, background_files, font_folder, save_as_pickle):

        range_start = batch_index * self.folder_limit
        range_end = range_start + self.folder_limit
        data_range = f"{range_start}_{range_end}"
        data_folder = os.path.join(self.output_folder, f"data_{data_range}")
        os.makedirs(data_folder, exist_ok=True)

        annotations = []
        pickle_data = [] if save_as_pickle else None

        for text in text_batch:
            timestamp = datetime.now().strftime("image_folder_date_%d_%m_%y_time_%H_%M_%S_%f")[:-3]
            batch_folder = os.path.join(data_folder, timestamp)
            os.makedirs(batch_folder, exist_ok=True)

            for _ in range(self.output_count):
                font_file = random.choice(font_files)
                background_file = random.choice(background_files)
                font_path = os.path.join(font_folder if self.customize_font and font_folder else self.font_path, font_file)

                # Dynamically size font
                temp_font_size = self.font_size
                while True:
                    temp_font = ImageFont.truetype(font_path, temp_font_size)
                    dummy_img = Image.new('RGB', (1, 1))
                    draw = ImageDraw.Draw(dummy_img)
                    bbox = draw.textbbox((0, 0), text, font=temp_font)
                    text_height = bbox[3] - bbox[1]
                    if text_height <= 60 or temp_font_size <= 10:
                        break
                    temp_font_size -= 1

                background_path = os.path.join(self.background_path, background_file)
                with Image.open(background_path).convert('RGB') as background_image:
                    text_width = bbox[2] - bbox[0]
                    img_w = text_width + 2 * self.margin
                    img_h = 60 + 2 * self.margin
                    text_layer = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 0))
                    draw = ImageDraw.Draw(text_layer)
                    draw.text((self.margin + random.randint(0, 10), self.margin), text, font=temp_font,
                              fill=self.text_color + (255,))

                    if self.rotate_text:
                        rotated_text = text_layer.rotate(random.uniform(-3, 3), expand=True)
                    else:
                        rotated_text = text_layer

                    resized_bg = background_image.resize(rotated_text.size)
                    final_image = Image.alpha_composite(resized_bg.convert('RGBA'), rotated_text)
                    cropped_image = final_image.crop((0, 5, final_image.width, final_image.height - 5)).convert('RGB')
                    noisy_image = self.add_noise(cropped_image)

                    ts = datetime.now().strftime("%d_%m_%y_%H_%M_%S_%f")[:-3]
                    fname = f"{os.path.splitext(font_file)[0]}_{os.path.splitext(background_file)[0]}_{ts}_noisy.png"
                    out_path = os.path.join(batch_folder, fname)
                    noisy_image.save(out_path)
                    print(f"[Batch {data_range}] Image saved to {out_path}")

                    annotations.append({'image_path': out_path.replace("\\", "/"), 'label': text})

                    if save_as_pickle:
                        b = io.BytesIO()
                        noisy_image.save(b, format='PNG')
                        pickle_data.append({'image': b.getvalue(), 'label': text, 'path': out_path.replace("\\", "/")})

                    # Manual memory cleanup
                    del draw, rotated_text, resized_bg, final_image, cropped_image, noisy_image
                    gc.collect()

        self._save_annotations_range(range_start, range_end, annotations, pickle_data, save_as_pickle)

    def generate_images(self, text_list, font_folder=None, save_as_pickle=False):
        font_files = [f for f in os.listdir(font_folder if self.customize_font and font_folder else self.font_path)
                      if f.lower().endswith(".ttf")]
        background_files = [f for f in os.listdir(self.background_path) if f.lower().endswith(".jpg")]

        batches = [
            text_list[i:i + self.folder_limit]
            for i in range(0, len(text_list), self.folder_limit)
        ]

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = []
            for idx, batch in enumerate(batches):
                futures.append(executor.submit(
                    self._generate_batch,
                    batch,
                    idx,
                    font_files,
                    background_files,
                    font_folder,
                    save_as_pickle
                ))
            for f in futures:
                f.result()

    def _save_annotations_range(self, start, end, annotations, pickle_data, save_as_pickle):
        data_range = f"{start}_{end}"
        folder = os.path.join(self.output_folder, f"data_{data_range}")
        if save_as_pickle and pickle_data is not None:
            with open(os.path.join(folder, f"annotations_{data_range}.pkl"), 'wb') as f:
                pickle.dump(pickle_data, f)
        else:
            with open(os.path.join(folder, f"annotations_{data_range}.txt"), 'w', encoding='utf-8') as f:
                for a in annotations:
                    f.write(f"{a['image_path']}\t{a['label']}\n")
        print(f"[Batch {data_range}] Annotations saved.")