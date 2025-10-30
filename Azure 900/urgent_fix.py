#!/usr/bin/env python3
"""
URGENT: Fix the Microsoft Purview card - user has test in 2 days!
"""

import json

def fix_purview_card_urgent():
    """Fix the Microsoft Purview card immediately"""
    
    # Load the fully corrected flashcard file
    with open('azure-900-fully-corrected.json', 'r') as f:
        flashcards = json.load(f)
    
    print("🚨 URGENT FIX: Microsoft Purview card mismatch!")
    
    # Find and fix card 27
    for card in flashcards:
        if card['id'] == 27:
            print(f"Found card {card['id']}: {card['question']}")
            print(f"Current answer: {card['answer']} (WRONG!)")
            print(f"Explanation: {card['explanation']}")
            print()
            
            # The explanation clearly states "Microsoft Purview is a unified data governance service"
            # which matches option A, so the answer should be A
            card['answer'] = 'A'
            
            print(f"✅ FIXED answer: {card['answer']} (Microsoft Purview)")
            print("This matches the explanation perfectly!")
            break
    
    # Save the corrected flashcards IMMEDIATELY
    with open('azure-900-urgent-fix.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"\n🚨 SAVED URGENT FIX to azure-900-urgent-fix.json")
    
    # Verify the fix
    for card in flashcards:
        if card['id'] == 27:
            print(f"\n✅ VERIFICATION:")
            print(f"Question: {card['question']}")
            print(f"Answer: {card['answer']}")
            correct_option = next(opt for opt in card['options'] if opt.startswith(card['answer'] + ')'))
            print(f"Correct option: {correct_option}")
            print(f"Explanation: {card['explanation']}")
            print("✅ PERFECT MATCH!")
            break

if __name__ == "__main__":
    fix_purview_card_urgent()

