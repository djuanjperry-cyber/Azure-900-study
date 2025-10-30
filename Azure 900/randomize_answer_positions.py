#!/usr/bin/env python3
"""
Randomize answer positions for Azure flashcards to prevent memorizing answer letters
"""

import json
import random

def randomize_answer_positions():
    """Randomize the order of answer options for each flashcard"""
    
    # Load the final expanded flashcard file
    with open('azure-900-final-expanded.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Loaded {len(flashcards)} flashcards")
    
    # Analyze initial distribution
    initial_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for card in flashcards:
        if card['answer'] in initial_distribution:
            initial_distribution[card['answer']] += 1
    print(f"Initial distribution: {initial_distribution}")
    
    # Randomize answer positions for each card
    for card in flashcards:
        options = card['options']
        correct_answer_text = next(opt for opt in options if opt.startswith(card['answer'] + ')'))
        
        # Remove the 'A) ', 'B) ' prefixes for shuffling
        clean_options = [opt[3:] for opt in options]
        
        # Shuffle the options
        random.shuffle(clean_options)
        
        # Find the new index of the correct answer
        new_correct_index = clean_options.index(correct_answer_text[3:])
        
        # Assign new prefixes and update the answer
        new_options = []
        for i, opt_text in enumerate(clean_options):
            new_options.append(f"{chr(65 + i)}) {opt_text}")
        
        card['options'] = new_options
        card['answer'] = chr(65 + new_correct_index)
    
    # Analyze new distribution
    new_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for card in flashcards:
        if card['answer'] in new_distribution:
            new_distribution[card['answer']] += 1
    print(f"New distribution: {new_distribution}")
    
    # Save the randomized flashcards
    with open('azure-900-randomized-answers.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"Randomized {len(flashcards)} flashcards and saved to azure-900-randomized-answers.json")

if __name__ == "__main__":
    randomize_answer_positions()

