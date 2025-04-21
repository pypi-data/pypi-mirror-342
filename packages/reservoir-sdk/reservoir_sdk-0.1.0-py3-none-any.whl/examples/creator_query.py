#!/usr/bin/env python
"""
Example script showing how to query videos from specific creators using the Reservoir SDK.
"""

from reservoir_sdk import ReservoirClient
import sys
import os


def main():
    # Get API key from environment or prompt
    api_key = os.environ.get("RESERVOIR_API_KEY")
    
    if not api_key:
        api_key = input("Enter your Reservoir API key: ")
        if not api_key:
            print("Error: API key is required")
            sys.exit(1)
    
    # Initialize the client with API key
    client = ReservoirClient(api_key=api_key)
    
    # Get list of available creators
    print("Fetching available creators...")
    try:
        creators = client.list_creators()
    except Exception as e:
        print(f"Error fetching creators: {str(e)}")
        sys.exit(1)
    
    if not creators:
        print("No creators found.")
        sys.exit(1)
    
    # Print creators
    print(f"Found {len(creators)} creators:")
    for i, creator in enumerate(creators):
        name = creator.get('full_name', 'Unnamed')
        creator_id = creator.get('id', 'unknown')
        print(f"{i+1}. {name} (ID: {creator_id})")
    
    # Select a creator (or you could prompt the user here)
    if len(creators) > 0:
        selected_creator = creators[0]
        creator_id = selected_creator.get('id')
        creator_name = selected_creator.get('full_name', 'Unnamed')
        
        print(f"\nSelected creator: {creator_name}")
        
        # Set query parameters
        query_text = "People laughing"
        
        print(f"Submitting query: '{query_text}' for creator: {creator_name}")
        
        # Submit the query
        try:
            result = client.query(
                query_text=query_text,
                max_duration_minutes=3.0,
                min_confidence=0.5,
                creators_ids=[creator_id]
            )
            
            job_id = result.get('job_id')
            result_url = result.get('result_url')
            
            if job_id:
                print(f"Query submitted successfully!")
                print(f"Job ID: {job_id}")
                print(f"Results will be available at: {result_url}")
            else:
                print("Error: No job ID returned")
        except Exception as e:
            print(f"Error submitting query: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main() 