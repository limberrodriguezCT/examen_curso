-- src/database/schema.sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    document_number TEXT NOT NULL UNIQUE,
    gender TEXT,
    number_telephone TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    plate_number TEXT NOT NULL UNIQUE,
    chassis_number TEXT UNIQUE,
    daily_rate REAL DEFAULT 0.0,
    is_available INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_date TEXT DEFAULT CURRENT_TIMESTAMP,
    return_date TEXT,
    customer_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    total_amount REAL,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    rental_id INTEGER NOT NULL,
    FOREIGN KEY (rental_id) REFERENCES rentals(id)
);

-- Tabla de Mantenimiento (La que te está dando error)
CREATE TABLE IF NOT EXISTS maintenance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date TEXT DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    cost REAL,
    vehicle_id INTEGER NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- Insertar roles obligatorios
INSERT OR IGNORE INTO roles (id, name) VALUES (1, 'Administrador');
INSERT OR IGNORE INTO roles (id, name) VALUES (2, 'Agente');