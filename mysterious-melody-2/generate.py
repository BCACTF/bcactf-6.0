#!/usr/bin/env python3

import sys
import numpy as np
import wave

def ascii_to_hex(text):
    return text.encode('ascii').hex()

def hex_to_frequencies(hex_string):
    base_freq = 441.0
    semitone_ratio = 2 ** (1/12)
    
    hex_to_note = {
        '0': 0, '1': 1, '2': 2, '3': 3,
        '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, 'a': 10, 'b': 11,
        'c': 12, 'd': 13, 'e': 14, 'f': 15
    }
    
    frequencies = []
    for char in hex_string.lower():
        if char in hex_to_note:
            semitones = hex_to_note[char]
            freq = base_freq * (semitone_ratio ** semitones)
            frequencies.append(freq)
    
    return frequencies

def generate_wav(frequencies, output_file="audio.wav"):
    sample_rate = 44100
    tone_duration = 0.1
    samples_per_tone = int(sample_rate * tone_duration)
    
    audio_data = []
    
    for freq in frequencies:
        t = np.linspace(0, tone_duration, samples_per_tone, False)
        tone = np.sin(2 * np.pi * freq * t)
        
        # Apply fade in/out to reduce clicks
        fade_samples = int(0.01 * sample_rate)  # 10ms fade
        tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
        tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        audio_data.extend(tone)
    
    # Normalize and convert to 16-bit integers
    audio_data = np.array(audio_data)
    audio_data = np.int16(audio_data * 32767)
    
    # Write WAV file
    with wave.open(output_file, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def main():
    input_text = "Good job! You effectively were able to solve part one of the challenge. Please notice that at the beginning of the audio file, there is a short symphonic excerpt. Above it, some high frequency tones are playing. These tones play at three different frequencies in total. Please ignore all occurrences of the middle frequency; it is just noise. The rest can be decoded as binary."
    print(f"Input text: {input_text}")
    
    hex_string = ascii_to_hex(input_text)
    print(f"Hex representation: {hex_string}")
    
    frequencies = hex_to_frequencies(hex_string)
    print(f"Generated {len(frequencies)} tones")
    
    generate_wav(frequencies)
    print("Generated audio.wav")

if __name__ == "__main__":
    main()