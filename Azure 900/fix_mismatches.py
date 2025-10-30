#!/usr/bin/env python3
"""
Fix all answer-explanation mismatches
"""

import json

def fix_answer_mismatches():
    """Fix cards where answer doesn't match explanation"""
    
    # Load the corrected flashcard file
    with open('azure-900-corrected.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"Fixing answer-explanation mismatches...\n")
    
    fixes_made = 0
    
    for card in flashcards:
        card_id = card['id']
        question = card['question']
        options = card['options']
        answer = card['answer']
        explanation = card['explanation']
        
        # Get the correct answer text
        correct_option = next((opt for opt in options if opt.startswith(answer + ')')), None)
        if not correct_option:
            continue
            
        correct_text = correct_option[3:]  # Remove "A) " prefix
        
        # Check for specific mismatches
        explanation_lower = explanation.lower()
        correct_text_lower = correct_text.lower()
        
        # Fix Card 95: Explanation says "distributing resources across physically separate data centers"
        # but answer is "By using virtual machines only" - should be option A
        if card_id == 95:
            if "distributing resources across physically separate data centers" in explanation_lower:
                card['answer'] = 'A'
                print(f"Card {card_id}: Fixed answer D -> A (matches 'distributing resources across physically separate data centers')")
                fixes_made += 1
        
        # Check for other obvious mismatches
        if "infrastructure as code" in explanation_lower and "performance" in correct_text_lower:
            # Find the IaC option
            for i, opt in enumerate(options):
                if "infrastructure as code" in opt.lower():
                    card['answer'] = chr(65 + i)  # A, B, C, or D
                    print(f"Card {card_id}: Fixed answer to match IaC explanation")
                    fixes_made += 1
                    break
        
        if "performance" in explanation_lower and "infrastructure as code" in correct_text_lower:
            # Find the performance option
            for i, opt in enumerate(options):
                if "performance" in opt.lower():
                    card['answer'] = chr(65 + i)  # A, B, C, or D
                    print(f"Card {card_id}: Fixed answer to match performance explanation")
                    fixes_made += 1
                    break
    
    print(f"\nMade {fixes_made} fixes")
    
    # Save the corrected flashcards
    with open('azure-900-fully-corrected.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"Saved corrected flashcards to azure-900-fully-corrected.json")
    
    # Verify the fixes
    print(f"\nVerification:")
    for card in flashcards:
        if card['id'] == 95:
            print(f"Card {card['id']}: {card['question']}")
            print(f"Answer: {card['answer']}")
            correct_option = next(opt for opt in card['options'] if opt.startswith(card['answer'] + ')'))
            print(f"Correct option: {correct_option}")
            print(f"Explanation: {card['explanation']}")
            break

if __name__ == "__main__":
    fix_answer_mismatches()

