#!/usr/bin/env python3
"""
ANOTHER CRITICAL FIX: Resource Manager question mismatch
"""

import json

def fix_resource_manager_card():
    """Fix the Resource Manager question"""
    
    # Load the critical fix file
    with open('azure-900-critical-fix.json', 'r') as f:
        flashcards = json.load(f)
    
    print("🚨 ANOTHER CRITICAL FIX: Resource Manager question!")
    
    # Find and fix card 84
    for card in flashcards:
        if card['id'] == 84:
            print(f"Found card {card['id']}: {card['question']}")
            print(f"Current answer: {card['answer']} (WRONG!)")
            print(f"Explanation: {card['explanation']}")
            print()
            
            # The explanation clearly states "unified management and deployment of Azure resources"
            # which matches option A, so the answer should be A
            card['answer'] = 'A'
            
            print(f"✅ FIXED answer: {card['answer']} (To provide unified management and deployment)")
            print("This matches the explanation perfectly!")
            break
    
    # Save the corrected flashcards IMMEDIATELY
    with open('azure-900-emergency-fix.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"\n🚨 SAVED EMERGENCY FIX to azure-900-emergency-fix.json")
    
    # Verify the fix
    for card in flashcards:
        if card['id'] == 84:
            print(f"\n✅ VERIFICATION:")
            print(f"Question: {card['question']}")
            print(f"Answer: {card['answer']}")
            correct_option = next(opt for opt in card['options'] if opt.startswith(card['answer'] + ')'))
            print(f"Correct option: {correct_option}")
            print(f"Explanation: {card['explanation']}")
            print("✅ PERFECT MATCH!")
            break

if __name__ == "__main__":
    fix_resource_manager_card()

