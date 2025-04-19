
-- Создание базы данных
CREATE DATABASE IF NOT EXISTS carpet_shop;
USE carpet_shop;

-- Таблица пользователей
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('customer', 'manager') NOT NULL
);

-- Категории ковров
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Материалы (модель, ткань, страна)
CREATE TABLE materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100),
    fabric VARCHAR(100),
    country VARCHAR(100)
);

-- Ковры
CREATE TABLE carpets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    image_url VARCHAR(255),
    category_id INT,
    material_id INT,
    price_per_m2 DECIMAL(10, 2),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

-- Окантовки
CREATE TABLE edge_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    image_url VARCHAR(255)
);

-- Заказы
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('в работе', 'оформлен', 'отгружен') DEFAULT 'в работе',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Элементы заказа
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    carpet_id INT,
    edge_type_id INT,
    width DECIMAL(5,2),
    height DECIMAL(5,2),
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (carpet_id) REFERENCES carpets(id),
    FOREIGN KEY (edge_type_id) REFERENCES edge_types(id)
);

-- Данные

INSERT INTO users (email, password_hash, role) VALUES
('client@example.com', 'hash1', 'customer'),
('manager@example.com', 'hash2', 'manager');

INSERT INTO categories (name) VALUES
('Дом'),
('Офис'),
('Детская');

INSERT INTO materials (model, fabric, country) VALUES
('Classic', 'Шерсть', 'Турция'),
('Modern', 'Синтетика', 'Китай'),
('Eco', 'Бамбук', 'Индия');

INSERT INTO carpets (name, image_url, category_id, material_id, price_per_m2) VALUES
('Ковер A', 'a.jpg', 1, 1, 1200.00),
('Ковер B', 'b.jpg', 2, 2, 850.00),
('Ковер C', 'c.jpg', 3, 3, 1000.00);

INSERT INTO edge_types (name, image_url) VALUES
('Без окантовки', 'no_edge.jpg'),
('Шелковая', 'silk_edge.jpg'),
('Хлопковая', 'cotton_edge.jpg');

