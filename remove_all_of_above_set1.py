#!/usr/bin/env python3
"""
Remove ALL "All of the above" options from set1 flashcards
"""

import json

def remove_all_of_above_from_set1():
    """Remove all 'All of the above' options from set1"""
    
    # Load the set1 file
    with open('azure-900-set1-45questions.json', 'r') as f:
        flashcards = json.load(f)
    
    print(f"🔧 Removing ALL 'All of the above' options from {len(flashcards)} cards...")
    
    fixed_count = 0
    
    for card in flashcards:
        options = card['options']
        answer = card['answer']
        
        # Check if any option contains "All of the above"
        all_of_above_options = [opt for opt in options if "All of the above" in opt]
        
        if all_of_above_options:
            print(f"Card {card['id']}: Found 'All of the above' option")
            
            # Remove the "All of the above" option
            new_options = [opt for opt in options if "All of the above" not in opt]
            
            # If the answer was "All of the above", change it to the first remaining option
            if answer in ['A', 'B', 'C', 'D']:
                all_of_above_option = all_of_above_options[0]
                all_of_above_letter = all_of_above_option[0]  # Get the letter (A, B, C, or D)
                
                if answer == all_of_above_letter:
                    # The answer was "All of the above", change it to the first remaining option
                    card['answer'] = 'A'  # First remaining option
                    print(f"  Changed answer from {all_of_above_letter} to A")
                else:
                    # The answer was not "All of the above", adjust the letter if needed
                    # Find the new position of the original answer
                    original_answer_text = next(opt for opt in options if opt.startswith(answer + ')'))
                    original_text = original_answer_text[3:]  # Remove "A) " prefix
                    
                    # Find this text in the new options
                    for i, new_opt in enumerate(new_options):
                        if new_opt[3:] == original_text:
                            card['answer'] = chr(65 + i)  # A, B, C, or D
                            print(f"  Adjusted answer from {answer} to {card['answer']}")
                            break
            
            # Update the options
            card['options'] = new_options
            fixed_count += 1
            print(f"  Removed 'All of the above' option")
    
    print(f"\n✅ Fixed {fixed_count} cards")
    
    # Save the corrected flashcards
    with open('azure-900-set1-no-all-of-above.json', 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"✅ SAVED to azure-900-set1-no-all-of-above.json")
    
    # Verify no "All of the above" remain
    remaining = 0
    for card in flashcards:
        for opt in card['options']:
            if "All of the above" in opt:
                remaining += 1
                print(f"❌ Card {card['id']} still has 'All of the above'")
    
    if remaining == 0:
        print("✅ ALL 'All of the above' options removed!")
    else:
        print(f"❌ {remaining} 'All of the above' options still remain")

if __name__ == "__main__":
    remove_all_of_above_from_set1()

