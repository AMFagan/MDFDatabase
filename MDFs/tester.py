from typing import Tuple, List

class Template():
    data = []
    replacements = {}
    def __init__(self, address: str) -> 'Template':
        with open(address) as f:
            for l in f:
                self.data += [l]

    def replace(self, find: str, replace: str) -> 'Template':
        self.replacements[find] = replace
        return self

    def __add__(self, t: Tuple[str, str]) -> 'Template':
        self.replace(t[0], t[1])
        return self

    def execute(self) -> 'Template':
        for i in range(len(self.data)):
            for k in self.replacements:
                self.data[i] = self.data[i].replace(k, self.replacements[k])
        return self

    def write(self, address: str) -> None:
        with open(address, mode='w') as out:
            [out.write(l) for l in self.data]

    def __mul__(self, address: str) -> None:
        self.execute().write(address)

    def replace_many(self, *args: List[Tuple[str, str]]) -> 'Template':
        for a in args:
            self.__add__(a)
        return self

        

def rewrite():
    t = (
            Template('EE107-MDF 2018-19_edit.htm')
            + ('{CODE}', 'EE107')
            + ('{NAME}', 'Electronic and Electrical Principles 1')
            + ('{REGISTRAR}', 'Dr. Phil McGlone')
            + ('{OTHERS}', ', '.join(['Dr. Mark Wilson', 'Morag MacDougall']))
            + ('{C}', '20')
            + ('{SEM}', '1/2')
            + ('{E}', 'NE')
            + ('{LEVEL}', '1')
            + ('{REQS}', 'Higher Physics and Maths, or equivalents')
            + ('{AIMS}', '''
                         Develop a firm grounding in the understanding, analysis
                         and design of analogue and digital circuits.
                         ''')
            + ('{OUTCOMES}', '''
                             LO 1: Demonstrate the ability to apply fundamental
                             circuit analysis techniques to DC and AC circuits.<br>
                             LO 2: Understand the fundamentals of amplifiers and
                             feedback, and the basic principles and design of
                             operational amplifier circuits.<br>
                             LO 3: Demonstrate an understanding of combinational
                             logic circuit design, analysis and synthesis.<br>
                             LO 4: Understand the behaviour, design and application
                             of specific combinational and sequential logic circuits.
                             ''')
            + ('{SYLLABUS}', '''
                             Fundamentals:- Units of measurement, SI units, symbols
                             and notations; charge flow and current; voltage drop;
                             resistivity, resistance and Ohm’s law, I-V
                             characteristics of resistors; I-V characteristics of
                             non-linear devices; open and short circuits; power
                             and energy.<br>
                             DC Circuits:- Kirchhoff’s laws; the application of
                             Ohm’s and Kirchhoff’s laws to DC circuit analysis,
                             series, parallel and series-parallel resistive
                             circuits; voltage division and current division;
                             Thévenin’s Theorem, Norton’s Theorem and source
                             conversion; maximum power transfer theorem; circuit
                             analysis using superposition; mesh analysis of
                             circuits.<br>
                             AC Circuits:- Phasors and complex algebra; properties
                             of capacitors and inductors; reactance of capacitors
                             and inductors; impedance and admittance; phasor
                             diagrams; extension of DC circuit analysis techniques
                             to AC circuits; RMS values, power and energy, power
                             factor.<br>
                             Passive Circuits:- Input impedance; output impedance;
                             insertion losses; voltage transfer function, frequency
                             response of magnitude and phase.<br>
                             Amplifier Fundamentals:- Gain, input and output impedance;
                             amplifier modelling; amplifiers in cascade; frequency response.
                             Feedback:- Introduction to negative feedback, multiple
                             feedback configurations.<br>
                             Operational Amplifiers:- Introduction to the
                             operational amplifier, the differential stage,
                             inverting and non-inverting configurations, common
                             amplifier circuits.<br>
                             Introduction to Digital Systems:- Binary, decimal and
                             hexadecimal numbering systems; arithmetical operations
                             and negative numbers in binary; comparisons and
                             relationships between analogue and digital systems.<br>
                             Digital Analysis:- Boolean algebra, Karnaugh and
                             inverse maps; minimisation of Boolean expressions,
                             basic logic gates, analysis of circuits containing
                             logic gates; timing diagrams and propagation delay.<br>
                             Design:- Design procedures; design of combinational logic
                             circuits; use of “don’t care” terms; Binary Coded Decimal
                             (BCD); minterms and maxterms; design of circuits
                             containing only NAND or only NOR gates; design of
                             basic digital systems.<br>
                             MSI Devices and Sequential Logic:- Introduction to the
                             adder, comparator, multiplexer and decoder devices;
                             active-low and active-high inputs and outputs;
                             introduction to sequential circuits, S-R latches and
                             flip-flops, D latches and flip-flops, J-K flip-flops
                             and counters.
                             ''')
            + ('{CRITERIA}', '''
                             LO 1:<br>
                             C 1: Describe and employ circuit analysis tools such
                             as voltage and current division, Kirchhoff's laws.<br>
                             C 2: Demonstrate ability to use simplification techniques
                             such as source conversion and reduction.<br>
                             C 3: Apply mesh analysis, superposition, Thevenin's
                             and Norton's theorems to solve circuits.<br>
                             C 4: Manipulate complex numbers in the solution of
                             AC problems using phasors.<br>
                             LO 2: <br>
                             C 1: Understand the fundamentals of amplifiers and
                             feedback.<br>
                             C 2: Understand and apply top-down design to amplifier
                             circuits.<br>
                             C 3: Demonstate the ability to design operational
                             amplifier circuits.<br>
                             C 4: Analyse the behaviour of circuits by way of
                             finding their transfer function in standard form.<br>
                             LO 3: <br>
                             C 1: Understand and apply the laws of Boolean algebra
                             to simplify expressions.<br>
                             C 2: Employ truth tables, Karnaugh and inverse maps
                             to the solution of combinational logic problems.<br>
                             C 3: Analyse combinational logic circuits and build
                             Boolean expressions and truth tables describing the
                             overall behaviour.<br>
                             C 4: Apply design procedures to synthesise digital
                             circuits, including: minterms; maxterms; don’t care
                             terms; implementation using universal NAND and NOR
                             gates.<br>
                             LO 4: <br>
                             C 1: Show an understanding of various MSI circuits,
                             including adders, comparators, multiplexers,
                             decoders.<br>
                             C 2: Employ MSI circuits appropriately in the design
                             of digital circuits and solution of basic digital
                             problems.<br>
                             C 3: Show an understanding of sequential logic
                             circuits including S-R Latches, J-K flip-flops,
                             counters.<br>
                             C 4: Employ sequential logic circuits in the design
                             of digital circuits and solution of basic digital
                             problems.
                             ''')
            + ('{FEEDBACK}', '''
                             Students sit a formative class test (multiple-choice
                             quiz), via myplace in week 7 of semester 1, with
                             feedback provided by worked solutions made available
                             on myplace. Formal feedback on the summative class
                             tests is provided in lectures or tutorials. In all
                             cases, students then have the opportunity to discuss
                             the solutions with teaching staff in tutorials,
                             completing the feedback loop.
                             ''')
            + ('{DEADLINES}', '')
            + ('{RESIT}', 'Examination')
            + ('{ADDITONAL}', '''
                              The coursework consists of two summative class tests
                              - in the exam period at the end of semester 1, and
                              in week 6 of semester 2 - each worth 15% of the final
                              mark. Class tests are used to assess interim progress.
                              ''')
            + ('{READING}', '''
                            Robert L Boylestad, "Introductory Circuit Analysis",
                            Latest Edition, Pearson Education ISBN-13 978-1292098951<br>
                            Thomas L Floyd, "Digital Fundamentals", Latest Edition,
                            Pearson Education ISBN-13 978-1292075983
                            ''')
            + ('{LEC}', '66')
            + ('{TUT}', '50')
            + ('{ASS}', '')
            + ('{LAB}', '')
            + ('{STUDY}', '84')
            + ('{TOTAL}', '200')
        )   * ('out.htm')

    

FIELDS = ['{OTHERS}', '{TOTAL}', '{FEEDBACK}', '{ADDITONAL}', '{REGISTRAR}',
          '{RESIT}', '{DEADLINES}', '{CRITERIA}']


FIELDS = {
    'code': '{CODE}',
    'name': '{NAME}',
    'credits': '{C}',
    'semester': '{SEM}',
    'elective': '{E}',
    'level': '{LEVEL}',
    'aims': '{AIMS}',
    'learning_outcomes': '{OUTCOMES}',
    'syllabus': '{SYLLABUS}',
    'comments': '',
    'reading': '{READING}',
    'required_modules': '{REQS}',
    'lecture_hours': '{LEC}',
    'tutorial_hours': '{TUT}',
    'assignment_hours': '{ASS}',
    'lab_hours': '{LAB}',
    'study_hours': '{STUDY}',
    }

if __name__ == '__main__':
    rewrite()
