delimiter $$

-- Function to Get First Day of The Month Given any Date:
create function fn_month_start(p_date date)
returns date
deterministic
begin
	return date_format(p_date, '%Y-%m-01');
end $$