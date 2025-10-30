#!/usr/bin/env python3
"""
Combine both 45-question sets into one 90-question file
"""

import json

def combine_flashcard_sets():
    """Combine set1 and set2 into one 90-question file"""
    
    # Load both sets
    with open('azure-900-set1-45questions.json', 'r') as f:
        set1 = json.load(f)
    
    with open('azure-900-set2-45questions.json', 'r') as f:
        set2 = json.load(f)
    
    print(f"Set1: {len(set1)} questions")
    print(f"Set2: {len(set2)} questions")
    
    # Combine both sets
    combined = set1 + set2
    
    print(f"Combined: {len(combined)} questions")
    
    # Save combined file
    with open('azure-900-combined-90questions.json', 'w') as f:
        json.dump(combined, f, indent=2)
    
    print("✅ Saved combined 90-question file")
    
    # Verify explanations exist
    missing_explanations = 0
    for i, card in enumerate(combined):
        if not card.get('explanation') or card['explanation'].strip() == '':
            missing_explanations += 1
            print(f"Missing explanation for card {i+1}: {card['question'][:50]}...")
    
    print(f"Cards with explanations: {len(combined) - missing_explanations}/{len(combined)}")
    
    if missing_explanations == 0:
        print("✅ All cards have explanations!")
    else:
        print(f"⚠️ {missing_explanations} cards missing explanations")

if __name__ == "__main__":
    combine_flashcard_sets()
