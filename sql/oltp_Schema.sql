CREATE TABLE address (
    address_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    street VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    state VARCHAR,
    postal_code VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    row_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE users (
    user_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    address_id BIGINT REFERENCES address(address_id),
    phone_number VARCHAR,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    row_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE products (
    product_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    sku VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    category VARCHAR,
    price NUMERIC(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    row_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    shipping_address_id BIGINT NOT NULL REFERENCES address(address_id),
    billing_address_id BIGINT NOT NULL REFERENCES address(address_id),
    order_status VARCHAR NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL,
    row_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    order_id BIGINT NOT NULL REFERENCES orders(order_id),
    product_id BIGINT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    row_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    order_id BIGINT NOT NULL REFERENCES orders(order_id),
    payment_method VARCHAR NOT NULL,
    payment_status VARCHAR NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    row_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);
