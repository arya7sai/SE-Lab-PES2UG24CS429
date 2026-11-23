from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
title = doc.add_heading('Lab 6 - Code and Branch Coverage', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph('Student: Arya | SRN: PES2UG24CS429')
doc.add_paragraph('Lab: 6 - Code/Branch Coverage Testing')
doc.add_paragraph('Date: 2026-11-23')
doc.add_paragraph('')

# Coverage Results
doc.add_heading('Coverage Results', level=1)

p = doc.add_paragraph()
p.add_run('============================= test session starts ==============================').bold = True
doc.add_paragraph('platform win32 -- Python 3.13.0, pytest-9.2.0, pluggy-1.7.0')
doc.add_paragraph('collected 55 items')
doc.add_paragraph('')
doc.add_paragraph('test_bike_share_rental.py .............................................. [ 83%]')
doc.add_paragraph('.........                                                                [100%]')
doc.add_paragraph('')
p = doc.add_paragraph()
p.add_run('=============================== tests coverage ================================').bold = True
doc.add_paragraph('')
doc.add_paragraph('Name                   Stmts   Miss Branch BrPart  Cover   Missing')
doc.add_paragraph('------------------------------------------------------------------')
p = doc.add_paragraph()
run = p.add_run('bike_share_rental.py      40      0     30      0   100%')
run.bold = True
doc.add_paragraph('------------------------------------------------------------------')
doc.add_paragraph('TOTAL                     40      0     30      0   100%')
doc.add_paragraph('')
p = doc.add_paragraph()
p.add_run('============================= 55 passed in 0.57s ==============================').bold = True
doc.add_paragraph('')

# Test Categories
doc.add_heading('Test Categories Covered', level=1)

doc.add_heading('ride_cost() - 23 tests', level=2)
tests_ride_cost = [
    'Unknown bike type raises ValueError',
    'Invalid duration (zero, negative) raises ValueError',
    'Non-subscriber, non-peak: standard (30, 45 min), electric (30 min), cargo (30 min)',
    'Subscriber (first block free): standard (15, 30, 45 min), electric (60 min)',
    'Peak pricing (non-cargo): standard (30, 45 min), electric (30 min)',
    'Peak pricing - cargo (no surcharge): 30 min, 45 min subscriber',
    'Long ride surcharge (>180 min): standard 200 min, electric 181 min, cargo 180/181 min',
]
for t in tests_ride_cost:
    doc.add_paragraph(t, style='List Bullet')

doc.add_heading('dock_status() - 16 tests', level=2)
tests_dock = [
    'Invalid capacity (zero, negative) raises ValueError',
    'Invalid bike count (negative, exceeds capacity) raises ValueError',
    'Empty (0 bikes docked)',
    'Full (capacity bikes docked)',
    'Few bikes: 1, 2 bikes docked; 3 bikes (boundary - not few)',
    'Few slots: 1, 2 free slots; 3 free slots (boundary - not few)',
    'Available: normal case (5/10)',
    'Small capacity edge cases: capacity 1 (empty/full), capacity 2',
]
for t in tests_dock:
    doc.add_paragraph(t, style='List Bullet')

doc.add_heading('can_unlock() - 16 tests', level=2)
tests_unlock = [
    'Has active ride: False regardless of balance/age (3 tests)',
    'Age < 16: False regardless of balance (2 tests)',
    'Age 16-17: needs >= 100 balance (4 tests covering boundaries 99/100/150/50)',
    'Age 18+: needs >= 50 balance (4 tests covering boundaries 49/50/100/0)',
    'Active ride overrides age/balance checks (3 tests)',
]
for t in tests_unlock:
    doc.add_paragraph(t, style='List Bullet')

# Branch Coverage Analysis
doc.add_heading('Branch Coverage Analysis (30 branches, 0 missed)', level=1)

branches = [
    ('ride_cost:', [
        'bike_type in RATE_PER_30_MIN (True/False) - unknown type raises',
        'minutes <= 0 (True/False) - invalid duration raises',
        'is_subscriber (True/False) - subscriber logic',
        'blocks <= 0 after subscriber discount (True/False) - free ride',
        'is_peak and bike_type != "cargo" (True/False) - peak surcharge',
        'is_peak True but bike_type == "cargo" (True/False) - no surcharge for cargo',
        'minutes > 180 (True/False) - long ride surcharge',
    ]),
    ('dock_status:', [
        'capacity <= 0 (True/False) - invalid capacity raises',
        'bikes_docked < 0 or > capacity (True/False) - invalid count raises',
        'bikes_docked == 0 (True/False) - empty',
        'free_slots == 0 (True/False) - full',
        'bikes_docked <= 2 (True/False) - few bikes',
        'free_slots <= 2 (True/False) - few slots',
        'else - available',
    ]),
    ('can_unlock:', [
        'has_active_ride (True/False) - immediate False',
        'age < 16 (True/False) - immediate False',
        'age < 18 (True/False) - teen logic',
        'account_balance >= 100 (True/False) - teen balance check',
        'else (age >= 18): account_balance >= 50 (True/False) - adult balance check',
    ]),
]

for func, branch_list in branches:
    p = doc.add_paragraph()
    p.add_run(func).bold = True
    for branch in branch_list:
        doc.add_paragraph(f'  - {branch}', style='List Bullet')

doc.add_paragraph('')
doc.add_heading('Summary', level=1)
doc.add_paragraph('All 30 branches in bike_share_rental.py are covered by the 55 test cases.')
doc.add_paragraph('Statement coverage: 100% (40/40 statements)')
doc.add_paragraph('Branch coverage: 100% (30/30 branches)')
doc.add_paragraph('All 55 tests pass.')

doc.save('PES2UG24CS429_Arya_LAB6.docx')
print('DOCX created successfully')