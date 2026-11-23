from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
title = doc.add_heading('Lab 4 - Vibe Coding: Chat History', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph('Student: Arya | SRN: PES2UG24CS429')
doc.add_paragraph('Lab: 4 - Vibe Coding')
doc.add_paragraph('Date: 2026-11-23')
doc.add_paragraph('Assigned Repo: https://github.com/SETAPESU26/55_card_predictor')
doc.add_paragraph('')

# Read the markdown and convert
with open('CHAT_HISTORY.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Simple markdown to docx conversion
lines = content.split('\n')
in_code_block = False
code_lines = []

for line in lines:
    if line.startswith('```'):
        if in_code_block:
            # End code block
            code_text = '\n'.join(code_lines)
            p = doc.add_paragraph()
            p.style = 'No Spacing'
            run = p.add_run(code_text)
            run.font.name = 'Consolas'
            run.font.size = Pt(10)
            code_lines = []
        in_code_block = not in_code_block
        continue

    if in_code_block:
        code_lines.append(line)
        continue

    if line.startswith('# '):
        doc.add_heading(line[2:], 1)
    elif line.startswith('## '):
        doc.add_heading(line[3:], 2)
    elif line.startswith('### '):
        doc.add_heading(line[4:], 3)
    elif line.startswith('- '):
        doc.add_paragraph(line[2:], style='List Bullet')
    elif line.startswith('> '):
        p = doc.add_paragraph()
        run = p.add_run(line[2:])
        run.italic = True
    elif line.strip() == '':
        doc.add_paragraph('')
    else:
        # Check for bold/italic
        p = doc.add_paragraph()
        # Simple bold handling
        parts = line.split('**')
        for i, part in enumerate(parts):
            run = p.add_run(part)
            if i % 2 == 1:
                run.bold = True

doc.save('CHAT_HISTORY.docx')
print('DOCX created')