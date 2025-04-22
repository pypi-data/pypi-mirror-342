"""Wordlist management module for SpellWell."""
import os
import json
from pathlib import Path
from datetime import datetime


def ensure_wordlist_exists(file_path):
    """Create the wordlist file if it doesn't exist."""
    if not os.path.exists(file_path):
        Path(file_path).touch()


def add_word(word, file_path, sentence=None):
    """Add a word to the wordlist with an optional example sentence."""
    ensure_wordlist_exists(file_path)
    
    # Read existing words to avoid duplicates
    words_data = get_words_with_sentences(file_path)
    
    # Check if word already exists
    for existing_word, _ in words_data:
        if existing_word.lower() == word.lower():
            # If the word exists but we have a new sentence, update it
            if sentence:
                remove_word(word, file_path)
                break
            else:
                # Word exists and no new sentence, so don't add a duplicate
                return
    
    # Add the word with sentence if provided
    with open(file_path, 'a') as f:
        if sentence:
            f.write(f"{word}|{sentence}\n")
        else:
            f.write(f"{word}\n")


def remove_word(word, file_path):
    """Remove a word from the wordlist."""
    ensure_wordlist_exists(file_path)
    
    words_data = get_words_with_sentences(file_path)
    
    # Filter out the word to remove
    words_data = [(w, s) for w, s in words_data if w.lower() != word.lower()]
    
    # Write the filtered list back to the file
    with open(file_path, 'w') as f:
        for word, sentence in words_data:
            if sentence:
                f.write(f"{word}|{sentence}\n")
            else:
                f.write(f"{word}\n")


def get_words(file_path):
    """Get all words from the wordlist (without sentences)."""
    words_data = get_words_with_sentences(file_path)
    return [word for word, _ in words_data]


def get_words_with_sentences(file_path):
    """Get all words with their example sentences from the wordlist."""
    ensure_wordlist_exists(file_path)
    
    words_data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Split by pipe to separate word and sentence
            parts = line.split('|', 1)
            word = parts[0]
            sentence = parts[1] if len(parts) > 1 else None
            
            words_data.append((word, sentence))
    
    return words_data


def store_results(results, results_file):
    """Store practice results to a JSON file."""
    # Load existing results if any
    existing_results = []
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                existing_results = json.load(f)
        except json.JSONDecodeError:
            # If the file is corrupted, start fresh
            existing_results = []
    
    # Add timestamp to results
    timestamped_results = {
        "timestamp": datetime.now().isoformat(),
        "results": [
            {"word": word, "guess": guess, "correct": correct}
            for word, guess, correct in results
        ]
    }
    
    existing_results.append(timestamped_results)
    
    # Save results back to file
    with open(results_file, 'w') as f:
        json.dump(existing_results, f, indent=2)


def get_results(results_file):
    """Get all practice results."""
    if not os.path.exists(results_file):
        return []
    
    try:
        with open(results_file, 'r') as f:
            all_sessions = json.load(f)
        
        # Flatten all sessions into a single list of (word, guess, correct) tuples
        results = []
        for session in all_sessions:
            for result in session["results"]:
                results.append((result["word"], result["guess"], result["correct"]))
        return results
    except (json.JSONDecodeError, KeyError):
        # If there's an error parsing the file, return empty results
        return []