-- Create the database if it doesn't exist
CREATE DATABASE gum_chat;

-- Connect to the gum_chat database
\c gum_chat;

-- Create users table for storing user information
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the email column to optimize searching
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- You can add more tables here if needed, e.g., for posts or messages

-- Sample data to test the application (optional)
INSERT INTO users (name, email, password, profile_picture)
VALUES
('Admin User', 'admin@example.com', 'adminpassword', 'profile_pictures/admin.jpg'),
('John Doe', 'johndoe@example.com', 'johnpassword', 'profile_pictures/john.jpg'),
('Jane Smith', 'janesmith@example.com', 'janesmithpassword', 'profile_pictures/jane.jpg');

