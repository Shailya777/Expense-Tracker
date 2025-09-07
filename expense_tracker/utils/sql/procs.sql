delimiter $$

-- Stored Procedure to Insert Transactions and Update Account Balance:
create procedure sp_post_transaction(
	in p_account_id int,
    in p_category_id int,
    in p_merchant_id int,
    in p_amount decimal(12,2),
    in p_date date,
    in p_description varchar(255),
    in p_transaction_type enum('expense', 'incomr')
    )
begin
	declare v_new_balance decimal(12,2);
    
	insert into transactions (
		account_id, category_id, merchant_id,
        amount, transaction_date, transaction_desc,
        transaction_type)
	values (p_account_id, p_category_id, p_merchant_id,
		p_amount, p_date, p_description, p_transaction_type);
        
	select balance into v_new_balance from accounts
    where account_id = p_account_id for update;
    
    if p_transaction_type = 'expense' then
		set v_new_balance = v_new_balance - p_amount;
	else
		set v_new_balance = v_new_balance + p_amount;
	end if;
    
    update accounts
    set balance = v_new_balance
    where account_id = p_account_id;
end $$

-- Stored Procedure to Upsert Budgets:
create procedure sp_upsert_budget(
	in p_user_id int,
    in p_category_id int,
    in p_amount decimal(12,2),
    in p_month int,
    in p_year int
	)
begin
	if exists(
		select 1 from budgets
        where user_id = p_user_id
        and category_id = p_category_id
        and budget_month = p_month
        and budget_year = p_year)
	then
		update budgets
        set amount = p_amount
        where user_id = p_user_id
        and category_id = p_category_id
        and budget_month = p_month
        and budget_year = p_year;
	else
		insert into budgets (
			user_id, category_id, amount,
            budget_month, budget_year)
		values (
			p_user_id, p_category_id, p_amount,
            p_month, p_year);
	end if;
end $$

delimiter ;