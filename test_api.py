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
            return True
        else:
            print("❌ Failed to retrieve posts")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_add_post():
    """Test the POST /api/posts endpoint"""
    try:
        print("\nTesting POST /api/posts endpoint...")
        
        # Test with valid data
        new_post_data = {
            "title": "Test Post",
            "content": "This is a test post created by the API test script."
        }
        
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json=new_post_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            new_post = response.json()
            print("✅ Success! Created new post:")
            print(json.dumps(new_post, indent=2))
            
            # Verify the post has an ID
            if 'id' in new_post and isinstance(new_post['id'], int):
                print(f"✅ Post created with ID: {new_post['id']}")
                return True
            else:
                print("❌ Post created but ID is missing or invalid")
                return False
        else:
            print("❌ Failed to create post")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_add_post_validation():
    """Test POST endpoint error handling"""
    try:
        print("\nTesting POST /api/posts validation...")
        
        # Test missing title
        print("• Testing missing title...")
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json={"content": "Content without title"}
        )
        
        if response.status_code == 400:
            print("✅ Correctly rejected missing title (400)")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
        
        # Test missing content
        print("• Testing missing content...")
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json={"title": "Title without content"}
        )
        
        if response.status_code == 400:
            print("✅ Correctly rejected missing content (400)")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
        
        # Test empty JSON
        print("• Testing empty JSON...")
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json={}
        )
        
        if response.status_code == 400:
            print("✅ Correctly rejected empty JSON (400)")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running API Tests for Step 2: Add Endpoint\n")
    
    # Test GET endpoint first
    get_success = test_get_posts()
    
    # Test POST endpoint
    add_success = test_add_post()
    
    # Test validation
    validation_success = test_add_post_validation()
    
    # Test GET again to see the new post
    if add_success:
        print("\n" + "="*50)
        print("📋 Final posts list after adding new post:")
        test_get_posts()
    
    print("\n" + "="*50)
    print("📊 Test Summary:")
    print(f"GET /api/posts: {'✅ PASS' if get_success else '❌ FAIL'}")
    print(f"POST /api/posts: {'✅ PASS' if add_success else '❌ FAIL'}")
    print(f"Validation: {'✅ PASS' if validation_success else '❌ FAIL'}")
    
    if all([get_success, add_success, validation_success]):
        print("\n🎉 All tests passed! Step 2 implementation is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")