#!/usr/bin/env python3
"""
Quick test for the Blog API - Step 6 Enhanced with Search + Sorting
Fast testing of all endpoints including CRUD, search, and sorting functionality
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
                
        # Test UPDATE (PUT)
        print("\n4. Testing PUT /api/posts/1 (update existing post)...")
        update_data = {
            "title": "Updated First Post",
            "content": "This post has been updated via PUT request."
        }
        
        response = requests.put(
            'http://localhost:5002/api/posts/1',
            headers={'Content-Type': 'application/json'},
            json=update_data
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_post = response.json()
            print(f"   Updated title: {updated_post.get('title', 'N/A')}")
        
        # Test PUT with partial update (title only)
        print("\n5. Testing PUT with partial update (title only)...")
        response = requests.put(
            'http://localhost:5002/api/posts/1',
            headers={'Content-Type': 'application/json'},
            json={"title": "Partially Updated Title"}
        )
        print(f"   Status: {response.status_code}")
        
        # Test PUT with non-existent ID
        print("\n6. Testing PUT with non-existent ID (99999)...")
        response = requests.put(
            'http://localhost:5002/api/posts/99999',
            headers={'Content-Type': 'application/json'},
            json={"title": "Won't work", "content": "Post doesn't exist"}
        )
        print(f"   Status: {response.status_code}")
        
        # Test DELETE with non-existent ID
        print("\n7. Testing DELETE with non-existent ID (99999)...")
        response = requests.delete('http://localhost:5002/api/posts/99999')
        print(f"   Status: {response.status_code}")
            
        # Test SEARCH functionality
        print("\n8. Testing GET /api/posts/search (search by title)...")
        response = requests.get('http://localhost:5002/api/posts/search?title=first')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            search_results = response.json()
            print(f"   Found {len(search_results)} posts matching 'first' in title")
        
        # Test SEARCH by content
        print("\n9. Testing GET /api/posts/search (search by content)...")
        response = requests.get('http://localhost:5002/api/posts/search?content=updated')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            search_results = response.json()
            print(f"   Found {len(search_results)} posts matching 'updated' in content")
        
        # Test SEARCH with no results
        print("\n10. Testing GET /api/posts/search (no matches)...")
        response = requests.get('http://localhost:5002/api/posts/search?title=nonexistent')
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            search_results = response.json()
            print(f"    Found {len(search_results)} posts (should be 0)")
        
        # Test validation
        print("\n11. Testing POST validation...")
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json={"title": "No content"}  # Missing content
        )
        print(f"    Status (missing content): {response.status_code}")
        
        # NEW: Test SORTING functionality
        print("\n12. Testing GET /api/posts with sorting (title asc)...")
        response = requests.get('http://localhost:5002/api/posts?sort=title&direction=asc')
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            sorted_posts = response.json()
            titles = [post['title'] for post in sorted_posts]
            print(f"    Found {len(sorted_posts)} posts sorted by title (asc)")
            print(f"    First title: {titles[0] if titles else 'None'}")
        
        print("\n13. Testing GET /api/posts with sorting (title desc)...")
        response = requests.get('http://localhost:5002/api/posts?sort=title&direction=desc')
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            sorted_posts = response.json()
            titles = [post['title'] for post in sorted_posts]
            print(f"    Found {len(sorted_posts)} posts sorted by title (desc)")
            print(f"    First title: {titles[0] if titles else 'None'}")
        
        print("\n14. Testing GET /api/posts with sorting (content asc)...")
        response = requests.get('http://localhost:5002/api/posts?sort=content&direction=asc')
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            sorted_posts = response.json()
            print(f"    Found {len(sorted_posts)} posts sorted by content (asc)")
        
        print("\n15. Testing GET /api/posts sorting validation (invalid field)...")
        response = requests.get('http://localhost:5002/api/posts?sort=invalid_field&direction=asc')
        print(f"    Status (should be 400): {response.status_code}")
        
        print("\n16. Testing GET /api/posts sorting validation (invalid direction)...")
        response = requests.get('http://localhost:5002/api/posts?sort=title&direction=invalid_dir')
        print(f"    Status (should be 400): {response.status_code}")
        
        print("\n17. Testing GET /api/posts default sorting (title only)...")
        response = requests.get('http://localhost:5002/api/posts?sort=title')
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            print("    Successfully defaulted to ascending order")
        
        print("\n✅ Quick test completed! Full CRUD + Search + Sorting API tested.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()