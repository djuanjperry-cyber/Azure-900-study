#!/usr/bin/env python3
"""
Fix the ARM template card answer mismatch
"""

import json

def fix_arm_template_card():
    """Fix the ARM template card where answer doesn't match explanation"""
    
    # Load the final clean flashcard file
    with open('azure-900-final-clean.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Fixing ARM template card answer mismatch...\n")
    
    # Find and fix card 26
    for card in flashcards:
        if card['id'] == 26:
            print(f"Found card {card['id']}: {card['question']}")
            print(f"Current answer: {card['answer']}")
            print(f"Explanation: {card['explanation']}")
            print()
            
            # The explanation clearly states "ARM Templates enable Infrastructure as Code (IaC)"
            # which matches option A, so the answer should be A
            card['answer'] = 'A'
            
            print(f"Fixed answer: {card['answer']} (Infrastructure as Code)")
            break
    
    # Save the corrected flashcards
    with open('azure-900-corrected.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"\nSaved corrected flashcards to azure-900-corrected.json")
    
    # Verify the fix
    for card in flashcards:
        if card['id'] == 26:
            print(f"\nVerification:")
            print(f"Question: {card['question']}")
            print(f"Answer: {card['answer']}")
            print(f"Correct option: {next(opt for opt in card['options'] if opt.startswith(card['answer'] + ')'))}")
            print(f"Explanation: {card['explanation']}")
            break

if __name__ == "__main__":
    fix_arm_template_card()

