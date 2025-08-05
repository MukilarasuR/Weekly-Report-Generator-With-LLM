-- Project Table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255),
    project_manager_id INT,
    status VARCHAR(50),
    start_date DATE,
    end_date DATE,
    budget BIGINT
);

-- Phase Table
CREATE TABLE phases (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id),
    phase_name VARCHAR(255),
    status VARCHAR(50),
    budget BIGINT
);

-- Task Table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    phase_id INT REFERENCES phases(id),
    name VARCHAR(255),
    status VARCHAR(50),
    estimated_budget BIGINT,
    actual_budget BIGINT
);

-- Finance Request Table
CREATE TABLE finance_requests (
    id SERIAL PRIMARY KEY,
    fk_project_id INT REFERENCES projects(id),
    requested_amount DECIMAL,
    approved_amount DECIMAL
);


-- Insert Project
INSERT INTO projects (project_name, project_manager_id, status, start_date, end_date, budget)
VALUES ('Mall Construction', 1, 'in_progress', '2024-01-10', '2025-12-31', 50000000);

-- Insert Phases
INSERT INTO phases (project_id, phase_name, status, budget)
VALUES 
(1, 'Foundation', 'completed', 10000000),
(1, 'Structural Work', 'in_progress', 15000000),
(1, 'Interiors', 'not_started', 25000000);

-- Insert Tasks
INSERT INTO tasks (phase_id, name, status, estimated_budget, actual_budget)
VALUES 
(1, 'Lay foundation', 'completed', 10000000, 10000000),
(1, 'Waterproofing base', 'completed', 1500000, 1500000),
(2, 'Concrete frame setup', 'in_progress', 2000000, 500000),
(2, 'Beam testing', 'not_started', 0, 0),
(3, 'HVAC Layout', 'not_started', 0, 0);

-- Insert Finance Requests
INSERT INTO finance_requests (fk_project_id, requested_amount, approved_amount)
VALUES 
(1, 2000000, 500000);
