import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, MobileNetV2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from pathlib import Path
import shutil
import json

# Define path to your dataset
dataset_path = '/content/Myntra_extracted/Myntra 13th July/2022_downloaded_images'

# Load images
def load_images(img_folder):
    img_data_list = []
    img_names = []
    for img in os.listdir(img_folder):
        img_path = os.path.join(img_folder, img)
        if img_path.endswith('.jpg') or img_path.endswith('.png'):
            img = image.load_img(img_path, target_size=(224, 224))
            img_data = image.img_to_array(img)
            img_data = np.expand_dims(img_data, axis=0)
            img_data = preprocess_input(img_data)
            img_data_list.append(img_data)
            img_names.append(Path(img_path).stem)
    return np.vstack(img_data_list), img_names

img_data, img_names = load_images(dataset_path)

# Load pre-trained MobileNetV2 model + higher level layers
base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# Extract features
features = base_model.predict(img_data)

# Number of clusters (adjust as needed)
num_clusters = 10

# Apply KMeans clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(features)
labels = kmeans.labels_

# Create a dictionary to hold clusters
clusters = {i: [] for i in range(num_clusters)}

# Assign image names to clusters
for img_name, label in zip(img_names, labels):
    clusters[label].append(img_name)

# Create folders for each cluster and move images to the corresponding folders
output_folder = '/content/Myntra_extracted/Myntra 13th July/2022_clustered_images'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for cluster_id in clusters.keys():
    cluster_folder = os.path.join(output_folder, f'cluster_{cluster_id}')
    if not os.path.exists(cluster_folder):
        os.makedirs(cluster_folder)
    for img_name in clusters[cluster_id]:
        src_path = os.path.join(dataset_path, f"{img_name}.jpg")
        dest_path = os.path.join(cluster_folder, f"{img_name}.jpg")
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
        else:
            # Try with .png extension if .jpg is not found
            src_path_png = os.path.join(dataset_path, f"{img_name}.png")
            if os.path.exists(src_path_png):
                shutil.copy(src_path_png, dest_path)

# Print cluster details
for cluster_id, img_list in clusters.items():
    print(f"Cluster {cluster_id}: {len(img_list)} images")

def plot_images(cluster, img_folder, num_images=5):
    plt.figure(figsize=(10, 10))
    for i, img_name in enumerate(clusters[cluster][:num_images]):
        img_path = os.path.join(img_folder, f"{img_name}.jpg")
        img = image.load_img(img_path, target_size=(224, 224))
        plt.subplot(1, num_images, i+1)
        plt.imshow(img)
        plt.title(f"Cluster {cluster}")
        plt.axis('off')
    plt.show()

# Plot images from cluster 0
plot_images(0, os.path.join(output_folder, 'cluster_0'))

# Save clusters to a JSON file
with open('clusters.json', 'w') as f:
    json.dump(clusters, f)
