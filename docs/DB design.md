# Product Database Design Documentation

## 1. Overview

This document outlines the database design decisions for managing diverse product categories, including jewelries, clothing, pottery, home decor, arts & paintings, food & beverage  and soon. The system uses a **key-value pair** approach for storing dynamic product attributes efficiently.

## 2. Design Goals

- **Flexibility**: Support a wide range of product categories with different attributes.
- **Scalability**: Ensure performance remains optimal as data grows.
- **Minimal Duplication**: Reduce redundant storage of common attributes.
- **Ease of Querying**: Enable efficient filtering and retrieval of product data.

## 3. Database Schema

### **3.1 Category Table**

Stores unique categories.

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | UUID (PK)    |  Unique value identifier       |
| name        | VARCHAR(255) | Category name                  |
| slug        | VARCHAR(255) | Unique url generated from name |

### **3.2 CategoryAttributes Table**

Defines the possible attributes for each category. This is also used for dynamic Front-end form generation.

| Column      | Type         | Description                                     |
|-------------|------------- |-------------------------------------------------|
| id          | UUID (PK)    | Unique attribute identifier                     |
| category_id | INT (FK)     | Links to Categories table                       |
| field_name  | VARCHAR(255) | Name of the attribute (e.g., 'size')            |
| field_type  | UUID(FK)     | Data type (string, integer, etc.)               |
| form_type   | UUID(FK)     | HTML form field type (dropdown, text, number)   |
| required    | BOOLEAN      | Whether the field is mandatory or not in the UI |

### **3.3 Products Table**

Stores common product details that apply to all categories.

| Column      | Type         | Description |
|-------------|------------- |-------------|
| id          | UUID (PK)    |  Unique product identifier |
| name        | VARCHAR(255) | Product name |
| category_id | UUID (FK)    | Links to Categories table |
| price       | DECIMAL(10,2)| product selling price |
| quantity    | INT          | product quantity available in stock |
| available_colors | Many-to-Many | Indicates available color choices for a product |
| description | VARCHAR(255) | Product description |
| material | VARCHAR(255) | Product ingredients |
| artisan | UUID(FK) | Product owner or supplier |

### **3.4 ProductAttributes Table**

Links products to it's unique attributes using a key-value structure.

| Column       | Type         | Description |
|-------------|--------------|-------------|
| id          | UUID (PK)    | Unique identifier |
| product_id  | UUID (FK)    | Links to Products table |
| field_name  | VARCHAR(100) | Links to CategoryAttributes table |
| field_value | VARCHAR(100) | Links to AttributeValues table |

## 4. Data Flow

### **Product Registration**

1. User selects a category (e.g., Pottery).
2. System retrieves predefined attributes for the category from `CategoryAttributes`.
3. User inputs values for each attribute.
4. Product details and attributes are stored in `Products` and `ProductAttributes`.

### **Querying Products with Attributes**

To fetch a product with its attributes:

```sql
SELECT p.id, p.name, p.price, p.quantity,,, ca.name
FROM Products p
JOIN ProductAttributes pa ON p.id = pa.product_id
WHERE p.id = ?;
```

## 5. Pros & Cons

### **Pros:**

- Flexible for adding new attributes dynamically.
- Dynamic form generation based on a given category.

### **Cons:**

- Requires multiple table joins for querying.
- Slightly more complex data insertion logic.

## 6. Alternatives Considered

### **1. Storing Attributes in JSON**

- **Pros:** Simple and requires fewer tables.
- **Cons:** Harder to query and filter attributes efficiently.

### **2. Separate Columns for Each Attribute**

- **Pros:** Easier to query directly.

- **Cons:** Not scalable for categories with different attributes.

## 7. Future Improvements

- Index optimization for faster queries.
- Implement caching for frequently accessed product attributes.

---
This document provides a structured foundation for the product database design. It ensures flexibility, efficiency, and maintainability as the system scales.
