#!/usr/bin/env python3
"""
Simple script to test the Blog API endpoints
"""
import requests
import json

def test_get_posts():
    """Test the GET /api/posts endpoint"""
    try:
        print("Testing GET /api/posts endpoint...")
        response = requests.get('http://localhost:5002/api/posts')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json()
            print("✅ Success! Retrieved posts:")
            print(json.dumps(posts, indent=2))
            print(f"Number of posts: {len(posts)}")
        else:
            print("❌ Failed to retrieve posts")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_get_posts()