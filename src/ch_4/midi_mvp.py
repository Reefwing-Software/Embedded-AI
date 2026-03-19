# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import pygame.midi

pygame.midi.init()

output_id = 2  # Replace with the correct ID
try:
    player = pygame.midi.Output(output_id)
    print(f"Successfully opened output device {output_id}.")
    # Play a simple MIDI note
    player.note_on(60, 127)  # Middle C
    pygame.time.wait(500)  # Play for 500ms
    player.note_off(60, 127)
except pygame.midi.MidiException as e:
    print(f"Failed to initialize MIDI Output: {e}")
finally:
    pygame.midi.quit()