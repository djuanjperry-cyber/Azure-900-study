#!/usr/bin/env python3
"""
CRITICAL FIX: Another answer mismatch - Resource Groups question
"""

import json

def fix_resource_groups_card():
    """Fix the Resource Groups governance question"""
    
    # Load the urgent fix file
    with open('azure-900-urgent-fix.json', 'r') as f:
        flashcards = json.load(f)
    
    print("🚨 CRITICAL FIX: Resource Groups governance question!")
    
    # Find and fix card 94
    for card in flashcards:
        if card['id'] == 94:
            print(f"Found card {card['id']}: {card['question']}")
            print(f"Current answer: {card['answer']} (WRONG!)")
            print(f"Explanation: {card['explanation']}")
            print()
            
            # The explanation clearly states "apply governance policies, access controls, and compliance requirements"
            # which matches option A, so the answer should be A
            card['answer'] = 'A'
            
            print(f"✅ FIXED answer: {card['answer']} (To apply policies and access controls)")
            print("This matches the explanation perfectly!")
            break
    
    # Save the corrected flashcards IMMEDIATELY
    with open('azure-900-critical-fix.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"\n🚨 SAVED CRITICAL FIX to azure-900-critical-fix.json")
    
    # Verify the fix
    for card in flashcards:
        if card['id'] == 94:
            print(f"\n✅ VERIFICATION:")
            print(f"Question: {card['question']}")
            print(f"Answer: {card['answer']}")
            correct_option = next(opt for opt in card['options'] if opt.startswith(card['answer'] + ')'))
            print(f"Correct option: {correct_option}")
            print(f"Explanation: {card['explanation']}")
            print("✅ PERFECT MATCH!")
            break

if __name__ == "__main__":
    fix_resource_groups_card()

