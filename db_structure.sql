-- Create database
CREATE DATABASE IF NOT EXISTS eval;
USE eval;

-- Table: admin_users
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_master_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: sections
CREATE TABLE sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: criteria (depends on sections)
CREATE TABLE criteria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    question TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE
);

-- Table: participants
CREATE TABLE participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    qualification VARCHAR(100) NOT NULL,
    program_type VARCHAR(50) NOT NULL,
    training_duration VARCHAR(100) NOT NULL,
    trainer_name VARCHAR(100) NOT NULL,
    evaluation_date DATE NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: responses_master (depends on participants)
CREATE TABLE responses_master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
);

-- Table: responses (depends on participants and criteria)
CREATE TABLE responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id INT NOT NULL,
    criterion_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES criteria(id) ON DELETE CASCADE,
    UNIQUE KEY unique_response (participant_id, criterion_id)
);