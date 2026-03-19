# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import random
import pickle
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from pathlib import Path
from music21 import note, chord, converter
from tensorflow.keras import layers, Model, Sequential, Input
from tensorflow.keras.layers import LSTM, Bidirectional, Dense, LeakyReLU, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy

# Hyperparameters
SEQUENCE_LENGTH = 100
LATENT_DIM = 1000
BATCH_SIZE = 16
EPOCHS = 100
SAMPLE_INTERVAL = 1
LEARNING_RATE = 0.0002
BETA_1 = 0.5
OUTPUT_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/GAN").expanduser()
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Metrics
disc_loss = []
gen_loss = []
disc_acc = []

def get_notes(sampled_files):
    
    # Extract chords and notes from sampled MIDI files
    notes = []

    total_files = len(sampled_files)
    for idx, file in enumerate(sampled_files):
        try:
            midi = converter.parse(file)
            file_name = file.name  
            remaining_files = total_files - idx
            print(f"Parsing {file_name}... {remaining_files} files left.")

            notes_to_parse = midi.flatten().notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Error parsing {file}: {e}")

    return notes

def prepare_sequences(notes, n_vocab, sequence_length=100):
    
    # Get all the unique pitch names
    unique_pitches = sorted(set(notes))

    # Create a dictionary to map pitches to integers
    note_to_int = {note: number for number, note in enumerate(unique_pitches)}

    network_input = []
    network_output = []

    # Create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[note] for note in sequence_in])
        network_output.append(note_to_int[sequence_out])

    # Handle case where notes are too few
    if not network_input:
        raise ValueError("Insufficient notes for the specified sequence length.")

    n_patterns = len(network_input)

    # Reshape the input into a format compatible with LSTM layers
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    
    # Normalize input between -1 and 1
    network_input = (network_input - float(n_vocab) / 2) / (float(n_vocab) / 2)
    
    # One-hot encode the output labels
    network_output = tf.keras.utils.to_categorical(network_output, num_classes=n_vocab)

    return network_input, network_output

# Generator
def build_generator(seq_shape):

    # Define the sequential model
    model = Sequential()

    # Input layer
    model.add(layers.Input(shape=(LATENT_DIM,)))

    # Hidden layers
    model.add(layers.Dense(256))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization(momentum=0.8))
    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization(momentum=0.8))
    model.add(layers.Dense(1024))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.BatchNormalization(momentum=0.8))

    # Output layer
    model.add(layers.Dense(np.prod(seq_shape), activation='tanh'))
    model.add(layers.Reshape(seq_shape))

    # Print model summary
    model.summary()

    # Define the input and output for the generator model
    noise = layers.Input(shape=(LATENT_DIM,))
    seq = model(noise)

    return Model(inputs=noise, outputs=seq, name="generator")

# Discriminator
def build_discriminator(seq_shape):
    
    # Define the sequential model
    model = Sequential()
    model.add(Input(shape=seq_shape))  
    model.add(LSTM(512, return_sequences=True))
    model.add(Bidirectional(LSTM(512)))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    
    # Adding Minibatch Discrimination
    model.add(Dense(100))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    
    # Show the model summary for debugging and clarity
    model.summary()

    # Wrap the Sequential model in the Functional API
    seq_input = Input(shape=seq_shape, name="input_layer")
    validity = model(seq_input)  # Pass the input through the Sequential model
    discriminator = Model(inputs=seq_input, outputs=validity, name="discriminator")

    # Return the Functional API model
    return discriminator

