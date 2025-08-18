CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS time_series (
    id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    series_id VARCHAR(255) NOT NULL,
    version VARCHAR(32) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(series_id, version)
);

CREATE TABLE IF NOT EXISTS data_points (
    id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    time_series_id UUID REFERENCES time_series(id) ON DELETE CASCADE,
    timestamp INT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(time_series_id, timestamp)
);

CREATE TABLE IF NOT EXISTS model_version (
    id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    time_series_id UUID REFERENCES time_series(id) ON DELETE CASCADE,
    version VARCHAR(32) NOT NULL,
    mean DOUBLE PRECISION NOT NULL,
    std DOUBLE PRECISION NOT NULL,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(time_series_id, version)
);