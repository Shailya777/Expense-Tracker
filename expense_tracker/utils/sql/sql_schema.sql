-- Creating Main Tables of the Expense Tracker DB Schema:

-- USER Table:
create table if not exists users (
	user_id int primary key auto_increment,
    email varchar(255) unique not null,
    password_hash varchar(255) not null,
    user_role enum('user','admin') default 'user',
    created_at timestamp default current_timestamp
    );
    
-- ACCOUNTS Table:
create table if not exists accounts (
	account_id int primary key auto_increment,
    user_id int not null,
    account_name varchar(100),
    balance decimal(12,2) default 0,
    account_type enum('cash', 'bank', 'creditcard') not null,
    created_at timestamp default current_timestamp,
    foreign key (user_id) references users(user_id) on delete cascade
);

-- CATEGORIES Table:
create table if not exists categories (
	category_id int primary key auto_increment,
    category_name varchar(255) not null,
    parent_id int default null,
    is_income boolean default false,
    foreign key (parent_id) references categories(category_id)
);

-- MERCHANTS table:
create table if not exists merchants (
	merchant_id int primary key auto_increment,
    merchant_name varchar(255) unique not null
);

-- TRANSACTIONS Table:
create table if not exists transactions (
	transaction_id int primary key auto_increment,
    account_id int not null,
    category_id int not null,
    merchant_id int not null,
    amount decimal(12,2) not null,
    transaction_date date not null,
    transaction_desc varchar(255),
    transaction_type enum('expense', 'income') not null,
    created_at timestamp default current_timestamp,
    foreign key (account_id) references accounts(account_id) on delete cascade,
    foreign key (category_id) references categories(category_id) on delete cascade,
    foreign key (merchant_id) references merchants(merchant_id) on delete cascade
);

-- BUDGETS Table:
create table if not exists budgets (
	budget_id int primary key auto_increment,
    user_id int not null,
    category_id int not null,
    amount decimal(12,2) not null,
    budget_month int not null,
    budget_year int not null,
    foreign key (user_id) references users(user_id) on delete cascade,
    foreign key (category_id) references categories(category_id) on delete cascade,
    unique (user_id, category_id, budget_month, budget_year)
);

-- AUDIT LOG Table:
create table if not exists audit_log (
	audit_id int primary key auto_increment,
    user_id int,
    user_action varchar(255),
    audit_timestamp timestamp default current_timestamp,
    foreign key (user_id) references users(user_id)
);