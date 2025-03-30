# Corlee API Documentation

This document provides detailed information about all the available API endpoints in the Corlee backend application.

## Table of Contents

1. [Authentication](#authentication)
2. [Product Categories](#product-categories)
3. [Blog Categories](#blog-categories)
4. [Color Categories](#color-categories)
5. [Fabrics](#fabrics)
6. [Events](#events)
7. [Orders](#orders)
8. [Users](#users)
9. [Contact Details](#contact-details)
10. [Contact Requests](#contact-requests)
11. [Blogs](#blogs)
12. [Media Uploads](#media-uploads)
13. [Cart](#cart)
14. [Favorites](#favorites)
15. [Subscription](#subscription)

## Authentication

### Register User

- **Endpoint**: `/register/`
- **Method**: POST
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "username": "exampleuser",
    "password": "password123",
    "email": "user@example.com",
    "name": "John Doe",
    "company_name": "Example Company",
    "address": "123 Example St",
    "phone": "1234567890",
    "mobile_phone": "0987654321"
  }
  ```
- **Response**: User details with token

### Login

- **Endpoint**: `/login/`
- **Method**: POST
- **Description**: Authenticate user and get token
- **Request Body**:
  ```json
  {
    "username": "exampleuser",
    "password": "password123"
  }
  ```
- **Response**: User details with token

### Google Login

- **Endpoint**: `/google-login/`
- **Method**: POST
- **Description**: Authenticate user with Google ID token
- **Request Body**:
  ```json
  {
    "idToken": "google-id-token"
  }
  ```
- **Response**: User details with token

### Email Verification

- **Endpoint**: `/verify-email/<verification_token>/`
- **Method**: GET
- **Description**: Verify user email with token
- **Response**: Redirects to frontend with success/failure message

### Password Reset

- **Endpoint**: `/password_reset/`
- **Method**: POST
- **Description**: Request password reset
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: Success message

### Password Reset Confirm

- **Endpoint**: `/password_reset/done/`
- **Method**: POST
- **Description**: Confirm password reset with token
- **Request Body**:
  ```json
  {
    "new_password1": "newpassword123",
    "new_password2": "newpassword123",
    "uid": "uid_from_email",
    "token": "token_from_email"
  }
  ```
- **Response**: Success message

## Product Categories

### List All Product Categories

- **Endpoint**: `/product-categories/`
- **Method**: GET
- **Description**: Get a list of all product categories
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of product categories with pagination

### Get Product Category

- **Endpoint**: `/product-categories/<id>/`
- **Method**: GET
- **Description**: Get details of a specific product category
- **Response**: Product category details

### Create Product Category

- **Endpoint**: `/product-categories/`
- **Method**: POST
- **Description**: Create a new product category
- **Request Body**:
  ```json
  {
    "name": "Category Name",
    "description": "Category Description",
    "image": 1 // ID of MediaUploads object
  }
  ```
- **Response**: Created product category details

### Update Product Category

- **Endpoint**: `/product-categories/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing product category
- **Request Body**:
  ```json
  {
    "name": "Updated Category Name",
    "description": "Updated Category Description",
    "image": 2 // ID of MediaUploads object
  }
  ```
- **Response**: Updated product category details

### Delete Product Category

- **Endpoint**: `/product-categories/<id>/`
- **Method**: DELETE
- **Description**: Delete a product category
- **Response**: No content (204)

## Blog Categories

### List All Blog Categories

- **Endpoint**: `/blog-categories/`
- **Method**: GET
- **Description**: Get a list of all blog categories
- **Response**: List of blog categories

### Get Blog Category

- **Endpoint**: `/blog-categories/<id>/`
- **Method**: GET
- **Description**: Get details of a specific blog category
- **Response**: Blog category details

### Create Blog Category

- **Endpoint**: `/blog-categories/`
- **Method**: POST
- **Description**: Create a new blog category
- **Request Body**:
  ```json
  {
    "name": "Blog Category Name"
  }
  ```
- **Response**: Created blog category details

### Update Blog Category

- **Endpoint**: `/blog-categories/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing blog category
- **Request Body**:
  ```json
  {
    "name": "Updated Blog Category Name"
  }
  ```
- **Response**: Updated blog category details

### Delete Blog Category

- **Endpoint**: `/blog-categories/<id>/`
- **Method**: DELETE
- **Description**: Delete a blog category
- **Response**: No content (204)

## Color Categories

### List All Color Categories

- **Endpoint**: `/color-categories/`
- **Method**: GET
- **Description**: Get a list of all fabric color categories
- **Response**: List of color categories

### Get Color Category

- **Endpoint**: `/color-categories/<id>/`
- **Method**: GET
- **Description**: Get details of a specific color category
- **Response**: Color category details

### Create Color Category

- **Endpoint**: `/color-categories/`
- **Method**: POST
- **Description**: Create a new color category
- **Request Body**:
  ```json
  {
    "display_name": "Red",
    "color": "#FF0000"
  }
  ```
- **Response**: Created color category details

### Update Color Category

- **Endpoint**: `/color-categories/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing color category
- **Request Body**:
  ```json
  {
    "display_name": "Dark Red",
    "color": "#8B0000"
  }
  ```
- **Response**: Updated color category details

### Delete Color Category

- **Endpoint**: `/color-categories/<id>/`
- **Method**: DELETE
- **Description**: Delete a color category
- **Response**: No content (204)

## Fabrics

### List All Fabrics

- **Endpoint**: `/fabrics/`
- **Method**: GET
- **Description**: Get a list of all fabrics with optional filtering
- **Query Parameters**:
  - `keyword`: Search term
  - `sort_by`: Sort by "newest" or "oldest"
  - `colors`: Filter by color names
  - `item_code`: Filter by item code
  - `page`: Page number for pagination
- **Response**: List of fabrics with pagination

### Get Fabric Details

- **Endpoint**: `/fabrics/<id>/`
- **Method**: GET
- **Description**: Get details of a specific fabric
- **Response**: Fabric details with color images

### Create Fabric

- **Endpoint**: `/fabrics/create/`
- **Method**: POST
- **Description**: Create a new fabric
- **Request Body**:
  ```json
  {
    "product_category": 1,
    "title": "Fabric Name",
    "description": "Fabric Description",
    "composition": "100% Cotton",
    "weight": "150gsm",
    "finish": "Soft",
    "item_code": "FAB123",
    "is_hot_selling": false,
    "color_images": [
      {
        "color_category": 1,
        "primary_image": 1,
        "aux_image1": 2,
        "aux_image2": 3,
        "aux_image3": 4,
        "model_image": 5
      }
    ]
  }
  ```
- **Response**: Created fabric details

### Update Fabric

- **Endpoint**: `/fabrics/<id>/update/`
- **Method**: PUT/PATCH
- **Description**: Update an existing fabric
- **Request Body**:
  ```json
  {
    "product_category": 1,
    "title": "Updated Fabric Name",
    "description": "Updated Fabric Description",
    "composition": "100% Cotton",
    "weight": "150gsm",
    "finish": "Soft",
    "item_code": "FAB123",
    "is_hot_selling": true,
    "color_images": [
      {
        "color_category": 1,
        "primary_image": 1,
        "aux_image1": 2,
        "aux_image2": 3,
        "aux_image3": 4,
        "model_image": 5
      }
    ]
  }
  ```
- **Response**: Updated fabric details

### Delete Fabric

- **Endpoint**: `/fabrics/<id>/delete/`
- **Method**: DELETE
- **Description**: Delete a fabric
- **Response**: No content (204)

## Events

### List All Events

- **Endpoint**: `/events/`
- **Method**: GET
- **Description**: Get a list of all events
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of events with pagination

### Get Event Details

- **Endpoint**: `/events/<id>/`
- **Method**: GET
- **Description**: Get details of a specific event
- **Response**: Event details

### Create Event

- **Endpoint**: `/events/`
- **Method**: POST
- **Description**: Create a new event
- **Request Body**:
  ```json
  {
    "title": "Event Title",
    "description": "Event Description",
    "date": "2023-12-31",
    "time": "18:00:00",
    "photo": 1, // ID of MediaUploads object
    "location": "Event Location",
    "url": "https://example.com/event",
    "email": "event@example.com",
    "phone": "1234567890"
  }
  ```
- **Response**: Created event details

### Update Event

- **Endpoint**: `/events/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing event
- **Request Body**:
  ```json
  {
    "title": "Updated Event Title",
    "description": "Updated Event Description",
    "date": "2023-12-31",
    "time": "19:00:00",
    "photo": 2, // ID of MediaUploads object
    "location": "Updated Event Location",
    "url": "https://example.com/updated-event",
    "email": "event@example.com",
    "phone": "1234567890"
  }
  ```
- **Response**: Updated event details

### Delete Event

- **Endpoint**: `/events/<id>/`
- **Method**: DELETE
- **Description**: Delete an event
- **Response**: No content (204)

## Orders

### List All Orders

- **Endpoint**: `/orders/`
- **Method**: GET
- **Description**: Get a list of all orders (admin) or user's orders (regular user)
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of orders with pagination

### Get Order Details

- **Endpoint**: `/orders/<id>/`
- **Method**: GET
- **Description**: Get details of a specific order
- **Response**: Order details with items

### Create Order

- **Endpoint**: `/orders/`
- **Method**: POST
- **Description**: Create a new order
- **Request Body**:
  ```json
  {
    "user": 1, // Optional, ID of user
    "items": [
      {
        "fabric": 1,
        "color": "Red",
        "quantity": 5
      },
      {
        "fabric": 2,
        "color": "Blue",
        "quantity": 3
      }
    ]
  }
  ```
- **Response**: Created order details

### Update Order

- **Endpoint**: `/orders/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing order
- **Request Body**:
  ```json
  {
    "user": 1,
    "items": [
      {
        "fabric": 1,
        "color": "Red",
        "quantity": 10
      },
      {
        "fabric": 3,
        "color": "Green",
        "quantity": 2
      }
    ]
  }
  ```
- **Response**: Updated order details

### Delete Order

- **Endpoint**: `/orders/<id>/`
- **Method**: DELETE
- **Description**: Delete an order
- **Response**: No content (204)

### Checkout

- **Endpoint**: `/checkout/`
- **Method**: POST
- **Description**: Process checkout from cart
- **Response**: Order details

## Users

### List All Users (Admin Only)

- **Endpoint**: `/users/`
- **Method**: GET
- **Description**: Get a list of all users (admin only)
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of users with pagination

### Get User Details (Admin Only)

- **Endpoint**: `/users/<id>/`
- **Method**: GET
- **Description**: Get details of a specific user (admin only)
- **Response**: User details

### Create User (Admin Only)

- **Endpoint**: `/users/`
- **Method**: POST
- **Description**: Create a new user (admin only)
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "name": "New User",
    "email": "newuser@example.com",
    "company_name": "Company Name",
    "address": "123 Address St",
    "phone": "1234567890",
    "mobile_phone": "0987654321",
    "photo": 1, // ID of MediaUploads object
    "auth_method": "email",
    "is_staff": false,
    "is_active": true
  }
  ```
- **Response**: Created user details

### Update User (Admin Only)

- **Endpoint**: `/users/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing user (admin only)
- **Request Body**:
  ```json
  {
    "name": "Updated User Name",
    "email": "updatedemail@example.com",
    "company_name": "Updated Company",
    "is_staff": true
  }
  ```
- **Response**: Updated user details

### Delete User (Admin Only)

- **Endpoint**: `/users/<id>/`
- **Method**: DELETE
- **Description**: Delete a user (admin only)
- **Response**: No content (204)

### Current User Profile

- **Endpoint**: `/user/`
- **Method**: GET
- **Description**: Get current user profile
- **Response**: User profile details

### Update Current User Profile

- **Endpoint**: `/user/`
- **Method**: PATCH
- **Description**: Update current user profile
- **Request Body**:
  ```json
  {
    "name": "Updated Name",
    "company_name": "Updated Company",
    "address": "New Address",
    "phone": "0987654321"
  }
  ```
- **Response**: Updated user profile

## Contact Details

### List Contact Details

- **Endpoint**: `/contact-details/`
- **Method**: GET
- **Description**: Get company contact details
- **Response**: Contact details

### Create Contact Details

- **Endpoint**: `/contact-details/`
- **Method**: POST
- **Description**: Create contact details
- **Request Body**:
  ```json
  {
    "phone": "1234567890",
    "email": "contact@example.com",
    "address": "123 Company St",
    "city": "Example City",
    "county": "Example County",
    "postal_code": "12345",
    "latitude": 12.345678,
    "longitude": 98.765432,
    "country": "Example Country",
    "facebook": "https://facebook.com/example",
    "instagram": "https://instagram.com/example",
    "whatsapp": "+1234567890",
    "line": "example-line"
  }
  ```
- **Response**: Created contact details

### Update Contact Details

- **Endpoint**: `/contact-details/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update contact details
- **Request Body**: Same as create
- **Response**: Updated contact details

### Delete Contact Details

- **Endpoint**: `/contact-details/<id>/`
- **Method**: DELETE
- **Description**: Delete contact details
- **Response**: No content (204)

## Contact Requests

### List Contact Requests

- **Endpoint**: `/contact-requests/`
- **Method**: GET
- **Description**: Get all contact requests (admin) or user's contact requests (regular user)
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of contact requests with pagination

### Get Contact Request

- **Endpoint**: `/contact-requests/<id>/`
- **Method**: GET
- **Description**: Get details of a specific contact request
- **Response**: Contact request details

### Create Contact Request

- **Endpoint**: `/contact-requests/`
- **Method**: POST
- **Description**: Create a new contact request
- **Request Body**:
  ```json
  {
    "user": 1, // Optional, ID of user
    "request_type": "general",
    "subject": "Request Subject",
    "message": "Request Message",
    "related_fabric": 1, // Optional, ID of fabric
    "company_name": "Company Name",
    "email": "email@example.com",
    "sample_requested": true,
    "related_order": 1, // Optional, ID of order
    "current_status": "new",
    "order_status": "new"
  }
  ```
- **Response**: Created contact request details

### Update Contact Request

- **Endpoint**: `/contact-requests/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing contact request
- **Request Body**:
  ```json
  {
    "current_status": "in_progress",
    "order_status": "processing"
  }
  ```
- **Response**: Updated contact request details

### Delete Contact Request

- **Endpoint**: `/contact-requests/<id>/`
- **Method**: DELETE
- **Description**: Delete a contact request
- **Response**: No content (204)

### Submit Contact Form

- **Endpoint**: `/contact/`
- **Method**: POST
- **Description**: Submit a contact form
- **Request Body**:
  ```json
  {
    "item_code": "FAB123",
    "name": "John Doe",
    "request_type": "general",
    "subject": "Contact Subject",
    "email": "johndoe@example.com",
    "phone_number": "1234567890",
    "company_name": "Example Company",
    "description": "Contact message",
    "sample_requested": false
  }
  ```
- **Response**: Success message

## Blogs

### List All Blogs

- **Endpoint**: `/blogs/`
- **Method**: GET
- **Description**: Get a list of all blogs with filtering options
- **Query Parameters**:
  - `category`: Filter by category ID
  - `search`: Search in title, content, category name
  - `ordering`: Order by created_at, title, view_count
  - `page`: Page number for pagination
- **Response**: List of blogs with pagination

### Get Blog Details

- **Endpoint**: `/blogs/<id>/`
- **Method**: GET
- **Description**: Get details of a specific blog (increments view count)
- **Response**: Blog details

### Create Blog

- **Endpoint**: `/blogs/`
- **Method**: POST
- **Description**: Create a new blog
- **Request Body**:
  ```json
  {
    "title": "Blog Title",
    "content": "Blog Content",
    "author": 1, // ID of user
    "photo": 1, // ID of MediaUploads object
    "category": 1 // ID of blog category
  }
  ```
- **Response**: Created blog details

### Update Blog

- **Endpoint**: `/blogs/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing blog
- **Request Body**:
  ```json
  {
    "title": "Updated Blog Title",
    "content": "Updated Blog Content",
    "photo": 2, // ID of MediaUploads object
    "category": 2 // ID of blog category
  }
  ```
- **Response**: Updated blog details

### Delete Blog

- **Endpoint**: `/blogs/<id>/`
- **Method**: DELETE
- **Description**: Delete a blog
- **Response**: No content (204)

## Media Uploads

### List All Media

- **Endpoint**: `/media/`
- **Method**: GET
- **Description**: Get a list of all media uploads
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of media uploads with pagination

### Get Media Details

- **Endpoint**: `/media/<id>/`
- **Method**: GET
- **Description**: Get details of a specific media upload
- **Response**: Media upload details with URL

### Create Media Upload

- **Endpoint**: `/media/create/`
- **Method**: POST
- **Description**: Upload a new media file (automatically converts images to WebP)
- **Request Body**: Form data with 'file' field
- **Response**: Created media upload details

### Delete Media Upload

- **Endpoint**: `/media/<id>/delete/`
- **Method**: DELETE
- **Description**: Delete a media upload
- **Response**: No content (204)

## Cart

### List Cart Items

- **Endpoint**: `/cart-items/`
- **Method**: GET
- **Description**: Get all items in the user's cart
- **Response**: List of cart items

### Add Item to Cart

- **Endpoint**: `/cart-items/`
- **Method**: POST
- **Description**: Add an item to the user's cart
- **Request Body**:
  ```json
  {
    "fabric_id": 1,
    "color": "Red",
    "quantity": 2
  }
  ```
- **Response**: Created cart item details

### Update Cart Item

- **Endpoint**: `/cart-items/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update a cart item
- **Request Body**:
  ```json
  {
    "quantity": 5
  }
  ```
- **Response**: Updated cart item details

### Remove Item from Cart

- **Endpoint**: `/cart-items/<id>/`
- **Method**: DELETE
- **Description**: Remove an item from the cart
- **Response**: No content (204)

## Favorites

### Toggle Favorite

- **Endpoint**: `/toggle_favorite/`
- **Method**: POST
- **Description**: Add or remove a fabric from favorites
- **Request Body**:
  ```json
  {
    "fabric_id": 1
  }
  ```
- **Response**: Success message

### List Favorite Fabrics

- **Endpoint**: `/favorite_fabrics/`
- **Method**: GET
- **Description**: Get all fabrics marked as favorite by the user
- **Query Parameters**:
  - `sort_by`: Sort by "newest" or "oldest"
  - `colors`: Filter by colors
- **Response**: List of favorite fabrics

## Subscription

### Subscribe to Newsletter

- **Endpoint**: `/subscribe/`
- **Method**: POST
- **Description**: Subscribe email to newsletter
- **Request Body**:
  ```json
  {
    "email": "subscriber@example.com"
  }
  ```
- **Response**: Success message
