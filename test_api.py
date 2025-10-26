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

def test_delete_post():
    """Test the DELETE /api/posts/<id> endpoint"""
    try:
        print("\nTesting DELETE /api/posts/<id> endpoint...")
        
        # First, create a post to delete
        print("• Creating a post to delete...")
        new_post_data = {
            "title": "Post to Delete",
            "content": "This post will be deleted during testing."
        }
        
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json=new_post_data
        )
        
        if response.status_code != 201:
            print("❌ Failed to create post for deletion test")
            return False
        
        created_post = response.json()
        post_id = created_post['id']
        print(f"✅ Created post with ID: {post_id}")
        
        # Now delete the post
        print(f"• Deleting post with ID: {post_id}...")
        response = requests.delete(f'http://localhost:5002/api/posts/{post_id}')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            delete_response = response.json()
            print("✅ Success! Post deleted:")
            print(json.dumps(delete_response, indent=2))
            
            # Verify the post is actually deleted by checking if it's still in the list
            print("• Verifying post is removed from list...")
            response = requests.get('http://localhost:5002/api/posts')
            if response.status_code == 200:
                posts = response.json()
                deleted_post_still_exists = any(post['id'] == post_id for post in posts)
                if not deleted_post_still_exists:
                    print(f"✅ Post with ID {post_id} successfully removed from list")
                    return True
                else:
                    print(f"❌ Post with ID {post_id} still exists in list")
                    return False
            else:
                print("❌ Failed to verify deletion")
                return False
        else:
            print("❌ Failed to delete post")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_delete_post_not_found():
    """Test DELETE endpoint with non-existent ID"""
    try:
        print("\nTesting DELETE /api/posts/<id> with non-existent ID...")
        
        # Try to delete a post with a very high ID that shouldn't exist
        non_existent_id = 99999
        response = requests.delete(f'http://localhost:5002/api/posts/{non_existent_id}')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 404:
            error_response = response.json()
            print("✅ Correctly returned 404 for non-existent post:")
            print(json.dumps(error_response, indent=2))
            return True
        else:
            print(f"❌ Expected 404, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running API Tests for Step 3: Add & Delete Endpoints\n")
    
    # Test GET endpoint first
    get_success = test_get_posts()
    
    # Test POST endpoint
    add_success = test_add_post()
    
    # Test POST validation
    validation_success = test_add_post_validation()
    
    # Test DELETE endpoint
    delete_success = test_delete_post()
    
    # Test DELETE with non-existent ID
    delete_not_found_success = test_delete_post_not_found()
    
    # Final GET to see remaining posts
    print("\n" + "="*50)
    print("📋 Final posts list after all operations:")
    test_get_posts()
    
    print("\n" + "="*50)
    print("📊 Test Summary:")
    print(f"GET /api/posts: {'✅ PASS' if get_success else '❌ FAIL'}")
    print(f"POST /api/posts: {'✅ PASS' if add_success else '❌ FAIL'}")
    print(f"POST Validation: {'✅ PASS' if validation_success else '❌ FAIL'}")
    print(f"DELETE /api/posts/<id>: {'✅ PASS' if delete_success else '❌ FAIL'}")
    print(f"DELETE 404 Error: {'✅ PASS' if delete_not_found_success else '❌ FAIL'}")
    
    all_tests_passed = all([get_success, add_success, validation_success, delete_success, delete_not_found_success])
    
    if all_tests_passed:
        print("\n🎉 All tests passed! Step 3 implementation is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")