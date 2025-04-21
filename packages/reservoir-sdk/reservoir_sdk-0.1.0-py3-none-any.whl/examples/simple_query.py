#!/usr/bin/env python
"""
Simple example script showing how to use the Reservoir SDK.
"""

from reservoir_sdk import ReservoirClient
import time
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
    
    # Set query parameters
    query_text = "People having a conversation"
    max_duration = 5.0
    min_confidence = 0.6
    
    print(f"Submitting query: '{query_text}'")
    
    # Submit the query
    try:
        result = client.query(
            query_text=query_text,
            max_duration_minutes=max_duration,
            min_confidence=min_confidence
        )
        
        job_id = result.get('job_id')
        result_url = result.get('result_url')
        
        if not job_id:
            print("Error: No job ID returned")
            sys.exit(1)
        
        print(f"Query submitted successfully!")
        print(f"Job ID: {job_id}")
        print(f"Results will be available at: {result_url}")
        
        # Wait for the query to complete
        print("\nChecking query status...")
        
        max_attempts = 10
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                status = client.get_query_status(job_id)
                current_status = status.get('status')
                
                print(f"Status: {current_status}")
                
                if current_status == "complete":
                    print(f"\nQuery complete! View results at: {result_url}")
                    break
                elif current_status == "error":
                    print(f"Error processing query: {status.get('message', 'Unknown error')}")
                    break
                    
                # Wait before checking again
                time.sleep(5)
                
            except Exception as e:
                print(f"Error checking status: {str(e)}")
                time.sleep(5)
        
        if attempts >= max_attempts:
            print("\nTimed out waiting for query to complete.")
            print(f"You can still check the results later at: {result_url}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 