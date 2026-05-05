/**
 * Copyright (c) 2026 David Such
 * 
 * This software is released under the MIT License.
 * https://opensource.org/licenses/MIT
 */

#define SEQUENCE_LENGTH 32  // Number of notes in the generated sequence
#define NUM_NOTES 12        // Total number of possible MIDI notes (C to B)
#define MIDI_BASE_NOTE 60   // Middle C (C4)

uint8_t markov_sequence[SEQUENCE_LENGTH]; // Global array to store the generated MIDI sequence

// Define the transition matrix for note transitions
const float transition_matrix[NUM_NOTES][NUM_NOTES] = {
    {0.05, 0.05, 0.15, 0.05, 0.15, 0.10, 0.05, 0.15, 0.05, 0.10, 0.05, 0.05},  // C
    {0.05, 0.10, 0.05, 0.15, 0.05, 0.10, 0.15, 0.05, 0.10, 0.05, 0.10, 0.05},  // C#
    {0.10, 0.05, 0.05, 0.15, 0.10, 0.05, 0.10, 0.15, 0.05, 0.10, 0.05, 0.05},  // D
    {0.05, 0.10, 0.05, 0.05, 0.15, 0.05, 0.10, 0.05, 0.10, 0.15, 0.10, 0.05},  // D#
    {0.10, 0.05, 0.10, 0.05, 0.05, 0.15, 0.05, 0.10, 0.05, 0.15, 0.05, 0.10},  // E
    {0.05, 0.10, 0.05, 0.10, 0.05, 0.05, 0.15, 0.05, 0.10, 0.05, 0.10, 0.15},  // F
    {0.10, 0.05, 0.15, 0.05, 0.10, 0.05, 0.10, 0.15, 0.05, 0.10, 0.05, 0.05},  // F#
    {0.05, 0.10, 0.05, 0.15, 0.10, 0.05, 0.10, 0.05, 0.15, 0.05, 0.10, 0.05},  // G
    {0.05, 0.10, 0.05, 0.10, 0.05, 0.15, 0.05, 0.10, 0.05, 0.05, 0.10, 0.15},  // G#
    {0.10, 0.05, 0.10, 0.05, 0.10, 0.05, 0.15, 0.05, 0.10, 0.10, 0.05, 0.10},  // A
    {0.05, 0.10, 0.05, 0.10, 0.15, 0.05, 0.10, 0.05, 0.10, 0.05, 0.05, 0.15},  // A#
    {0.05, 0.10, 0.05, 0.10, 0.05, 0.15, 0.05, 0.10, 0.10, 0.05, 0.15, 0.05}   // B
};

// Function to select the next note based on probabilities
uint8_t select_next_note(uint8_t current_note) {
    float rand_value = (float)rand() / RAND_MAX;
    float cumulative = 0.0;
    
    for (int i = 0; i < NUM_NOTES; i++) {
        cumulative += transition_matrix[current_note][i];
        if (rand_value < cumulative) {
            return MIDI_BASE_NOTE + i;
        }
    }
    return MIDI_BASE_NOTE; // Default to base note if no match
}

// Generate a MIDI sequence using Markov chains
void generate_markov_sequence(uint8_t start_note) {
    markov_sequence[0] = start_note;

    for (int i = 1; i < SEQUENCE_LENGTH; i++) {
        markov_sequence[i] = select_next_note(markov_sequence[i - 1] - MIDI_BASE_NOTE);
    }
}
