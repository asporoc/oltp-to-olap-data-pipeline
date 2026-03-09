CREATE TABLE raw.address (
	raw_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    address_id BIGINT,
    street VARCHAR,
    city VARCHAR,
    state VARCHAR,
    postal_code VARCHAR,
    country VARCHAR,
    row_hash TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    is_deleted BOOLEAN,
    ingested_at TIMESTAMPTZ DEFAULT now()
   );

CREATE TABLE raw.users (
	raw_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT,
    email VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    address_id BIGINT,
    phone_number VARCHAR,
    is_deleted BOOLEAN,
    row_hash TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE raw.products (
	raw_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    product_id BIGINT,
    sku VARCHAR,
    name VARCHAR,
    category VARCHAR,
    price NUMERIC(10,2),
    is_active BOOLEAN,
    row_hash TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE raw.orders (
	raw_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    order_id BIGINT,
    user_id BIGINT,
    shipping_address_id BIGINT,
    billing_address_id BIGINT,
    order_status VARCHAR,
    total_amount NUMERIC(12,2),
    row_hash TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    is_deleted BOOLEAN,
    ingested_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE raw.order_items (
	raw_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    order_item_id BIGINT,
    order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    unit_price NUMERIC(10,2),
    row_hash TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    is_deleted BOOLEAN,
    ingested_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE raw.payments (
	raw_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    payment_id BIGINT,
    order_id BIGINT,
    payment_method VARCHAR,
    payment_status VARCHAR,
    amount NUMERIC(12,2),
    row_hash TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    is_deleted BOOLEAN,
    ingested_at TIMESTAMPTZ DEFAULT now()
);