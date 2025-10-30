#!/usr/bin/env python3
"""
Fix answer consistency issues in Azure flashcards
"""

import json
import re

def fix_answer_consistency():
    """Fix answer consistency issues"""
    
    # Load the cleaned flashcard file
    with open('azure-900-no-all-of-above.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Loaded {len(flashcards)} flashcards")
    
    fixed_count = 0
    
    for card in flashcards:
        # Check if the answer matches the explanation
        answer_letter = card['answer']
        explanation = card['explanation'].lower()
        
        # Find the option that matches the explanation
        correct_option_text = None
        for option in card['options']:
            option_text = option[3:].lower()  # Remove "A) " prefix
            
            # Check if this option is mentioned in the explanation
            if any(word in explanation for word in option_text.split() if len(word) > 3):
                correct_option_text = option
                break
        
        # If we found a better match, update the answer
        if correct_option_text:
            new_answer_letter = correct_option_text[0]  # Get A, B, C, or D
            if new_answer_letter != answer_letter:
                print(f"Card {card['id']}: Fixed answer from {answer_letter} to {new_answer_letter}")
                card['answer'] = new_answer_letter
                fixed_count += 1
    
    print(f"\nFixed {fixed_count} answer consistency issues")
    
    # Save the corrected flashcards
    with open('azure-900-fixed-answers.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"Saved {len(flashcards)} flashcards to azure-900-fixed-answers.json")

if __name__ == "__main__":
    fix_answer_consistency()

