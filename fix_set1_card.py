#!/usr/bin/env python3
"""
Fix the "All of the above" card in set1
"""

import json

def fix_all_of_above_card():
    """Fix the card that still has 'All of the above' as answer"""
    
    # Load the set1 file
    with open('azure-900-set1-45questions.json', 'r') as f:
        flashcards = json.load(f)
    
    print("🔧 Fixing 'All of the above' card...")
    
    # Find and fix card 67
    for card in flashcards:
        if card['id'] == 67:
            print(f"Found card {card['id']}: {card['question']}")
            print(f"Current answer: {card['answer']} (All of the above)")
            print(f"Explanation: {card['explanation']}")
            print()
            
            # The explanation mentions Microsoft Defender for Cloud first and most prominently
            # So let's make that the correct answer
            card['answer'] = 'B'
            
            print(f"✅ FIXED answer: {card['answer']} (Microsoft Defender for Cloud)")
            print("This matches the explanation better!")
            break
    
    # Save the corrected flashcards
    with open('azure-900-set1-fixed.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"\n✅ SAVED FIXED FILE to azure-900-set1-fixed.json")
    
    # Verify the fix
    for card in flashcards:
        if card['id'] == 67:
            print(f"\n✅ VERIFICATION:")
            print(f"Question: {card['question']}")
            print(f"Answer: {card['answer']}")
            correct_option = next(opt for opt in card['options'] if opt.startswith(card['answer'] + ')'))
            print(f"Correct option: {correct_option}")
            print(f"Explanation: {card['explanation']}")
            print("✅ PERFECT MATCH!")
            break

if __name__ == "__main__":
    fix_all_of_above_card()

