# Clinic SQL Q&A Results of All 20 Questions

--- Question 1 --- 
Q: How many patients do we have? 
{ "sql": "select
count(id) from patients;", "rows": \[\[200\]\] }

--- Question 2 --- 
Q: List all doctors and their specializations 
{
"sql": "select name, specialization from doctors", "rows":
\[\["Dr. Pooja","Dermatology"\],\["Dr. Pooja","Cardiology"\],\["Dr. Anjali","Orthopedics"\],\["Dr. Ravi","General"\],\["Dr. Neha","Pediatrics"\],\["Dr. Vikram","Dermatology"\],\["Dr. Priya","Cardiology"\],\["Dr. Priya","Orthopedics"\],\["Dr. Amit","General"\],\["Dr. Priya","Pediatrics"\],\["Dr. Anjali","Dermatology"\],\["Dr. Vikram","Cardiology"\],\["Dr. Anjali","Orthopedics"\],\["Dr. Pooja","General"\],\["Dr. Sneha","Pediatrics"\]\]
}

--- Question 3 --- 
Q: Show me appointments for last month 
{ "sql":
"select \* from appointments where strftime('%y-%m', appointment_date) =
strftime('%y-%m', 'now', '-1 month')", "rows": \[\] }

--- Question 4 --- 
Q: Which doctor has the most appointments? 
{ "sql":
"select d.name from doctors d join appointments a on d.id = a.doctor_id
group by d.id order by count(a.id) desc limit 1;", "rows":
\[\["Dr. Priya"\]\] }

--- Question 5 --- 
Q: What is the total revenue? 
{ "sql": "select
sum(paid_amount) from invoices", "rows": \[\[387809.0\]\] }

--- Question 6 --- 
Q: Show revenue by doctor 
{ "sql": "select d.name as
doctor_name, sum(t.cost) as total_revenue from doctors d join
appointments a on d.id = a.doctor_id join treatments t on a.id =
t.appointment_id group by d.name;", "rows":
\[\["Dr. Amit",92701.0\],\["Dr. Anjali",147555.0\],\["Dr. Neha",43712.0\],\["Dr. Pooja",165224.0\],\["Dr. Priya",124175.0\],\["Dr. Ravi",68045.0\],\["Dr. Sneha",98718.0\],\["Dr. Vikram",159191.0\]\]
}

--- Question 7 --- 
Q: How many cancelled appointments last quarter? 
{
"sql": "select count(id) from appointments where status = 'cancelled'
and appointment_date between (case when cast(strftime('%m','now') as
integer) between 1 and 3 then strftime('%y',date('now','-1
year'))\|\|'-10-01' when cast(strftime('%m','now') as integer) between 4
and 6 then strftime('%y','now')\|\|'-01-01' when
cast(strftime('%m','now') as integer) between 7 and 9 then
strftime('%y','now')\|\|'-04-01' when cast(strftime('%m','now') as
integer) between 10 and 12 then strftime('%y','now')\|\|'-07-01' end)
and (case when cast(strftime('%m','now') as integer) between 1 and 3
then strftime('%y',date('now','-1 year'))\|\|'-12-31' when
cast(strftime('%m','now') as integer) between 4 and 6 then
strftime('%y','now')\|\|'-03-31' when cast(strftime('%m','now') as
integer) between 7 and 9 then strftime('%y','now')\|\|'-06-30' when
cast(strftime('%m','now') as integer) between 10 and 12 then
strftime('%y','now')\|\|'-09-30' end)", "rows": \[\[0\]\] }

--- Question 8 --- 
Q: Top 5 patients by spending 
{ "sql": "select
p.first_name,p.last_name,sum(i.total_amount) as total_spending from
patients p join invoices i on p.id=i.patient_id group by
p.id,p.first_name,p.last_name order by total_spending desc limit 5;",
"rows":
\[\["Rahul","Gupta",21082.0\],\["Kiran","Nair",16237.0\],\["Vikram","Nair",14193.0\],\["Rahul","Sharma",13945.0\],\["Vikram","Kumar",13624.0\]\]
}

--- Question 9 --- 
Q: Average treatment cost by specialization 
{ "sql":
"select d.specialization,avg(t.cost) as average_treatment_cost from
treatments t join appointments a on t.appointment_id=a.id join doctors d
on a.doctor_id=d.id group by d.specialization;", "rows":
\[\["Cardiology",2446.25\],\["Dermatology",2827.0571\],\["General",2558.03\],\["Orthopedics",2452.07\],\["Pediatrics",2585.53\]\]
}

--- Question 10 --- 
Q: Show monthly appointment count for the past 6 months 
{
"sql": "select strftime('%y-%m',appointment_date) as
appointment_month,count(id) from appointments where
appointment_date\>=date('now','-6 months') group by appointment_month
order by appointment_month;", "rows": \[\[null,239\]\] }

--- Question 11 --- 
Q: Which city has the most patients? 
{ "sql":
"select city from patients group by city order by count(id) desc limit
1;", "rows": \[\["Hyderabad"\]\] }

--- Question 12 --- 
Q: List patients who visited more than 3 times
{ "sql":
"select p.id,p.first_name,p.last_name from patients p join appointments
a on p.id=a.patient_id group by p.id,p.first_name,p.last_name having
count(a.id)\>3;", "rows":
\[\[10,"Sneha","Das"\],\[11,"Priya","Yadav"\]\] }

--- Question 13 --- 
Q: Show unpaid invoices 
{ "sql": "select \* from
invoices where status='unpaid';", "rows": \[\] }

--- Question 14 --- 
Q: What percentage of appointments are no-shows? 
{ "sql": "select
cast(sum(case when status='no-show' then 1 else 0 end) as
real)*100/count(*) from appointments;", "rows": \[\[0.0\]\] }

--- Question 15 --- 
Q: Show the busiest day of the week for appointments 
{ "sql": "select case
strftime('%w',appointment_date) when '0' then 'sunday' when '1' then
'monday' when '2' then 'tuesday' when '3' then 'wednesday' when '4' then
'thursday' when '5' then 'friday' when '6' then 'saturday' end as
day_of_week from appointments group by day_of_week order by count(\*)
desc limit 1;","rows": \[\["sunday"\]\] }

--- Question 16 --- 
Q: Revenue trend by month
{ "sql": "select
strftime('%y-%m',invoice_date),sum(total_amount) from invoices group by
1 order by 1;", "rows": \[\[null,801721.0\]\] }

--- Question 17 --- 
Q: Average appointment duration by doctor 
{ "sql": "select
d.name,avg(t.duration_minutes) from doctors d join appointments a on
d.id=a.doctor_id join treatments t on a.id=t.appointment_id group by
d.id,d.name;", "rows": \[\["Dr. Pooja",68.89\],\["Dr. Anjali",69.10\]\]
}

--- Question 18 --- 
Q: List patients with overdue invoices
{ "sql": "select
distinct p.id,p.first_name,p.last_name from patients p join invoices i
on p.id=i.patient_id where i.total_amount\>i.paid_amount and i.status
not in ('paid','cancelled');", "rows":
\[\[186,"Neha","Das"\],\[150,"Rahul","Sharma"\]\] }

--- Question 19 --- 
Q: Compare revenue between departments 
{ "sql": "select
d.department,sum(t.cost) from doctors d join appointments a on
d.id=a.doctor_id join treatments t on a.id=t.appointment_id group by
d.department order by 2 desc;", "rows": \[\["Dermatology
Dept",259464.0\],\["Cardiology Dept",186421.0\]\] }

--- Question 20 --- 
Q: Show patient registration trend by month
{ "sql": "select
strftime('%y-%m',registered_date),count(id) from patients group by 1
order by 1;", "rows": \[\[null,200\]\] }
