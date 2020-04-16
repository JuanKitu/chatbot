CREATE TABLE PREDEFINEDQUESTIONS (ID serial PRIMARY KEY, QUESTION varchar(1000), EXPRESSION varchar (1000));

INSERT INTO PREDEFINEDQUESTIONS (QUESTION,EXPRESSION) VALUES
('¿Cuáles son los requisitos para ser alumno regular?','{requisitos| necesita |pautas| cuáles+puntos| cuándo |qué}+ alum+regular'),
('¿Cuántas veces se puede rendir un final?','{veces|cuándo + recursar} + final')