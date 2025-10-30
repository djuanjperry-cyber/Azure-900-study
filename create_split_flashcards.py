#!/usr/bin/env python3
"""
Create additional Azure flashcards by splitting existing ones
"""

import json
import re

def create_split_flashcards():
    """Create new flashcards by splitting existing ones"""
    
    # Load the main flashcard file
    with open('azure-900-ultimate-randomized.json', 'r') as f:
        flashcards = json.load(f)
    
    new_flashcards = []
    current_id = len(flashcards) + 1
    
    # Define specific questions to split based on multiple concepts
    split_questions = [
        {
            'original_id': 1,
            'splits': [
                {
                    'question': 'What automatic scaling feature does Azure SQL Database provide?',
                    'answer': 'A',
                    'options': [
                        'A) Automatic scaling based on demand',
                        'B) Manual scaling only',
                        'C) Fixed capacity scaling',
                        'D) No scaling capabilities'
                    ],
                    'explanation': 'Azure SQL Database provides automatic scaling that adjusts compute and storage resources based on application demand without manual intervention.'
                },
                {
                    'question': 'What built-in security features does Azure SQL Database offer?',
                    'answer': 'A',
                    'options': [
                        'A) Built-in security and encryption',
                        'B) No security features',
                        'C) Third-party security only',
                        'D) Basic security only'
                    ],
                    'explanation': 'Azure SQL Database includes built-in security features such as encryption at rest and in transit, threat detection, and vulnerability assessment.'
                }
            ]
        },
        {
            'original_id': 6,
            'splits': [
                {
                    'question': 'What is the primary purpose of Azure Resource Groups for billing?',
                    'answer': 'A',
                    'options': [
                        'A) To group resources for consolidated billing',
                        'B) To separate billing by region',
                        'C) To create individual bills per resource',
                        'D) To eliminate billing entirely'
                    ],
                    'explanation': 'Azure Resource Groups allow you to group related resources together for consolidated billing, making it easier to track costs and manage expenses.'
                },
                {
                    'question': 'What is the primary purpose of Azure Resource Groups for governance?',
                    'answer': 'A',
                    'options': [
                        'A) To apply policies and access controls to grouped resources',
                        'B) To create separate governance per resource',
                        'C) To eliminate governance requirements',
                        'D) To bypass all governance policies'
                    ],
                    'explanation': 'Azure Resource Groups enable you to apply governance policies, access controls, and compliance requirements to all resources within the group.'
                }
            ]
        },
        {
            'original_id': 8,
            'splits': [
                {
                    'question': 'How do Azure Availability Zones provide fault tolerance?',
                    'answer': 'A',
                    'options': [
                        'A) By distributing resources across physically separate data centers',
                        'B) By using only one data center',
                        'C) By relying on backup systems only',
                        'D) By using virtual machines only'
                    ],
                    'explanation': 'Azure Availability Zones provide fault tolerance by distributing resources across physically separate data centers within the same region.'
                },
                {
                    'question': 'How do Azure Availability Zones provide high availability?',
                    'answer': 'A',
                    'options': [
                        'A) By ensuring 99.99% uptime SLA',
                        'B) By providing 95% uptime SLA',
                        'C) By offering no uptime guarantee',
                        'D) By providing 100% uptime SLA'
                    ],
                    'explanation': 'Azure Availability Zones provide high availability with a 99.99% uptime SLA by distributing workloads across multiple zones.'
                }
            ]
        }
    ]
    
    # Process each split question
    for split_question in split_questions:
        original_card = next((card for card in flashcards if card['id'] == split_question['original_id']), None)
        if not original_card:
            continue
            
        for split in split_question['splits']:
            new_card = {
                'id': current_id,
                'question': split['question'],
                'options': split['options'],
                'answer': split['answer'],
                'explanation': split['explanation'],
                'category': original_card['category'],
                'source': f"Split from original card {split_question['original_id']} + {original_card['source']}"
            }
            new_flashcards.append(new_card)
            current_id += 1
    
    # Add some additional common Azure service questions
    additional_questions = [
        {
            'question': 'What is Azure Blob Storage primarily used for?',
            'options': [
                'A) Storing unstructured data like images and videos',
                'B) Storing relational database data',
                'C) Storing only text files',
                'D) Storing only binary files'
            ],
            'answer': 'A',
            'explanation': 'Azure Blob Storage is designed for storing unstructured data such as images, videos, documents, and other binary files.',
            'category': 'Azure Architecture and Services',
            'source': 'Additional Azure Service Question'
        },
        {
            'question': 'What is Azure Table Storage designed for?',
            'options': [
                'A) Storing structured NoSQL data',
                'B) Storing relational database data',
                'C) Storing only JSON data',
                'D) Storing only XML data'
            ],
            'answer': 'A',
            'explanation': 'Azure Table Storage is a NoSQL data store designed for storing structured, non-relational data.',
            'category': 'Azure Architecture and Services',
            'source': 'Additional Azure Service Question'
        },
        {
            'question': 'What is Azure Queue Storage used for?',
            'options': [
                'A) Asynchronous messaging between application components',
                'B) Synchronous data transfer only',
                'C) Real-time data streaming',
                'D) Direct database connections'
            ],
            'answer': 'A',
            'explanation': 'Azure Queue Storage provides asynchronous messaging between application components, enabling reliable message delivery.',
            'category': 'Azure Architecture and Services',
            'source': 'Additional Azure Service Question'
        },
        {
            'question': 'What is Azure File Storage used for?',
            'options': [
                'A) Shared file access using SMB protocol',
                'B) Individual file storage only',
                'C) Database file storage',
                'D) Web page hosting'
            ],
            'answer': 'A',
            'explanation': 'Azure File Storage provides fully managed file shares in the cloud accessible via SMB protocol.',
            'category': 'Azure Architecture and Services',
            'source': 'Additional Azure Service Question'
        },
        {
            'question': 'What is Azure Disk Storage used for?',
            'options': [
                'A) Persistent storage for virtual machines',
                'B) Temporary storage only',
                'C) Network storage only',
                'D) Cloud storage only'
            ],
            'answer': 'A',
            'explanation': 'Azure Disk Storage provides persistent, high-performance storage for Azure virtual machines.',
            'category': 'Azure Architecture and Services',
            'source': 'Additional Azure Service Question'
        }
    ]
    
    # Add additional questions
    for question in additional_questions:
        new_card = {
            'id': current_id,
            'question': question['question'],
            'options': question['options'],
            'answer': question['answer'],
            'explanation': question['explanation'],
            'category': question['category'],
            'source': question['source']
        }
        new_flashcards.append(new_card)
        current_id += 1
    
    # Combine original flashcards with new ones
    all_flashcards = flashcards + new_flashcards
    
    # Save the expanded flashcard set
    with open('azure-900-expanded-flashcards.json', 'w') as f:
        json.dump(all_flashcards, f, indent=2)
    
    print(f"Created {len(new_flashcards)} new flashcards")
    print(f"Total flashcards: {len(all_flashcards)}")
    print("Saved to azure-900-expanded-flashcards.json")

if __name__ == "__main__":
    create_split_flashcards()

