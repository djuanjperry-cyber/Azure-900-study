#!/usr/bin/env python3
import json
import random

def randomize_flashcard_answers(input_file, output_file):
    """Randomize the correct answer positions in flashcards"""
    
    # Load the flashcards
    with open(input_file, 'r') as f:
        flashcards = json.load(f)
    
    # Randomize each flashcard
    for flashcard in flashcards:
        # Get the current correct answer
        correct_answer = flashcard['answer']
        
        # Get all options without the letter prefix
        options = []
        for option in flashcard['options']:
            # Remove the letter prefix (A), B), C), D))
            option_text = option.split(') ', 1)[1] if ') ' in option else option[3:]
            options.append(option_text)
        
        # Find the correct option text
        correct_option_text = None
        for i, option in enumerate(flashcard['options']):
            if option.startswith(correct_answer + ')'):
                correct_option_text = option.split(') ', 1)[1] if ') ' in option else option[3:]
                break
        
        if correct_option_text is None:
            print(f"Warning: Could not find correct answer for question {flashcard['id']}")
            continue
        
        # Shuffle the options
        random.shuffle(options)
        
        # Find where the correct answer ended up
        new_correct_position = None
        for i, option in enumerate(options):
            if option == correct_option_text:
                new_correct_position = chr(ord('A') + i)
                break
        
        if new_correct_position is None:
            print(f"Warning: Could not find correct answer after shuffling for question {flashcard['id']}")
            continue
        
        # Update the flashcard
        flashcard['answer'] = new_correct_position
        flashcard['options'] = [f"{chr(ord('A') + i)}) {option}" for i, option in enumerate(options)]
    
    # Save the randomized flashcards
    with open(output_file, 'w') as f:
        json.dump(flashcards, f, indent=2)
    
    print(f"Randomized {len(flashcards)} flashcards and saved to {output_file}")
    
    # Show distribution of correct answers
    answer_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for flashcard in flashcards:
        answer_counts[flashcard['answer']] += 1
    
    print(f"Answer distribution: A={answer_counts['A']}, B={answer_counts['B']}, C={answer_counts['C']}, D={answer_counts['D']}")

if __name__ == "__main__":
    randomize_flashcard_answers('azure-900-all-materials-comprehensive.json', 'azure-900-randomized-comprehensive.json')
