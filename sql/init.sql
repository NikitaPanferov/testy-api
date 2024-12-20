CREATE DATABASE IF NOT EXISTS form_editor;
use form_editor;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    hashed_password BINARY(60) NOT NULL,
    refresh_token VARCHAR(255)
);

CREATE TABLE tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    type ENUM('single_choice', 'multiple_choice', 'free_text') NOT NULL,
    number_in_test INT,
    test_id INT,
    FOREIGN KEY (test_id) REFERENCES tests(id) ON DELETE CASCADE,
    UNIQUE KEY _test_number_uc (test_id, number_in_test)
);

CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    number_in_question INT,
    question_id INT,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    UNIQUE KEY _question_number_uc (question_id, number_in_question)
);