# GAN Training Loop
def train_gan(generator, discriminator, combined, X_train, patience=20, checkpoint_dir="checkpoints"):
    
    # Create checkpoint directory - to rollback weights if early termination occurs
    os.makedirs(checkpoint_dir, exist_ok=True)
    best_combined_loss = float("inf")  # To track the best combined generator + discriminator performance
    patience_counter = 0  # Counter to track epochs without improvement
    best_generator_weights = os.path.join(checkpoint_dir, "best_generator.weights.h5")
    best_discriminator_weights = os.path.join(checkpoint_dir, "best_discriminator.weights.h5")


    # Real and fake labels as tensors
    real_labels = tf.ones((BATCH_SIZE, 1))
    fake_labels = tf.zeros((BATCH_SIZE, 1))

    for epoch in range(EPOCHS):

        # Select a random batch of note sequences
        idx = np.random.randint(0, X_train.shape[0], BATCH_SIZE)
        real_seqs = X_train[idx]

        # Skip batches that don't match the batch size
        if real_seqs.shape[0] != BATCH_SIZE:
            print("Skipping batch due to incomplete data.")
            continue

        # Generate fake sequences
        noise = np.random.normal(0, 1, (BATCH_SIZE, LATENT_DIM))
        fake_seqs = generator(noise)
            
        # Train Discriminator
        discriminator.trainable = True
        d_loss_real = discriminator.train_on_batch(real_seqs, real_labels)
        d_loss_fake = discriminator.train_on_batch(fake_seqs, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # Train Generator
        discriminator.trainable = False
        noise = np.random.normal(0, 1, (BATCH_SIZE, LATENT_DIM))
        g_loss = combined.train_on_batch(noise, real_labels)

        # Monitor discriminator accuracy and combined loss
        current_accuracy = 100 * d_loss[1]  # Discriminator accuracy in percentage
        combined_loss = d_loss[0] + g_loss

        # Check for improvement
        if combined_loss < best_combined_loss:
            best_combined_loss = combined_loss
            patience_counter = 0  # Reset patience counter
            # Save the best weights
            generator.save_weights(best_generator_weights)
            discriminator.save_weights(best_discriminator_weights)
            print(f"Epoch {epoch}: New best combined loss: {combined_loss:.4f}")
        else:
            patience_counter += 1
            print(f"Epoch {epoch}: No improvement. Patience counter: {patience_counter}")

        # Early stopping condition
        if patience_counter >= patience:
            print(f"Early stopping triggered. Best combined loss: {best_combined_loss:.4f}")

            # Roll back to the best weights
            print("Restoring best weights...")
            generator.load_weights(best_generator_weights)
            discriminator.load_weights(best_discriminator_weights)
            break

        # Display Progress
        if epoch % SAMPLE_INTERVAL == 0:
            disc_loss.append(d_loss[0])
            gen_loss.append(g_loss)
            disc_acc.append(d_loss[1])
            print(f"{epoch} [D loss: {d_loss[0]:.4f}, acc.: {100 * d_loss[1]:.2f}%] [G loss: {g_loss:.4f}]")

    print("Training complete.")

def plot_metrics(disc_loss, gen_loss, disc_acc):
    """
    Plot GAN training metrics including loss and discriminator accuracy.
    """
    # Specify the path to the .otf font file (update with your specific font path)
    font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
    prop = fm.FontProperties(fname=font_path, size=12)

    # Define the image folder and file name
    image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4_v6")
    image_name = 'f04018.pdf'
    image_path = os.path.join(image_folder, image_name)

    # Create the directory if it doesn't exist
    os.makedirs(image_folder, exist_ok=True)

    # Plot generator and discriminator losses
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    plt.plot(disc_loss, color='gray', label='Discriminator Loss')
    plt.plot(gen_loss, color='black', label='Generator Loss')
    plt.title('GAN Loss per Epoch', fontproperties=prop)
    plt.xlabel('Epoch', fontproperties=prop)
    plt.ylabel('Loss', fontproperties=prop)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend(prop=prop)

    # Plot discriminator accuracy
    plt.subplot(1, 2, 2)
    plt.plot(disc_acc, color='black', label='Discriminator Accuracy')
    plt.title('Discriminator Accuracy per Epoch', fontproperties=prop)
    plt.xlabel('Epoch', fontproperties=prop)
    plt.ylabel('Accuracy', fontproperties=prop)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend(prop=prop)

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.show()

def save_notes(notes, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(notes, f)
    print(f"Notes saved to {file_path}")

def load_notes(file_path):
    with open(file_path, "rb") as f:
        notes = pickle.load(f)
    print(f"Notes loaded from {file_path}")
    return notes

# Main Function
if __name__ == "__main__":

    # Define the data folder and file name
    data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/maestro").expanduser()
    extracted_folder = data_folder / "maestro-v3.0.0"
    midi_files = list(extracted_folder.rglob("*.midi")) + list(extracted_folder.rglob("*.mid"))
    saved_notes_file = OUTPUT_FOLDER / "extracted_notes.pkl"

    # Option to parse all MIDI files or a sample
    parse_all = False  # Set to True to parse all MIDI files
    num_files_to_sample = 256  # Number of files to sample if parse_all is False

    if parse_all:
        sampled_files = midi_files
    else:
        sampled_files = random.sample(midi_files, min(num_files_to_sample, len(midi_files)))

    # Check if the notes file already exists
    if saved_notes_file.exists():
        notes = load_notes(saved_notes_file)
    else:
        # Extract notes from sampled files and save them
        notes = get_notes(sampled_files)
        save_notes(notes, saved_notes_file)

    # Prepare the data for training
    n_vocab = len(set(notes))
    X_train, y_train = prepare_sequences(notes, n_vocab, sequence_length=SEQUENCE_LENGTH)
    seq_shape = (SEQUENCE_LENGTH, 1)

    # Build GAN components
    discriminator = build_discriminator(seq_shape)
    discriminator.compile(optimizer=Adam(LEARNING_RATE, BETA_1), 
                      loss=BinaryCrossentropy(from_logits=False),
                      metrics=["accuracy"])

    generator = build_generator(seq_shape)

    # Freeze discriminator weights for GAN training
    discriminator.trainable = False

    # Input for the generator (latent space vector)
    noise_input = layers.Input(shape=(LATENT_DIM,), name="noise_input")

    # Generator output
    generated_seq = generator(noise_input)

    # Discriminator output
    validity = discriminator(generated_seq)

    # Combined GAN model (Generator + Discriminator)
    combined = Model(noise_input, validity, name="combined_gan")
    combined.compile(optimizer=Adam(LEARNING_RATE, BETA_1), loss=BinaryCrossentropy(from_logits=False))

    # Train GAN
    train_gan(generator, discriminator, combined, X_train)

    # Save Models
    generator.export(str(OUTPUT_FOLDER / "generator"))
    discriminator.export(str(OUTPUT_FOLDER / "discriminator"))
    combined.export(str(OUTPUT_FOLDER / "combined_gan"))
    print("GAN models saved.")

    # Plot GAN training metrics
    plot_metrics(disc_loss, gen_loss, disc_acc)
