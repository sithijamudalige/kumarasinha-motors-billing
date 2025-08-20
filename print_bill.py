import datetime
import os
import tempfile

try:
    import win32print
    import win32api
    WINDOWS = True
except ImportError:
    WINDOWS = False

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import pytz  # for timezone support

def format_currency(amount):
    return f"Rs {amount:.2f}"

def print_or_save_bill(customer_number, bill_items, total_amount, cash, change):
    """
    customer_number: string
    bill_items: list of tuples (name, model, qty, price, total)
    total_amount, cash, change: floats
    """

    # Get Sri Lanka local time
    try:
        tz = pytz.timezone("Asia/Colombo")
        now = datetime.datetime.now(tz)
    except Exception:
        # fallback local time
        now = datetime.datetime.now()

    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    header = [
        "KUMARASINGHE MOTORS",
        "Address: No. 225/B Rajaphilla Road, Kandy",
        "Tel: 081 222 11 43 / 078 733 95 16",
        "Registration Number: 5/2/8246",
        "",
        f"Customer Number: {customer_number}",
        f"Date: {date_str}    Time: {time_str}",
        "-"*40
    ]

    columns = f"{'Name':15} {'Model':10} {'Qty':>3} {'Price':>8} {'Total':>10}"
    lines = header + [columns, "-"*40]

    for name, model, qty, price, total in bill_items:
        name_display = name[:15]
        model_display = (model if model else "")[:10]
        lines.append(f"{name_display:15} {model_display:10} {qty:3d} {format_currency(price):>8} {format_currency(total):>10}")

    lines += [
        "-"*40,
        f"{'Total':>38}: {format_currency(total_amount)}",
        f"{'Cash':>38}: {format_currency(cash)}",
        f"{'Change':>38}: {format_currency(change)}",
        "-"*40
    ]

    bill_text = "\n".join(lines)

    if WINDOWS and is_printer_available():
        send_to_printer(bill_text)
    else:
        save_as_pdf(bill_text, customer_number, date_str)

def is_printer_available():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    return len(printers) > 0

def send_to_printer(text):
    printer_name = win32print.GetDefaultPrinter()
    if not printer_name:
        raise RuntimeError("No default printer configured")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(text.encode('utf-8'))
        temp_filename = f.name

    try:
        win32api.ShellExecute(
            0,
            "print",
            temp_filename,
            f'/d:"{printer_name}"',
            ".",
            0
        )
    finally:
        pass  # optionally delete temp file later

def save_as_pdf(text, customer_number, date_str):
    filename = f"Bill_{customer_number}_{date_str}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin

    for line in text.split("\n"):
        c.drawString(margin, y, line)
        y -= 15
        if y < margin:
            c.showPage()
            y = height - margin

    c.save()
    print(f"Bill saved as PDF: {filename}")

if __name__ == "__main__":
    test_items = [
        ("Brake Pad", "BP-123", 2, 500.0, 1000.0),
        ("Headlight", "", 1, 1200.0, 1200.0),
    ]
    print_or_save_bill("12345", test_items, 2200.0, 2500.0, 300.0)
