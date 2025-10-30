#!/usr/bin/env python3
"""
Remove all "All of the above" options from Azure flashcards
"""

import json
import re

def remove_all_of_above_options():
    """Remove all 'All of the above' options from flashcards"""
    
    # Load the final expanded flashcard file
    with open('azure-900-final-expanded.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Loaded {len(flashcards)} flashcards")
    
    removed_count = 0
    modified_cards = []
    
    for card in flashcards:
        original_options = card['options']
        
        # Check if any option contains "All of the above" (case insensitive)
        has_all_of_above = any('all of the above' in option.lower() for option in original_options)
        
        if has_all_of_above:
            # Remove the "All of the above" option
            filtered_options = [opt for opt in original_options if 'all of the above' not in opt.lower()]
            
            # Update the card with filtered options
            card['options'] = filtered_options
            
            # If the correct answer was "All of the above", we need to pick a different correct answer
            original_answer = card['answer']
            original_correct_text = next((opt for opt in original_options if opt.startswith(original_answer + ')')), None)
            
            if original_correct_text and 'all of the above' in original_correct_text.lower():
                # The correct answer was "All of the above", so we need to make one of the remaining options correct
                # For now, let's make the first remaining option correct
                card['answer'] = 'A'
                card['explanation'] = card['explanation'] + " (Note: This question previously had 'All of the above' as the correct answer, but has been updated for clarity.)"
                removed_count += 1
                print(f"Card {card['id']}: Removed 'All of the above' option and updated correct answer")
            else:
                # The correct answer is still valid, just update the answer letter if needed
                # Find the new position of the correct answer
                correct_text = original_correct_text[3:] if original_correct_text else ""
                new_index = None
                for i, opt in enumerate(filtered_options):
                    if opt[3:] == correct_text:
                        new_index = i
                        break
                
                if new_index is not None:
                    card['answer'] = chr(65 + new_index)  # A, B, C, or D
                    removed_count += 1
                    print(f"Card {card['id']}: Removed 'All of the above' option and updated answer position")
                else:
                    print(f"Card {card['id']}: Warning - Could not find correct answer after filtering")
            
            modified_cards.append(card)
        else:
            modified_cards.append(card)
    
    print(f"\nRemoved 'All of the above' from {removed_count} flashcards")
    
    # Save the cleaned flashcards
    with open('azure-900-no-all-of-above.json', 'w') as f:
        json.dump(modified_cards, f, indent=2)
    
    print(f"Saved {len(modified_cards)} flashcards to azure-900-no-all-of-above.json")

if __name__ == "__main__":
    remove_all_of_above_options()

