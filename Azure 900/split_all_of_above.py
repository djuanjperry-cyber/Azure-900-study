#!/usr/bin/env python3
"""
Split Azure flashcards that have "All of the above" answers into individual service questions
"""

import json
import re

def split_all_of_above_flashcards():
    """Create individual flashcards for services mentioned in 'All of the above' answers"""
    
    # Load the expanded flashcard file
    with open('azure-900-expanded-flashcards.json', 'r') as f:
        flashcards = json.load(f)
    
    new_flashcards = []
    current_id = len(flashcards) + 1
    
    # Define specific "All of the above" questions to split
    split_questions = [
        {
            'original_question': 'Which Azure service provides comprehensive application performance monitoring and diagnostics?',
            'services': [
                {
                    'question': 'What does Azure Monitor provide for application monitoring?',
                    'answer': 'A',
                    'options': [
                        'A) Comprehensive monitoring and diagnostics platform',
                        'B) Only log analysis capabilities',
                        'C) Only performance metrics',
                        'D) Only alerting features'
                    ],
                    'explanation': 'Azure Monitor provides a comprehensive monitoring and diagnostics platform that collects, analyzes, and acts on telemetry data from Azure and on-premises environments.'
                },
                {
                    'question': 'What does Application Insights provide for application monitoring?',
                    'answer': 'A',
                    'options': [
                        'A) Application performance monitoring and diagnostics',
                        'B) Only infrastructure monitoring',
                        'C) Only security monitoring',
                        'D) Only cost monitoring'
                    ],
                    'explanation': 'Application Insights provides application performance monitoring (APM) and diagnostics for web applications, helping developers understand how their applications are performing.'
                },
                {
                    'question': 'What does Azure Log Analytics provide for application monitoring?',
                    'answer': 'A',
                    'options': [
                        'A) Log analysis and query capabilities',
                        'B) Only real-time monitoring',
                        'C) Only performance metrics',
                        'D) Only alerting features'
                    ],
                    'explanation': 'Azure Log Analytics provides log analysis and query capabilities, allowing you to search and analyze log data from various sources.'
                }
            ]
        },
        {
            'original_question': 'Which Azure service provides comprehensive hybrid cloud backup and disaster recovery?',
            'services': [
                {
                    'question': 'What does Azure Backup provide for hybrid environments?',
                    'answer': 'A',
                    'options': [
                        'A) Backup capabilities for hybrid cloud environments',
                        'B) Only on-premises backup',
                        'C) Only cloud backup',
                        'D) Only disaster recovery'
                    ],
                    'explanation': 'Azure Backup provides backup capabilities for hybrid cloud environments, protecting data across on-premises and cloud resources.'
                },
                {
                    'question': 'What does Azure Site Recovery provide for disaster recovery?',
                    'answer': 'A',
                    'options': [
                        'A) Disaster recovery and business continuity',
                        'B) Only backup services',
                        'C) Only data replication',
                        'D) Only monitoring services'
                    ],
                    'explanation': 'Azure Site Recovery provides disaster recovery and business continuity by replicating workloads to Azure and orchestrating failover processes.'
                },
                {
                    'question': 'What does Azure Archive Storage provide for long-term retention?',
                    'answer': 'A',
                    'options': [
                        'A) Long-term retention and cost-effective storage',
                        'B) Only real-time access storage',
                        'C) Only backup services',
                        'D) Only disaster recovery'
                    ],
                    'explanation': 'Azure Archive Storage provides long-term retention with cost-effective storage for data that is rarely accessed but needs to be retained for compliance or business requirements.'
                }
            ]
        }
    ]
    
    # Add additional individual service questions
    additional_questions = [
        {
            'question': 'What is the primary purpose of Azure Monitor?',
            'options': [
                'A) Comprehensive monitoring and diagnostics platform',
                'B) Only application performance monitoring',
                'C) Only log analysis',
                'D) Only alerting services'
            ],
            'answer': 'A',
            'explanation': 'Azure Monitor is a comprehensive monitoring and diagnostics platform that provides full-stack monitoring for applications, infrastructure, and networks.',
            'category': 'Azure Management and Governance',
            'source': 'Split from All of the Above Question'
        },
        {
            'question': 'What is the primary purpose of Application Insights?',
            'options': [
                'A) Application performance monitoring and diagnostics',
                'B) Infrastructure monitoring only',
                'C) Security monitoring only',
                'D) Cost monitoring only'
            ],
            'answer': 'A',
            'explanation': 'Application Insights is specifically designed for application performance monitoring (APM) and diagnostics, helping developers understand application behavior.',
            'category': 'Azure Management and Governance',
            'source': 'Split from All of the Above Question'
        },
        {
            'question': 'What is the primary purpose of Azure Log Analytics?',
            'options': [
                'A) Log analysis and query capabilities',
                'B) Real-time monitoring only',
                'C) Performance metrics only',
                'D) Alerting services only'
            ],
            'answer': 'A',
            'explanation': 'Azure Log Analytics provides log analysis and query capabilities, allowing you to search, analyze, and visualize log data from various sources.',
            'category': 'Azure Management and Governance',
            'source': 'Split from All of the Above Question'
        },
        {
            'question': 'What is the primary purpose of Azure Backup?',
            'options': [
                'A) Backup and data protection services',
                'B) Disaster recovery only',
                'C) Data replication only',
                'D) Monitoring services only'
            ],
            'answer': 'A',
            'explanation': 'Azure Backup provides backup and data protection services for Azure and on-premises resources, ensuring data is safely stored and recoverable.',
            'category': 'Azure Management and Governance',
            'source': 'Split from All of the Above Question'
        },
        {
            'question': 'What is the primary purpose of Azure Site Recovery?',
            'options': [
                'A) Disaster recovery and business continuity',
                'B) Backup services only',
                'C) Data replication only',
                'D) Monitoring services only'
            ],
            'answer': 'A',
            'explanation': 'Azure Site Recovery provides disaster recovery and business continuity by replicating workloads and orchestrating failover processes.',
            'category': 'Azure Management and Governance',
            'source': 'Split from All of the Above Question'
        },
        {
            'question': 'What is the primary purpose of Azure Archive Storage?',
            'options': [
                'A) Long-term retention and cost-effective storage',
                'B) Real-time access storage',
                'C) Backup services only',
                'D) Disaster recovery only'
            ],
            'answer': 'A',
            'explanation': 'Azure Archive Storage provides long-term retention with cost-effective storage for data that is rarely accessed but needs to be retained.',
            'category': 'Azure Architecture and Services',
            'source': 'Split from All of the Above Question'
        }
    ]
    
    # Add the additional questions
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
    with open('azure-900-final-expanded.json', 'w') as f:
        json.dump(all_flashcards, f, indent=2)
    
    print(f"Created {len(new_flashcards)} new flashcards")
    print(f"Total flashcards: {len(all_flashcards)}")
    print("Saved to azure-900-final-expanded.json")

if __name__ == "__main__":
    split_all_of_above_flashcards()

