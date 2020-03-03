-- all records returned with openlow_spread, ten_day_max, and ten_day_max_time;
create view base_table as
	select *, (lowmid <= (select min(lowmid) from eur_usd eu2
						where eu2.time between e.time and e.ten_day_max_time)) entry_bottom,
			  (highmid >= (select max(highmid) from eur_usd eu2
			  			where eu2.time between e.time and e.ten_day_max_time)) entry_top
	from ( 
		-- select *, (select eu2.time from eur_usd eu2 where d.ten_day_max = highmid ) ten_day_max_time
		select *, (select eu2.time from eur_usd eu2
			where d.ten_day_max = highmid 
			and eu2.time between d.time and (d.time + 12) limit 1) ten_day_max_time,
			(select eu3.time from eur_usd eu3 
			where d.ten_day_min = lowmid 
			and eu3.time between d.time and (d.time + 12) limit 1) ten_day_min_time
		from (
			select *, ((openmid - lowmid) * 10) openlow_spread,
			((highmid - openmid) * 10) openhigh_spread,
			max(highmid) over(rows between current row and 10 following) ten_day_max,
			min(lowmid) over(rows between current row and 10 following ) ten_day_min
			from eur_usd eu 	
		) as d
	) as e

drop view base_table;

select * from base_table;

select time 
from base_table 
where (ten_day_max - openmid) > openlow_spread
and




