from django.db import models


class Semester(models.TextChoices):
    ONE = '1', '1'
    ONETWO = '4', '1/2'
    TWO = '2', '2'
    TWOTHREE = '5', '2/3'
    THREE = '3', '3'
    ALL = '6', '1/2/3'

ReducedSemester = [Semester.choices[0], Semester.choices[2], Semester.choices[4]]

class Week(models.TextChoices):
    ONE = '1', '1'
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'
    SIX = '6', '6'
    SEVEN = '7', '7'
    EIGHT = '8', '8'
    NINE = '9', '9'
    TEN = '10', '10'
    ELEVEN = '11', '11'
    EXAM = 'E', 'Exam Period'


class StaffRoles(models.TextChoices):
    REGISTRAR = '1', 'IC'
    LECTURER = '2', 'L'
    ASSISTANT = '3', 'A'
    MARKER = '4', 'Ma'
    MODERATOR = '5', 'Moderator'
    YEAR_ADVISOR = '6', 'Year Advisor'
    COURSE_DIRECTOR = '7', 'Course Director'

class Levels(models.TextChoices):
    ONE = '1', '1'
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'
    NINE = '9', '9'


class ElectiveOptions(models.TextChoices):
    NE = '1', 'Compulsory'
    PE = '2', 'Optional'
