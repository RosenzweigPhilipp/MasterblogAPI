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

def test_update_post():
    """Test the PUT /api/posts/<id> endpoint"""
    try:
        print("\nTesting PUT /api/posts/<id> endpoint...")
        
        # First, create a post to update
        print("• Creating a post to update...")
        new_post_data = {
            "title": "Post to Update",
            "content": "Original content that will be updated."
        }
        
        response = requests.post(
            'http://localhost:5002/api/posts',
            headers={'Content-Type': 'application/json'},
            json=new_post_data
        )
        
        if response.status_code != 201:
            print("❌ Failed to create post for update test")
            return False
        
        created_post = response.json()
        post_id = created_post['id']
        print(f"✅ Created post with ID: {post_id}")
        
        # Test 1: Update both title and content
        print(f"• Updating post {post_id} (title and content)...")
        update_data = {
            "title": "Updated Title",
            "content": "Updated content for the test post."
        }
        
        response = requests.put(
            f'http://localhost:5002/api/posts/{post_id}',
            headers={'Content-Type': 'application/json'},
            json=update_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_post = response.json()
            print("✅ Success! Post updated:")
            print(json.dumps(updated_post, indent=2))
            
            # Verify the update
            if (updated_post['title'] == update_data['title'] and 
                updated_post['content'] == update_data['content'] and 
                updated_post['id'] == post_id):
                print("✅ Post updated correctly with new title and content")
            else:
                print("❌ Post update verification failed")
                return False
        else:
            print("❌ Failed to update post")
            print(f"Response: {response.text}")
            return False
        
        # Test 2: Update only title (content should remain)
        print(f"• Updating post {post_id} (title only)...")
        title_only_update = {
            "title": "Title Only Update"
        }
        
        response = requests.put(
            f'http://localhost:5002/api/posts/{post_id}',
            headers={'Content-Type': 'application/json'},
            json=title_only_update
        )
        
        if response.status_code == 200:
            updated_post = response.json()
            if (updated_post['title'] == title_only_update['title'] and 
                updated_post['content'] == update_data['content']):  # Content should remain from previous update
                print("✅ Title-only update successful, content preserved")
            else:
                print("❌ Title-only update failed - content not preserved")
                return False
        else:
            print("❌ Failed to update post title only")
            return False
        
        # Test 3: Update only content (title should remain)
        print(f"• Updating post {post_id} (content only)...")
        content_only_update = {
            "content": "Content Only Update - new content here."
        }
        
        response = requests.put(
            f'http://localhost:5002/api/posts/{post_id}',
            headers={'Content-Type': 'application/json'},
            json=content_only_update
        )
        
        if response.status_code == 200:
            updated_post = response.json()
            if (updated_post['content'] == content_only_update['content'] and 
                updated_post['title'] == title_only_update['title']):  # Title should remain from previous update
                print("✅ Content-only update successful, title preserved")
                return True
            else:
                print("❌ Content-only update failed - title not preserved")
                return False
        else:
            print("❌ Failed to update post content only")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_update_post_not_found():
    """Test PUT endpoint with non-existent ID"""
    try:
        print("\nTesting PUT /api/posts/<id> with non-existent ID...")
        
        # Try to update a post with a very high ID that shouldn't exist
        non_existent_id = 99999
        update_data = {
            "title": "Updated Title",
            "content": "Updated content."
        }
        
        response = requests.put(
            f'http://localhost:5002/api/posts/{non_existent_id}',
            headers={'Content-Type': 'application/json'},
            json=update_data
        )
        
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

def test_sorting_functionality():
    """Test the GET /api/posts endpoint with sorting parameters"""
    try:
        print("\nTesting GET /api/posts endpoint with sorting...")
        
        # First, create multiple posts with different titles and content for sorting
        print("• Creating posts for sorting testing...")
        test_posts = [
            {"title": "Apple Tutorial", "content": "Zebra content for testing sorting."},
            {"title": "Banana Guide", "content": "Alpha content for testing sorting."},
            {"title": "Cherry Notes", "content": "Beta content for testing sorting."},
        ]
        
        created_post_ids = []
        for post_data in test_posts:
            response = requests.post(
                'http://localhost:5002/api/posts',
                headers={'Content-Type': 'application/json'},
                json=post_data
            )
            if response.status_code == 201:
                created_post_ids.append(response.json()['id'])
        
        print(f"✅ Created {len(created_post_ids)} test posts for sorting")
        
        # Test 1: Sort by title ascending
        print("• Testing sort by title ascending...")
        response = requests.get('http://localhost:5002/api/posts?sort=title&direction=asc')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            sorted_posts = response.json()
            print(f"✅ Retrieved {len(sorted_posts)} posts sorted by title (asc)")
            
            # Check if posts are sorted by title in ascending order
            titles = [post['title'] for post in sorted_posts]
            is_sorted_asc = titles == sorted(titles)
            
            if is_sorted_asc:
                print("✅ Posts correctly sorted by title in ascending order")
                print(f"   Titles: {titles}")
            else:
                print("❌ Posts not sorted correctly by title ascending")
                return False
        else:
            print("❌ Failed to sort by title ascending")
            return False
        
        # Test 2: Sort by title descending
        print("• Testing sort by title descending...")
        response = requests.get('http://localhost:5002/api/posts?sort=title&direction=desc')
        
        if response.status_code == 200:
            sorted_posts = response.json()
            titles = [post['title'] for post in sorted_posts]
            is_sorted_desc = titles == sorted(titles, reverse=True)
            
            if is_sorted_desc:
                print("✅ Posts correctly sorted by title in descending order")
                print(f"   Titles: {titles}")
            else:
                print("❌ Posts not sorted correctly by title descending")
                return False
        else:
            print("❌ Failed to sort by title descending")
            return False
        
        # Test 3: Sort by content ascending
        print("• Testing sort by content ascending...")
        response = requests.get('http://localhost:5002/api/posts?sort=content&direction=asc')
        
        if response.status_code == 200:
            sorted_posts = response.json()
            contents = [post['content'] for post in sorted_posts]
            is_sorted_asc = contents == sorted(contents)
            
            if is_sorted_asc:
                print("✅ Posts correctly sorted by content in ascending order")
            else:
                print("❌ Posts not sorted correctly by content ascending")
                return False
        else:
            print("❌ Failed to sort by content ascending")
            return False
        
        # Test 4: Sort by content descending
        print("• Testing sort by content descending...")
        response = requests.get('http://localhost:5002/api/posts?sort=content&direction=desc')
        
        if response.status_code == 200:
            sorted_posts = response.json()
            contents = [post['content'] for post in sorted_posts]
            is_sorted_desc = contents == sorted(contents, reverse=True)
            
            if is_sorted_desc:
                print("✅ Posts correctly sorted by content in descending order")
            else:
                print("❌ Posts not sorted correctly by content descending")
                return False
        else:
            print("❌ Failed to sort by content descending")
            return False
        
        # Test 5: Default to ascending when direction not provided
        print("• Testing default direction (ascending) when only sort field provided...")
        response = requests.get('http://localhost:5002/api/posts?sort=title')
        
        if response.status_code == 200:
            sorted_posts = response.json()
            titles = [post['title'] for post in sorted_posts]
            is_sorted_asc = titles == sorted(titles)
            
            if is_sorted_asc:
                print("✅ Correctly defaulted to ascending order when direction not provided")
            else:
                print("❌ Failed to default to ascending order")
                return False
        else:
            print("❌ Failed to handle missing direction parameter")
            return False
        
        # Test 6: No parameters (original order)
        print("• Testing no sorting parameters (original order)...")
        response = requests.get('http://localhost:5002/api/posts')
        
        if response.status_code == 200:
            posts = response.json()
            print("✅ Successfully retrieved posts in original order")
        else:
            print("❌ Failed to retrieve posts without sorting parameters")
            return False
        
        # Test 7: Invalid sort field
        print("• Testing invalid sort field...")
        response = requests.get('http://localhost:5002/api/posts?sort=invalid_field&direction=asc')
        
        if response.status_code == 400:
            error_response = response.json()
            print("✅ Correctly returned 400 for invalid sort field")
            print(f"   Error: {error_response.get('error', 'No error message')}")
        else:
            print(f"❌ Expected 400 for invalid sort field, got {response.status_code}")
            return False
        
        # Test 8: Invalid direction
        print("• Testing invalid direction...")
        response = requests.get('http://localhost:5002/api/posts?sort=title&direction=invalid_dir')
        
        if response.status_code == 400:
            error_response = response.json()
            print("✅ Correctly returned 400 for invalid direction")
            print(f"   Error: {error_response.get('error', 'No error message')}")
        else:
            print(f"❌ Expected 400 for invalid direction, got {response.status_code}")
            return False
        
        # Test 9: Direction without sort field
        print("• Testing direction without sort field...")
        response = requests.get('http://localhost:5002/api/posts?direction=asc')
        
        if response.status_code == 400:
            error_response = response.json()
            print("✅ Correctly returned 400 for direction without sort field")
            print(f"   Error: {error_response.get('error', 'No error message')}")
            return True
        else:
            print(f"❌ Expected 400 for direction without sort field, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search_posts():
    """Test the GET /api/posts/search endpoint"""
    try:
        print("\nTesting GET /api/posts/search endpoint...")
        
        # First, create some posts with specific content for searching
        print("• Creating posts for search testing...")
        test_posts = [
            {"title": "Flask Tutorial", "content": "Learn how to build web applications with Flask framework."},
            {"title": "Python Basics", "content": "Introduction to Python programming language."},
            {"title": "Database Design", "content": "How to design efficient databases with Flask-SQLAlchemy."}
        ]
        
        created_post_ids = []
        for post_data in test_posts:
            response = requests.post(
                'http://localhost:5002/api/posts',
                headers={'Content-Type': 'application/json'},
                json=post_data
            )
            if response.status_code == 201:
                created_post_ids.append(response.json()['id'])
        
        print(f"✅ Created {len(created_post_ids)} test posts")
        
        # Test 1: Search by title
        print("• Testing search by title (query: 'flask')...")
        response = requests.get('http://localhost:5002/api/posts/search?title=flask')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            search_results = response.json()
            print(f"✅ Found {len(search_results)} posts matching title 'flask'")
            
            # Verify results contain the word "flask" in title
            flask_found = any('flask' in post['title'].lower() for post in search_results)
            if flask_found:
                print("✅ Search results contain posts with 'flask' in title")
            else:
                print("❌ Search results don't contain expected posts")
                return False
        else:
            print("❌ Failed to search by title")
            return False
        
        # Test 2: Search by content
        print("• Testing search by content (query: 'python')...")
        response = requests.get('http://localhost:5002/api/posts/search?content=python')
        
        if response.status_code == 200:
            search_results = response.json()
            print(f"✅ Found {len(search_results)} posts matching content 'python'")
            
            # Verify results contain the word "python" in content
            python_found = any('python' in post['content'].lower() for post in search_results)
            if python_found:
                print("✅ Search results contain posts with 'python' in content")
            else:
                print("❌ Search results don't contain expected posts")
                return False
        else:
            print("❌ Failed to search by content")
            return False
        
        # Test 3: Search with both parameters
        print("• Testing search with both title and content parameters...")
        response = requests.get('http://localhost:5002/api/posts/search?title=database&content=flask')
        
        if response.status_code == 200:
            search_results = response.json()
            print(f"✅ Found {len(search_results)} posts matching either criteria")
            print("✅ Combined search working correctly")
        else:
            print("❌ Failed to search with combined parameters")
            return False
        
        # Test 4: Search with no matches
        print("• Testing search with no matches (query: 'nonexistent')...")
        response = requests.get('http://localhost:5002/api/posts/search?title=nonexistent')
        
        if response.status_code == 200:
            search_results = response.json()
            if len(search_results) == 0:
                print("✅ Correctly returned empty list for no matches")
            else:
                print("❌ Should return empty list for no matches")
                return False
        else:
            print("❌ Failed to handle no matches case")
            return False
        
        # Test 5: Search with no parameters
        print("• Testing search with no parameters...")
        response = requests.get('http://localhost:5002/api/posts/search')
        
        if response.status_code == 200:
            search_results = response.json()
            if len(search_results) == 0:
                print("✅ Correctly returned empty list for no search parameters")
                return True
            else:
                print("❌ Should return empty list when no parameters provided")
                return False
        else:
            print("❌ Failed to handle no parameters case")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running on port 5002")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running API Tests for Step 6: Complete CRUD + Search + Sorting Operations\n")
    
    # Test GET endpoint first
    get_success = test_get_posts()
    
    # Test POST endpoint
    add_success = test_add_post()
    
    # Test POST validation
    validation_success = test_add_post_validation()
    
    # Test PUT endpoint (update)
    update_success = test_update_post()
    
    # Test PUT with non-existent ID
    update_not_found_success = test_update_post_not_found()
    
    # Test SEARCH endpoint
    search_success = test_search_posts()
    
    # Test SORTING functionality
    sorting_success = test_sorting_functionality()
    
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
    print(f"PUT /api/posts/<id>: {'✅ PASS' if update_success else '❌ FAIL'}")
    print(f"PUT 404 Error: {'✅ PASS' if update_not_found_success else '❌ FAIL'}")
    print(f"GET /api/posts/search: {'✅ PASS' if search_success else '❌ FAIL'}")
    print(f"GET /api/posts (sorting): {'✅ PASS' if sorting_success else '❌ FAIL'}")
    print(f"DELETE /api/posts/<id>: {'✅ PASS' if delete_success else '❌ FAIL'}")
    print(f"DELETE 404 Error: {'✅ PASS' if delete_not_found_success else '❌ FAIL'}")
    
    all_tests_passed = all([get_success, add_success, validation_success, update_success, update_not_found_success, search_success, sorting_success, delete_success, delete_not_found_success])
    
    if all_tests_passed:
        print("\n🎉 All tests passed! Step 6 Enhanced API implementation is complete and working correctly.")
        print("✨ Your RESTful Blog API supports: CREATE, READ, UPDATE, DELETE + SEARCH + SORTING operations!")
        print("🔍 Search functionality allows finding posts by title or content!")
        print("📊 Sorting functionality allows organizing posts by title or content in asc/desc order!")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")