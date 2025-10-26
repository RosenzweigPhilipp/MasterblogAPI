#!/usr/bin/env python3
"""
Quick test for the POST endpoint
"""
import requests
import json

def quick_test():
    try:
        # Test GET first
        print("1. Testing GET /api/posts...")
        response = requests.get('http://localhost:5002/api/posts')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            posts = response.json()
            print(f"   Found {len(posts)} posts")
            
        # Test POST
        print("\n2. Testing POST /api/posts...")
        new_post = {
            "title": "Quick Test Post",
            "content": "This is a test post."
        }
        
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json=new_post
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            created_post = response.json()
            print(f"   Created post with ID: {created_post.get('id')}")
            
        # Test validation
        print("\n3. Testing validation...")
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json={"title": "No content"}  # Missing content
        )
        print(f"   Status (missing content): {response.status_code}")
        
        print("\n✅ Quick test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()