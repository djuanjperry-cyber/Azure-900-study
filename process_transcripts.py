#!/usr/bin/env python3
"""
Azure 900 Transcript Processor
Processes VTT transcript files from John Savill's Azure 900 course to generate flashcards
"""

import os
import re
import json
from pathlib import Path

def clean_vtt_content(content):
    """Clean VTT content by removing timestamps and formatting"""
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip empty lines, timestamps, and WEBVTT header
        if not line or line.startswith('WEBVTT') or re.match(r'^\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+$', line):
            continue
        # Skip cue numbers
        if line.isdigit():
            continue
        # Remove HTML tags
        line = re.sub(r'<[^>]+>', '', line)
        cleaned_lines.append(line)
    
    return ' '.join(cleaned_lines)

def extract_key_concepts(text, video_title):
    """Extract key concepts from transcript text"""
    concepts = []
    
    # Define patterns for key concepts
    patterns = [
        r'([A-Z][^.!?]*\?)\s*([^.!?]*[.!?])',  # Questions and answers
        r'(Azure [A-Za-z\s]+)\s*is\s*([^.!?]*[.!?])',  # Azure service definitions
        r'(What is [^.!?]*[.!?])',  # What is questions
        r'(Which [^.!?]*[.!?])',  # Which questions
        r'(How [^.!?]*[.!?])',  # How questions
        r'(Benefits of [^.!?]*[.!?])',  # Benefits
        r'(Purpose of [^.!?]*[.!?])',  # Purpose
        r'(Functionality of [^.!?]*[.!?])',  # Functionality
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                concepts.append({
                    'question': match[0].strip(),
                    'context': match[1].strip(),
                    'source': video_title
                })
            else:
                concepts.append({
                    'question': match.strip(),
                    'context': '',
                    'source': video_title
                })
    
    return concepts

def generate_flashcard_from_concept(concept, flashcard_id):
    """Generate a flashcard from a concept"""
    question = concept['question']
    context = concept['context']
    source = concept['source']
    
    # Extract category from source
    category = "Azure Fundamentals"
    if "Cloud" in source:
        category = "Cloud Concepts"
    elif "Security" in source or "Defender" in source or "Key Vault" in source:
        category = "Security, Privacy, and Compliance"
    elif "Cost" in source or "Pricing" in source or "TCO" in source:
        category = "Azure Pricing and Support"
    elif "Virtual Machine" in source or "Storage" in source or "Network" in source:
        category = "Core Azure Services"
    
    # Generate options based on question type
    if "What is" in question:
        options = [
            f"A) {context[:50]}..." if context else "A) A cloud computing service",
            "B) A programming language",
            "C) An operating system",
            "D) A database management system"
        ]
        answer = "A"
    elif "Which" in question:
        options = [
            "A) Option 1",
            "B) Option 2", 
            "C) Option 3",
            "D) All of the above"
        ]
        answer = "D"
    elif "Benefits" in question:
        options = [
            "A) Scalability",
            "B) Cost reduction",
            "C) High availability",
            "D) All of the above"
        ]
        answer = "D"
    else:
        options = [
            "A) True",
            "B) False",
            "C) Partially true",
            "D) Not applicable"
        ]
        answer = "A"
    
    return {
        "id": flashcard_id,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": context if context else f"Based on {source}",
        "category": category,
        "source": source
    }

def process_transcript_file(file_path, start_id=1):
    """Process a single VTT transcript file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = clean_vtt_content(content)
        video_title = Path(file_path).stem.replace('.en', '')
        
        concepts = extract_key_concepts(cleaned_content, video_title)
        flashcards = []
        
        for i, concept in enumerate(concepts[:5]):  # Limit to 5 concepts per video
            flashcard = generate_flashcard_from_concept(concept, start_id + i)
            flashcards.append(flashcard)
        
        return flashcards
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def main():
    """Main function to process all transcript files"""
    vtt_files = [f for f in os.listdir('.') if f.endswith('.vtt')]
    all_flashcards = []
    current_id = 1
    
    print(f"Processing {len(vtt_files)} transcript files...")
    
    for i, vtt_file in enumerate(sorted(vtt_files), 1):
        print(f"Processing {i}/{len(vtt_files)}: {vtt_file}")
        flashcards = process_transcript_file(vtt_file, current_id)
        all_flashcards.extend(flashcards)
        current_id += len(flashcards)
    
    # Remove duplicates based on question text
    unique_flashcards = []
    seen_questions = set()
    
    for flashcard in all_flashcards:
        if flashcard['question'] not in seen_questions:
            unique_flashcards.append(flashcard)
            seen_questions.add(flashcard['question'])
    
    # Save to JSON file
    output_file = 'azure-900-transcript-flashcards.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_flashcards, f, indent=2, ensure_ascii=False)
    
    print(f"\nGenerated {len(unique_flashcards)} unique flashcards")
    print(f"Saved to {output_file}")
    
    # Print sample flashcards
    print("\nSample flashcards:")
    for i, flashcard in enumerate(unique_flashcards[:3]):
        print(f"\n{i+1}. {flashcard['question']}")
        print(f"   Category: {flashcard['category']}")
        print(f"   Source: {flashcard['source']}")

if __name__ == "__main__":
    main()
