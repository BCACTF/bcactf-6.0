#!/usr/bin/env python3

import numpy as np
import wave
import random

def ascii_to_binary(text):
    binary_string = ""
    for char in text:
        binary_string += format(ord(char), '08b')
    return binary_string

def replace_ones_with_twos(binary_string):
    return binary_string.replace('1', '2')

def add_random_ones(modified_binary):
    result = ""
    for i, char in enumerate(modified_binary):
        result += char
        if i < len(modified_binary) - 1:  # Don't add after the last character
            if random.random() < 0.5:  # 50% chance
                result += '1'
    return result

def binary_to_frequencies(binary_string):
    freq_map = {
        '0': 1300.0,
        '1': 1400.0,
        '2': 1500.0
    }
    
    frequencies = []
    for char in binary_string:
        if char in freq_map:
            frequencies.append(freq_map[char])
    
    return frequencies

def generate_wav(frequencies, output_file="audio2.wav"):
    sample_rate = 44100
    tone_duration = 0.2  # 5 tones per second
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
    input_text = "Congrats on part two of the chall. The flag is the name of the chord at 6:39. As for which chord I am referring to, it is the most noticeable one out of the surrounding chords, played on the downbeat. If you are wondering about the format, some acceptable names of chords are: A, Cm, C7, Db7, Dmaj7, Gm7, G#, Bbm7. Don't do anything fancy! For example, write Cm7 instead of Eb/C."
    print(f"Input text: {input_text}")
    
    # Step 1: Convert to binary
    binary_string = ascii_to_binary(input_text)
    print(f"Binary representation: {binary_string}")
    
    # Step 2: Replace 1s with 2s
    modified_binary = replace_ones_with_twos(binary_string)
    print(f"After replacing 1s with 2s: {modified_binary}")
    
    # Step 3: Add random 1s between characters
    random.seed(42)  # For reproducible results
    final_binary = add_random_ones(modified_binary)
    print(f"After adding random 1s: {final_binary}")
    
    # Step 4: Convert to frequencies
    frequencies = binary_to_frequencies(final_binary)
    print(f"Generated {len(frequencies)} tones")
    
    # Step 5: Generate WAV file
    generate_wav(frequencies)
    print("Generated audio2.wav")

if __name__ == "__main__":
    main()