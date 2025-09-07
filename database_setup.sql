-- Create database
CREATE DATABASE analytics_demo;

-- Connect to database
\c analytics_demo;

-- Create tables
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE sales_data (
    sale_id SERIAL PRIMARY KEY,
    region_id INTEGER REFERENCES regions(region_id),
    product_id INTEGER REFERENCES products(product_id),
    sale_date DATE NOT NULL,
    revenue DECIMAL(10,2) NOT NULL,
    forecast DECIMAL(10,2) NOT NULL,
    units_sold INTEGER NOT NULL
);

-- Insert sample data
INSERT INTO regions (region_name) VALUES
('North America'), ('Europe'), ('Asia Pacific'), ('Latin America');

INSERT INTO products (product_name, category) VALUES
('Laptop Pro', 'Electronics'),
('Smartphone X', 'Electronics'),
('Tablet Plus', 'Electronics'),
('Wireless Headphones', 'Accessories'),
('Smart Watch', 'Wearables');

-- Insert 1000 sample sales records
INSERT INTO sales_data (region_id, product_id, sale_date, revenue, forecast, units_sold)
SELECT
    (RANDOM() * 3 + 1)::INTEGER,
    (RANDOM() * 4 + 1)::INTEGER,
    DATE '2024-01-01' + (RANDOM() * 365)::INTEGER,
    (RANDOM() * 50000 + 10000)::DECIMAL(10,2),
    (RANDOM() * 45000 + 12000)::DECIMAL(10,2),
    (RANDOM() * 100 + 10)::INTEGER
FROM generate_series(1, 1000);