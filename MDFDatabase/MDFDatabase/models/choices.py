from django.db import models


class Semester(models.TextChoices):
    ONE = '1', '1'
    ONETWO = '2', '1/2'
    TWO = '3', '2'
    TWOTHREE = '4', '2/3'
    THREE = '5', '3'
    ALL = '6', '1/2/3'


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
    REGISTRAR = '1', 'Class Registrar'
    LECTURER = '2', 'Lecturer'
    ASSISTANT = '3', 'Assistant'
    MARKER = '4', 'Marker'


class Levels(models.TextChoices):
    ONE = '1', '1'
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'
    NINE = '9', '9'


class ElectiveOptions(models.TextChoices):
    NE = '1', 'NE'
    PE = '2', 'PE'
    EO = '3', 'EO'
