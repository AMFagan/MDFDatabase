import PyPDF2
import re


class MDF:
    module_code = None
    module_title = None
    module_registrar = None
    other_staff = []
    credits = None
    semester = None
    coe = None
    level = None
    pre_requisites = {'strict': [], 'recommended': [], 'other': []}
    delivery = {'lectures': None, 'tutorial': None, 'assignments': None, 'laboratories': None, 'private study': None,
                'total': None}
    aims = ''
    learning_outcomes = ''
    syllabus = ''
    assessment = None
    deadlines = None
    resit = None
    additional_comments = ''
    reading_list = None

    def __str__(self):
        return (("%s\t%s\n" * 4) + ("%s\n" * 12)) % (
            "Module code: %s" % self.module_code,
            "Module title: %s" % self.module_title,
            "Module registrar: %s" % self.module_registrar,
            "Other staff: %s" % self.other_staff,
            "Credits: %s" % self.credits,
            "Semester: %s" % self.semester,
            "Compulsory/Optional/Elective: %s" % self.coe,
            "Academic level %s" % self.level,
            "Required Classes: %s" % self.pre_requisites['strict'],
            "Recommended Classes: %s" % self.pre_requisites['recommended'],
            "Other Requirements: %s" % self.pre_requisites['other'],
            "Delivery: %s" % self.delivery,
            "Aims : %s" % self.aims,
            "Learning Outcomes: %s" % self.learning_outcomes,
            "Syllabus: %s" % self.syllabus,
            "Assessment: %s" % self.assessment,
            "Deadlines: %s" % self.deadlines,
            "Resit Procedure: %s" % self.resit,
            "Additional Comments: %s" % self.additional_comments,
            "Recommended Reading: %s" % self.reading_list,
        )

    def __init__(self, tup):
        self.module_code = str(tup[0])
        self.module_title = str(tup[1])
        self.module_registrar = tup[2]
        self.other_staff += ("" or tup[3]).split(',')
        self.credits = int(tup[4] or 0)
        self.semester = int(tup[5] or 0)
        self.coe = tup[6] or ""
        self.level = tup[7] or 0
        self.pre_requisites['other'] += ([] if tup[8] is None else [tup[8]])
        self.delivery['lectures'] = (tup[9] or "").strip().split(" ")[0]
        self.delivery['tutorial'] = (tup[9] or "").strip().split(" ")[1]
        self.delivery['assignments'] = (tup[9] or "").strip().split(" ")[2]
        self.delivery['laboratories'] = (tup[9] or "").strip().split(" ")[3]
        self.delivery['private study'] = (tup[9] or "").strip().split(" ")[4]
        self.delivery['total'] = (tup[9] or "").strip().split(" ")[5]

        self.aims = tup[10] or ""
        self.learning_outcomes = tup[11] or ""
        self.syllabus = tup[12] or ""

        self.assessment = tup[13] or ""
        self.deadlines = tup[14] or ""
        self.resit = tup[15] or ""
        self.additional_comments = tup[16] or ""
        self.reading_list = tup[17] or ""


with open('MDFs/PH167-md.pdf', 'rb') as pdf:
    reader = PyPDF2.PdfFileReader(pdf)
    out = ''
    for p in reader.pages:
        out += p.extractText()
    out = out.replace('\n', '').replace(u'\u2122', '\'')

    with open('PH167_template.txt', 'r') as template:
        reg = template.read()
        re.DOTALL = True
        # re.DEBUG = True
        # print(reg)
        print("starting comparison")
        thing = re.match(reg, out)
        if thing:
            print("success")
            mdf = MDF(thing.group(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18))
            print(str(mdf))
        else:
            print("failure")

    with open('output.txt', 'w') as output:
        output.write(out)
