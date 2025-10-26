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
            "title": "Quick Test Post for Deletion",
            "content": "This post will be deleted in the test."
        }
        
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json=new_post
        )
        print(f"   Status: {response.status_code}")
        created_id = None
        if response.status_code == 201:
            created_post = response.json()
            created_id = created_post.get('id')
            print(f"   Created post with ID: {created_id}")
        
        # Test DELETE
        if created_id:
            print(f"\n3. Testing DELETE /api/posts/{created_id}...")
            response = requests.delete(f'http://localhost:5002/api/posts/{created_id}')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                delete_response = response.json()
                print(f"   Message: {delete_response.get('message', 'No message')}")
                
        # Test DELETE with non-existent ID
        print("\n4. Testing DELETE with non-existent ID (99999)...")
        response = requests.delete('http://localhost:5002/api/posts/99999')
        print(f"   Status: {response.status_code}")
            
        # Test validation
        print("\n5. Testing POST validation...")
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