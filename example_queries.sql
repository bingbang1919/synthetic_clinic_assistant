-- Dataset reference date: 2026-10-13.
-- Count patients with recorded Type 2 diabetes.
SELECT COUNT(DISTINCT pc.patient_id) AS patient_count
FROM patient_condition pc JOIN condition c ON c.condition_id=pc.condition_id
WHERE c.condition_name='Type 2 diabetes';

-- Provider with the most visits last month (September 2026).
SELECT p.provider_name, COUNT(*) AS visit_count
FROM visit v JOIN provider p ON p.provider_id=v.provider_id
WHERE v.visit_date >= date('2026-10-13','start of month','-1 month')
AND v.visit_date < date('2026-10-13','start of month')
GROUP BY p.provider_id,p.provider_name ORDER BY visit_count DESC,p.provider_id LIMIT 1;

-- Average completed age of patients with asthma.
SELECT ROUND(AVG(CAST(strftime('%Y','2026-10-13') AS INTEGER)
- CAST(strftime('%Y',p.date_of_birth) AS INTEGER)
- (strftime('%m-%d','2026-10-13') < strftime('%m-%d',p.date_of_birth))),2) AS average_age
FROM patient p JOIN patient_condition pc ON pc.patient_id=p.patient_id
JOIN condition c ON c.condition_id=pc.condition_id WHERE c.condition_name='Asthma';

-- Common active prescriptions among patients with hypertension.
SELECT m.medication_name, COUNT(DISTINCT rx.patient_id) AS patient_count
FROM prescription rx JOIN medication m ON m.medication_id=rx.medication_id
JOIN patient_condition pc ON pc.patient_id=rx.patient_id
JOIN condition c ON c.condition_id=pc.condition_id
WHERE c.condition_name='Hypertension' AND rx.start_date <= '2026-10-13'
AND (rx.end_date IS NULL OR rx.end_date >= '2026-10-13')
GROUP BY m.medication_id,m.medication_name ORDER BY patient_count DESC,m.medication_name;
