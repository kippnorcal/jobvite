USE Cust14315

ALTER TABLE custom.jobvite_full ADD [source] VARCHAR(MAX) NULL;

ALTER TABLE custom.jobvite_full
    ADD [exempt_status] VARCHAR(MAX),
        [offer_1] VARCHAR(MAX),
        [offer_2] VARCHAR(MAX),
        [assigned_pay_location] VARCHAR(MAX)

ALTER TABLE custom.jobvite_full ADD [startDate] VARCHAR(MAX) NULL;
