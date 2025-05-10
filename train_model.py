import os
import numpy as np
import cv2
from sklearn.preprocessing import LabelEncoder
from deepface import DeepFace
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

def load_images_from_folder(folder):
    images = []
    labels = []

    for subdir in os.listdir(folder):
        subdir_path = os.path.join(folder, subdir)
        if os.path.isdir(subdir_path):
            for img_name in os.listdir(subdir_path):
                img_path = os.path.join(subdir_path, img_name)
                if img_path.endswith('.jpg') or img_path.endswith('.png'):
                    try:
                        # Extract face embeddings using DeepFace
                        img = DeepFace.represent(img_path=img_path, model_name='VGG-Face', enforce_detection=False)
                        if img:
                            # Add the embedding of the image
                            images.append(img[0]['embedding'])
                            labels.append(subdir)  # Use the folder name as the label
                    except Exception as e:
                        print(f"Error processing image {img_path}: {e}")
    
    return np.array(images), labels

def train_model():
    dataset_path = 'dataset'  # Path to the dataset folder
    print("[+] Loading data...")
    images, labels = load_images_from_folder(dataset_path)

    # Check if any data was loaded
    if len(images) == 0 or len(labels) == 0:
        print("[!] No data for training.")
        return

    # Convert labels to numbers using LabelEncoder
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Split data into training and testing sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(images, labels_encoded, test_size=0.2, random_state=42)

    # Create a simple Keras model
    model = Sequential([
        Dense(512, input_dim=X_train.shape[1], activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(len(np.unique(labels_encoded)), activation='softmax')  # Number of classes (labels)
    ])

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    print("[+] Training the model...")
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    print("[+] Model trained successfully!")

    # Save the trained model
    model.save("face_recognition_model.h5")
    print("[+] The trained model has been saved.")

if __name__ == "__main__":
    train_model()