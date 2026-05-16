# AWB Scanner Tool

<img width="781" height="479" alt="image" src="https://github.com/user-attachments/assets/daff0899-15eb-4183-8bf1-932a1d90872c" />

Python desktop application สำหรับ automate การ scan AWB (Air Waybill) ผ่าน mouse automation และ keyboard automation พร้อมระบบ Hotkey Control, Position Capture และ Auto Input Workflow

โปรแกรมถูกออกแบบสำหรับ warehouse operation และ logistics scanning workflow เพื่อช่วยลดเวลาการยิงเลข AWB ซ้ำ ๆ ในระบบ WMS หรือ Web Application

รองรับ:

- Auto AWB Input
- Mouse Automation
- Keyboard Automation
- Paste Mode
- Global Hotkeys
- Pause / Resume
- Emergency Stop
- Position Capture
- Config Persistence
- Background Thread Processing

---

# Features

- Auto scan AWB list
- Mouse click automation
- Type mode input
- Paste mode input
- Position capture system
- Global hotkeys
- Pause / Resume support
- Emergency stop system
- Remaining counter
- Current AWB display
- Auto clipboard copy
- Config auto save
- Background threading
- GUI desktop application
- Windows automation support

---

# Application Overview

โปรแกรมนี้ใช้สำหรับ:

1. อ่านรายการ AWB
2. คลิกตำแหน่ง input อัตโนมัติ
3. พิมพ์หรือ paste AWB
4. คลิก submit อัตโนมัติ
5. Loop จนรายการหมด

เหมาะสำหรับ:

- Warehouse Operation
- Logistics Hub
- WMS Input Automation
- Parcel Sorting
- AWB Validation
- Manual Scan Replacement

---

# Tech Stack

- Python
- Tkinter
- PyAutoGUI
- Pyperclip
- Keyboard
- Threading
- ConfigParser

---

# Project Structure

```text
project/
│
├── main.py
├── config.ini
│
└── requirements.txt
```

---

# Scan Workflow

```text
Load AWB List
    ↓
Capture Input Position
    ↓
Capture Submit Position
    ↓
Start Auto Scan
    ↓
Click Input Position
    ↓
Type / Paste AWB
    ↓
Click Submit Position
    ↓
Next AWB
```

---

# Input Modes

## 1. Type Mode

ใช้:

```python
pyautogui.write()
```

ระบบจะพิมพ์ AWB ทีละตัวอักษร

รองรับ:

- ระบบที่ block paste
- โปรแกรมที่ต้อง simulate keyboard จริง

---

## 2. Paste Mode

ใช้:

```python
Ctrl + V
```

Workflow:

```text
Copy AWB → Clipboard
    ↓
Paste ผ่าน Ctrl+V
```

เหมาะสำหรับ:

- Web Application
- Fast Input
- Large AWB Batch

---

# Position Capture System

ผู้ใช้สามารถ capture:

| Position | Function |
|---|---|
| Input | ช่องกรอก AWB |
| Submit | ปุ่ม submit |

โดยกด:

```text
=
```

ระบบจะ save:

```text
x1 y1
x2 y2
```

ลง config อัตโนมัติ

---

# Auto Scan Logic

Workflow:

```text
Read First AWB
    ↓
Copy Clipboard
    ↓
Click Input Position
    ↓
Type / Paste AWB
    ↓
Click Submit
    ↓
Remove AWB From Queue
    ↓
Update Counter
```

---

# Queue System

AWB จะถูกดึงจาก Textbox แบบ FIFO

ตัวอย่าง:

```text
AWB001
AWB002
AWB003
```

เมื่อ scan:

```text
AWB001 → remove
AWB002 → next
```

---

# Global Hotkeys

รองรับ hotkey ระดับ system-wide

## Emergency Stop

Default:

```text
F12
```

Function:

- stop automation ทันที
- reset running state

---

## Pause / Resume

Default:

```text
F11
```

Function:

- pause auto scan
- resume scan

---

## Stop

Default:

```text
F10
```

Function:

- stop current loop
- clear running state

---

# FailSafe System

ใช้:

```python
pyautogui.FAILSAFE = True
```

หากลาก mouse ไปมุมซ้ายบน:

```text
TOP LEFT CORNER
```

ระบบจะหยุด automation ทันที

---

# Delay System

รองรับ delay 2 แบบ

## Click Delay

ใช้สำหรับ:

- delay ระหว่าง scan loop
- รอระบบ response

---

## Type Delay

ใช้สำหรับ:

- delay ระหว่าง character
- slow typing simulation

---

# GUI Overview

โปรแกรมแบ่งออกเป็น:

## AWB List Panel

ใช้สำหรับ:

- paste AWB list
- edit queue
- monitor remaining items

---

## Position Panel

ใช้สำหรับ:

- capture input position
- capture submit position

---

## Delay Panel

ใช้สำหรับ:

- set click delay
- set type delay

---

## Input Mode Panel

เลือก:

- Type Mode
- Paste Mode

---

## Action Panel

ประกอบด้วย:

- Auto Scan
- Pause / Resume
- Stop
- Save Config

---

# Status Bar

แสดง:

| Status | Description |
|---|---|
| AWB | Current Processing AWB |
| Remaining | Remaining Queue Count |

---

# Config System

ใช้:

```text
config.ini
```

สำหรับเก็บ:

- mouse positions
- delay settings
- hotkeys

---

# Example Config

```ini
[POSITION]
x1=500
y1=300
x2=800
y2=300

[DELAY]
click=0.5
key=0.3

[HOTKEY]
emergency_stop=F12
pause_resume=F11
stop=F10
```

---

# Threading Design

โปรแกรมใช้:

```python
threading.Thread()
```

สำหรับ:

- background auto scan
- non-blocking GUI
- smooth UI update

ช่วยให้:

- GUI ไม่ค้าง
- stop automation ได้ทันที
- pause/resume ได้

---

# Clipboard Workflow

ระบบใช้:

```python
pyperclip.copy()
```

สำหรับ:

- copy AWB
- prepare paste mode
- reduce typing error

---

# Auto Queue Update

หลัง scan:

- remove AWB จาก textbox
- update remaining count
- update current AWB

แบบ real-time

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourname/awb-scanner-tool.git
```

---

## 2. Install Dependencies

```bash
pip install pyautogui pyperclip keyboard
```

---

## 3. Run Application

```bash
python main.py
```

---

# Build EXE

ใช้ PyInstaller:

```bash
pyinstaller --onefile --windowed main.py
```

หรือ:

```bash
pyinstaller --noconsole --onefile main.py
```

---

# Windows Automation Notes

โปรแกรมใช้ mouse และ keyboard automation

แนะนำ:

- Run as Administrator
- Disable screen sleep
- ใช้บน monitor scale 100%
- ห้ามขยับตำแหน่ง window ระหว่าง automation

---

# Error Handling

ระบบรองรับ:

- empty AWB queue
- invalid position
- hotkey registration failure
- emergency stop
- invalid delay value
- interrupted automation
- config load failure

---

# User Experience Features

- Real-time AWB status
- Remaining counter
- Auto clipboard copy
- Hotkey control
- Pause / Resume
- Emergency stop
- Auto config save
- FIFO queue processing

---

# Future Improvements

- OCR screen detection
- Image recognition button click
- CSV import
- Excel import
- Auto retry submit
- Scan success validation
- Multi-position workflow
- Multi-monitor support
- Macro recording
- Scheduler mode

---

# License

MIT License

---

# Author

Developed for warehouse automation and AWB scanning workflow optimization.


