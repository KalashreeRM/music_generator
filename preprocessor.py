import os
import pickle
from music21 import converter, instrument, note, chord

notes = []

midi_folder = "dataset/midi_files"
print(f"Reading MIDI files from: {midi_folder}")

# Loop through each MIDI file in the folder
for file in os.listdir(midi_folder):
    if file.endswith(".mid") or file.endswith(".midi"):
        path = os.path.join(midi_folder, file)
        print(f"Processing {path}")
        try:
            midi = converter.parse(path)

            parts = instrument.partitionByInstrument(midi)
            if parts:  # if instrument parts are found
                notes_to_parse = parts.parts[0].recurse()
            else:
                notes_to_parse = midi.flat.notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Error processing {file}: {e}")

# Save notes to a pickle file
with open("notes.pkl", "wb") as filepath:
    pickle.dump(notes, filepath)

print(f"✅ Saved {len(notes)} notes to notes.pkl")
