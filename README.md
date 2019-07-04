# MDFDatabase

Summer internship project to build comprehensive database of EEE department classes. Includes two primary modules, parser and database. 

The Parser module utilises the PyPDF2 library in order to convert MDF PDFs into plaintext, then compares them with pre-formatted blank MDFs in order to determine which of the several formats is in use. It then uses the relevant schema to dump data from the fields of the PDF into the approximately correct fields of the database. Some supervision is required in order to ensure that reasonable data is placed into the database. The parser tries to default to putting dubious information into the text fields.

The database is a fully normalised SQL DB, consisting of three primary tables, Classes, Courses and Staff. In order to comply with normalisation, relationships between or within these tables such as class assignments for lecturers or class pre-requisites are modelled using additional tables for only that relationship. This increases the integrity of the data but does slow database access.

