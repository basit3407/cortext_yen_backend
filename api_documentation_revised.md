# Corlee API Documentation - Core Models

This document provides detailed information about the API endpoints for the core models in the Corlee backend application.

## Table of Contents

1. [Product Categories](#product-categories)
2. [Blog Categories](#blog-categories)
3. [Color Categories](#color-categories)
4. [Events](#events)
5. [Orders](#orders)
6. [Users](#users)
7. [Contact Details](#contact-details)
8. [Contact Requests](#contact-requests)
9. [Blogs](#blogs)
10. [Fabrics](#fabrics)
11. [Media Uploads](#media-uploads)

## Fabrics

### List All Fabrics

- **Endpoint**: `/fabrics/`
- **Method**: GET
- **Description**: Get a list of all fabrics with filtering options
- **Query Parameters**:
  - `keyword`: Search keyword
  - `sort_by`: Sort by "newest" or "oldest"
  - `colors`: Filter by colors (array of color names) - see [Color Categories](#color-categories)
  - `item_code`: Filter by item code
  - `page`: Page number for pagination
- **Response**: List of fabrics with pagination

### Get Fabric Details

- **Endpoint**: `/fabrics/<id>/`
- **Method**: GET
- **Description**: Get details of a specific fabric
- **Response**: Fabric details including color images, product category, and metadata

### Create Fabric

- **Endpoint**: `/fabrics/`
- **Method**: POST
- **Description**: Create a new fabric
- **Request Body**:
  ```json
  {
    "product_category": 1, // ID of product category - see Product Categories section
    "title": "Fabric Title",
    "description": "Fabric Description",
    "composition": "100% Cotton",
    "weight": "200 gsm",
    "finish": "Soft",
    "item_code": "FAB123",
    "is_hot_selling": false,
    "color_images": [
      {
        "color_category": 1, // ID of color category - see Color Categories section
        "primary_image": 1,
        "aux_image1": null,
        "aux_image2": null,
        "aux_image3": null,
        "model_image": null
      }
    ]
  }
  ```
- **Response**: Created fabric details

### Update Fabric

- **Endpoint**: `/fabrics/<id>/update/`
- **Method**: PUT/PATCH
- **Description**: Update an existing fabric
- **Request Body**: Same as Create Fabric
- **Response**: Updated fabric details

### Delete Fabric

- **Endpoint**: `/fabrics/<id>/delete/`
- **Method**: DELETE
- **Description**: Delete a fabric
- **Response**: No content (204)

### Add/Remove Fabric to Favorites

- **Endpoint**: `/toggle_favorite/`
- **Method**: POST
- **Description**: Add or remove a fabric from the user's favorites
- **Request Body**:
  ```json
  {
    "fabric_id": 1
  }
  ```
- **Response**:
  - 201: Fabric added to favorites
  - 204: Fabric removed from favorites

### List Favorite Fabrics

- **Endpoint**: `/favorite_fabrics/`
- **Method**: GET
- **Description**: Get a list of the user's favorite fabrics
- **Query Parameters**:
  - `sort_by`: Sort by "newest" or "oldest"
  - `colors`: Filter by colors
- **Response**: List of favorite fabrics

## Product Categories

### List All Product Categories

- **Endpoint**: `/product-categories/`
- **Alternative Endpoint**: `/categories/` (also available)
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
- **Alternative Endpoint**: `/color-categories/` (also available via separate view)
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
- **Description**: Get a list of all orders (admin) or user's orders (regular user) with complete user details
- **Query Parameters**:
  - `page`: Page number for pagination
- **Response**: List of orders with pagination, including full user details

- **Response Structure**:
  ```json
  {
    "count": 25,
    "next": "https://api.example.com/orders/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "order_id": 1,
        "order_date": "2023-05-15T14:30:45Z",
        "items": [
          {
            "id": 1,
            "fabric": {
              "id": 23,
              "title": "Premium Cotton",
              "item_code": "FAB123"
            },
            "color": "Red",
            "quantity": 5
          }
        ],
        "user": {
          "id": 12,
          "username": "customer123",
          "name": "John Smith",
          "company_name": "Fashion Designs Ltd.",
          "address": "123 Main Street, New York, NY 10001",
          "phone": "212-555-1234",
          "mobile_phone": "917-555-5678",
          "email": "john.smith@fashiondesigns.com",
          "is_verified": true
        }
      },
      {
        "id": 2,
        "order_id": 2,
        "order_date": "2023-05-18T09:15:22Z",
        "items": [
          {
            "id": 3,
            "fabric": {
              "id": 45,
              "title": "Silk Blend",
              "item_code": "FAB456"
            },
            "color": "Blue",
            "quantity": 2
          }
        ],
        "user": {
          "id": 12,
          "username": "customer123",
          "name": "John Smith",
          "company_name": "Fashion Designs Ltd.",
          "address": "123 Main Street, New York, NY 10001",
          "phone": "212-555-1234",
          "mobile_phone": "917-555-5678",
          "email": "john.smith@fashiondesigns.com",
          "is_verified": true
        }
      }
    ]
  }
  ```

### Get Order Details

- **Endpoint**: `/orders/<id>/`
- **Method**: GET
- **Description**: Get details of a specific order including complete user information
- **Response**: Order details with items and user details including:

  - User ID
  - Username
  - Name
  - Company name
  - Address
  - Phone numbers
  - Email
  - Verification status

- **Response Structure**:
  ```json
  {
    "id": 1,
    "order_id": 1,
    "order_date": "2023-05-15T14:30:45Z",
    "items": [
      {
        "id": 1,
        "fabric": {
          "id": 23,
          "title": "Premium Cotton",
          "item_code": "FAB123"
        },
        "color": "Red",
        "quantity": 5
      },
      {
        "id": 2,
        "fabric": {
          "id": 45,
          "title": "Silk Blend",
          "item_code": "FAB456"
        },
        "color": "Blue",
        "quantity": 3
      }
    ],
    "user": {
      "id": 12,
      "username": "customer123",
      "name": "John Smith",
      "company_name": "Fashion Designs Ltd.",
      "address": "123 Main Street, New York, NY 10001",
      "phone": "212-555-1234",
      "mobile_phone": "917-555-5678",
      "email": "john.smith@fashiondesigns.com",
      "is_verified": true
    }
  }
  ```

### Create Order

- **Endpoint**: `/orders/`
- **Method**: POST
- **Description**: Create a new order
- **Request Body**:
  ```json
  {
    "user_id": 1, // ID of user
    "items": [
      {
        "fabric": 1, // Required - Fabric ID must be specified for each item
        "color": "Red",
        "quantity": 5
      },
      {
        "fabric": 2, // Required - Fabric ID must be specified for each item
        "color": "Blue",
        "quantity": 3
      }
    ]
  }
  ```
- **Response**: Created order details including user information and order ID

- **Response Structure**:
  ```json
  {
    "id": 3,
    "order_id": 3,
    "order_date": "2023-06-02T11:45:30Z",
    "items": [
      {
        "id": 5,
        "fabric": {
          "id": 1,
          "title": "Premium Cotton",
          "item_code": "FAB123"
        },
        "color": "Red",
        "quantity": 5
      },
      {
        "id": 6,
        "fabric": {
          "id": 2,
          "title": "Linen Blend",
          "item_code": "FAB789"
        },
        "color": "Blue",
        "quantity": 3
      }
    ],
    "user": {
      "id": 12,
      "username": "customer123",
      "name": "John Smith",
      "company_name": "Fashion Designs Ltd.",
      "address": "123 Main Street, New York, NY 10001",
      "phone": "212-555-1234",
      "mobile_phone": "917-555-5678",
      "email": "john.smith@fashiondesigns.com",
      "is_verified": true
    }
  }
  ```

### Update Order

- **Endpoint**: `/orders/<id>/`
- **Method**: PUT/PATCH
- **Description**: Update an existing order
- **Request Body**:
  ```json
  {
    "user_id": 1,
    "items": [
      {
        "fabric": 1, // Required - Fabric ID must be specified for each item
        "color": "Red",
        "quantity": 10
      },
      {
        "fabric": 3, // Required - Fabric ID must be specified for each item
        "color": "Green",
        "quantity": 2
      }
    ]
  }
  ```
- **Response**: Updated order details with user information

- **Error Responses**:
  - `400 Bad Request`: If fabric is missing from any order item
  - `404 Not Found`: If the order doesn't exist
  - `500 Internal Server Error`: If there's a database error

### Delete Order

- **Endpoint**: `/orders/<id>/`
- **Method**: DELETE
- **Description**: Delete an order
- **Response**: No content (204)

### Checkout

- **Endpoint**: `/checkout/`
- **Method**: POST
- **Description**: Process checkout from cart
- **Response**: Order details with user information

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
