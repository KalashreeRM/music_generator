import numpy as np
import pickle
from tensorflow.keras.models import load_model
from music21 import note, chord, stream

def generate():
    with open("notes.pkl", "rb") as f:
        notes = pickle.load(f)

    model = load_model("model.h5")

    seq_len = 100
    pitchnames = sorted(set(notes))
    note_to_int = {note: num for num, note in enumerate(pitchnames)}
    int_to_note = {num: note for note, num in note_to_int.items()}

    start = np.random.randint(0, len(notes) - seq_len)
    pattern = [note_to_int[note] for note in notes[start:start + seq_len]]
    prediction_output = []

    for _ in range(500):
        input_seq = np.reshape(pattern, (1, len(pattern), 1)) / float(len(pitchnames))
        prediction = model.predict(input_seq, verbose=0)
        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:]

    output_notes = []
    for pattern in prediction_output:
        if '.' in pattern:
            notes_in_chord = pattern.split('.')
            chord_notes = [note.Note(int(n)) for n in notes_in_chord]
            new_chord = chord.Chord(chord_notes)
            output_notes.append(new_chord)
        else:
            output_notes.append(note.Note(pattern))

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='output.mid')

if __name__ == "__main__":
    generate()
