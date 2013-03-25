select trunc(occurred_at), ip_address, count(*)
from primary_event partition (pn20120601)
where classified_by_rule_id is not null
group by trunc(occurred_at), ip_address
having count(*) >30
order by 1
