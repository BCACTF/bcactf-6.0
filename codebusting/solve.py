#!/usr/bin/env python3
from pwn import *
import json
import string
import unicodedata
import time
from collections import Counter

# Configure logging
context.log_level = 'debug'

# Load required files
def load_quotes():
    with open("quotes.txt", "r", encoding="utf-8") as f:
        return f.read().strip().split("\n")

def load_spanish_quotes():
    with open("spanish.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [p["Cita"][1:-1] for p in data["quotes"]]

def load_words():
    with open("words.txt", "r", encoding="utf-8") as f:
        return f.read().strip().split("\n")

quotes = load_quotes()
spanish_quotes = load_spanish_quotes()
words = load_words()

# Helper functions
def remove_accents_preserve_n(text):
    """Remove diacritics but preserve Ñ"""
    result = []
    for char in text:
        if char in ["Ñ", "ñ"]:
            result.append(char)
        else:
            normalized = unicodedata.normalize("NFD", char)
            without_accents = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
            result.append(without_accents)
    return "".join(result)

def create_structure_mask(text):
    """Create a mask where letters are replaced with X but spaces and punctuation remain"""
    return ''.join('X' if c.isalpha() else c for c in text)

def create_pattern_mask(text):
    """Create a pattern mask where each unique letter is numbered"""
    pattern = []
    char_map = {}
    next_id = 0
    
    for char in text:
        if char.isalpha():
            if char not in char_map:
                char_map[char] = next_id
                next_id += 1
            pattern.append(str(char_map[char]))
        else:
            pattern.append(char)
    
    return ''.join(pattern)

def find_structure_matches(ciphertext, quotes_list, strict=True):
    """Find quotes that match the structure of spaces and punctuation"""
    if not ciphertext.strip():
        return []
    
    cipher_mask = create_structure_mask(ciphertext)
    cipher_pattern = create_pattern_mask(ciphertext)
    cipher_len = len(ciphertext)
    
    exact_matches = []
    flexible_matches = []
    
    for quote in quotes_list:
        quote_upper = quote.upper()
        
        # Skip if length difference is too large
        if abs(len(quote_upper) - cipher_len) > (0 if strict else 3):
            continue
            
        # Create structure mask for quote
        quote_mask = create_structure_mask(quote_upper)
        
        # Strict matching if lengths are equal
        if len(quote_mask) == len(cipher_mask):
            # Exact structure match
            if quote_mask == cipher_mask:
                exact_matches.append(quote_upper)
            # Flexible structure match - allow punctuation differences
            elif sum(1 for a, b in zip(quote_mask, cipher_mask) if a != b) <= 3:
                flexible_matches.append(quote_upper)
            
    # If we have exact matches, return those
    if exact_matches:
        return exact_matches
    
    # If strict mode and no exact matches, return flexible matches if any
    if strict and flexible_matches:
        return flexible_matches
    
    # If still no matches or in flexible mode, try letter frequency patterns
    if not exact_matches and not flexible_matches or not strict:
        freq_matches = []
        for quote in quotes_list:
            quote_upper = quote.upper()
            
            # Skip if length difference is too large
            if abs(len(quote_upper) - cipher_len) > 5:
                continue
                
            # Compare word count and structure pattern
            cipher_words = len([w for w in ciphertext.split() if any(c.isalpha() for c in w)])
            quote_words = len([w for w in quote_upper.split() if any(c.isalpha() for c in w)])
            
            if abs(cipher_words - quote_words) <= 1:
                freq_matches.append(quote_upper)
                
        return freq_matches[:10]  # Limit to top 10 frequency matches
    
    return flexible_matches

def find_spanish_structure_matches(ciphertext, quotes_list, strict=True):
    """Find Spanish quotes that match the structure"""
    cipher_mask = create_structure_mask(ciphertext)
    cipher_len = len(ciphertext)
    
    exact_matches = []
    flexible_matches = []
    
    for quote in quotes_list:
        normalized = remove_accents_preserve_n(quote).upper()
        
        # Skip if length difference is too large
        if abs(len(normalized) - cipher_len) > (2 if strict else 4):
            continue
            
        # Create structure mask
        quote_mask = create_structure_mask(normalized)
        
        if len(quote_mask) == len(cipher_mask):
            # Exact structure match
            if quote_mask == cipher_mask:
                exact_matches.append(normalized)
            # Flexible structure match
            elif sum(1 for a, b in zip(quote_mask, cipher_mask) if a != b) <= 3:
                flexible_matches.append(normalized)
    
    if exact_matches:
        return exact_matches
    elif flexible_matches or strict:
        return flexible_matches
    
    # Fallback to more relaxed matching
    freq_matches = []
    for quote in quotes_list:
        normalized = remove_accents_preserve_n(quote).upper()
        
        # Skip if length difference is too large
        if abs(len(normalized) - cipher_len) > 8:
            continue
            
        # Compare word count
        cipher_words = len([w for w in ciphertext.split() if any(c.isalpha() for c in w)])
        quote_words = len([w for w in normalized.split() if any(c.isalpha() for c in w)])
        
        if abs(cipher_words - quote_words) <= 1:
            freq_matches.append(normalized)
            
    return freq_matches[:10]

def is_caesar_possible(ciphertext, plaintext):
    """Check if ciphertext could be a Caesar shift of plaintext"""
    shifts = set()
    
    for c, p in zip(ciphertext, plaintext):
        if c.isalpha() and p.isalpha():
            shift = (ord(c) - ord(p)) % 26
            shifts.add(shift)
            if len(shifts) > 1:
                return False
    
    return True if shifts else False

def extract_ciphertext(data):
    """Extract ciphertext from server response"""
    if "Ciphertext" in data and ":" in data:
        # Split by "Ciphertext" and take the last part
        parts = data.split("Ciphertext")
        last_part = parts[-1]
        # Split by ":" and take everything after it
        ciphertext = last_part.split(":", 1)[1].strip()
        # If "Your answer:" is in the ciphertext, split it out
        if "Your answer:" in ciphertext:
            ciphertext = ciphertext.split("Your answer:")[0].strip()
        return ciphertext
    return None

# Main solver function
def solve_challenge():
    conn = remote('challs.bcactf.com', 23701)
    
    # Question types based on server code
    question_types = [
        "1 2", "1 1", "1 0", "1 1", "2 1", "2 2", "2 1", "2 0",
        "4 D", "4 E", "4 D", "4 E", "5 C", "8 1", "8 1", "8 1"
    ]
    
    # Skip welcome messages
    conn.recvuntil(b"Note: Answers are accepted with up to 2 character errors.\n")
    
    # Initialize next_ciphertext to None
    next_ciphertext = None
    next_challenge_number = 1
    
    for i in range(len(question_types) + 1):  # +1 because server sends 17 challenges
        try:
            # If we already have the next ciphertext from previous loop, use it
            # Otherwise receive a new one
            if next_ciphertext:
                ciphertext = next_ciphertext
                next_ciphertext = None
                # Wait for the "Your answer:" prompt
                conn.recvuntil(b"Your answer: ")
            else:
                # Wait for the ciphertext prompt
                data = conn.recvuntil(b"Your answer: ").decode()
                ciphertext = extract_ciphertext(data)
                if not ciphertext:
                    log.error(f"Couldn't parse ciphertext from: {data}")
                    break
            
            log.info(f"Challenge {next_challenge_number}: {ciphertext}")
            next_challenge_number += 1
            
            # Determine question type
            if i == 0:
                question_type = "1 1"  # Initial question
            else:
                question_type = question_types[i-1]
            
            # Solve based on question type
            q_num = int(question_type.split(' ')[0])
            
            # Try strict matching first
            if q_num == 8:  # Xenocrypt (Spanish)
                potential_answers = find_spanish_structure_matches(ciphertext, spanish_quotes, strict=True)
            else:
                potential_answers = find_structure_matches(ciphertext, quotes, strict=True)
            
            # If no matches, try flexible matching
            if not potential_answers:
                log.info("No strict matches found, trying flexible matching...")
                if q_num == 8:
                    potential_answers = find_spanish_structure_matches(ciphertext, spanish_quotes, strict=False)
                else:
                    potential_answers = find_structure_matches(ciphertext, quotes, strict=False)
            
            # For Caesar cipher, refine matches if we have some
            if q_num == 4 and potential_answers and len(potential_answers) > 1:
                caesar_matches = []
                for answer in potential_answers:
                    if is_caesar_possible(ciphertext, answer):
                        caesar_matches.append(answer)
                if caesar_matches:
                    potential_answers = caesar_matches
            
            log.info(f"Found {len(potential_answers)} potential matches")
            
            # Let the user choose the answer or type their own
            if potential_answers:
                print("\nPotential answers:")
                for idx, answer in enumerate(potential_answers[:5]):  # Show top 5
                    print(f"{idx+1}. {answer}")
                print("0. Type your own answer")
                
                choice = input("Select an answer (1-5, or 0): ")
                if choice == "0":
                    answer = input("Enter your answer: ")
                else:
                    try:
                        answer = potential_answers[int(choice)-1]
                    except:
                        answer = input("Invalid choice. Enter your answer manually: ")
            else:
                print("No matches found. Please solve manually:")
                print(f"Ciphertext: {ciphertext}")
                answer = input("Enter your answer: ")
            
            # Send the answer
            conn.sendline(answer.encode())
            
            # Get the response - either the next challenge or the flag
            response = conn.recvline().decode().strip()
            log.info(f"Response: {response}")
            
            # Check if this is the flag
            if "flag" in response.lower():
                log.success(f"Flag: {response}")
                # Try to get any additional lines with the flag
                try:
                    while True:
                        additional = conn.recvline(timeout=1).decode().strip()
                        if additional:
                            log.info(f"Additional: {additional}")
                        else:
                            break
                except:
                    pass
                break
                
            # Check for incorrect answer
            if "incorrect" in response.lower():
                log.error("Answer was wrong!")
                break
            
            # Otherwise, this should be the next ciphertext
            next_ciphertext = extract_ciphertext(response)
            if not next_ciphertext:
                log.warning(f"Couldn't extract next ciphertext from: {response}")
                
        except EOFError:
            log.error("Connection closed unexpectedly")
            break
            
        except Exception as e:
            log.error(f"Error: {str(e)}")
            break
    
    conn.close()

if __name__ == "__main__":
    solve_challenge()
