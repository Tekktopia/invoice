#!/usr/bin/env python3
"""Tekktopia invoice TEK/LD/2026/007 - Netcom Africa Limited."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "tekktopia-logo.png"
OUT_DIR = ROOT / "invoices"
OUT_DIR.mkdir(exist_ok=True)
OUT = OUT_DIR / "Tekktopia Invoice TEK-LD-2026-007 - Netcom Africa.pdf"

# Calibri on Windows; Carlito (its metric-compatible open clone) on Linux/macOS
_FONT_SETS = [
    ("C:/Windows/Fonts", ("calibri.ttf", "calibrib.ttf", "calibrii.ttf")),
    ("/usr/share/fonts/truetype/crosextra", ("Carlito-Regular.ttf", "Carlito-Bold.ttf", "Carlito-Italic.ttf")),
    (str(Path.home() / "Library/Fonts"), ("Carlito-Regular.ttf", "Carlito-Bold.ttf", "Carlito-Italic.ttf")),
]
for _dir, _files in _FONT_SETS:
    _paths = [Path(_dir) / f for f in _files]
    if all(p.exists() for p in _paths):
        pdfmetrics.registerFont(TTFont("Calibri", str(_paths[0])))
        pdfmetrics.registerFont(TTFont("Calibri-Bold", str(_paths[1])))
        pdfmetrics.registerFont(TTFont("Calibri-Italic", str(_paths[2])))
        break
else:
    sys.exit("Calibri/Carlito fonts not found. On Linux: sudo apt install fonts-crosextra-carlito")

W, H = A4
ML, MR = 18 * mm, 18 * mm
RIGHT = W - MR

INK    = HexColor("#22252A")
GRAY   = HexColor("#5C6570")
FAINT  = HexColor("#9AA1A9")
LINE   = HexColor("#C9CED4")
LINE2  = HexColor("#3A3F45")
BLUE   = HexColor("#1B75BC")
ORANGE = HexColor("#F5921E")
BGROW  = HexColor("#F4F5F7")

c = canvas.Canvas(str(OUT), pagesize=A4)
c.setFont("Calibri", 9)
c.setTitle("Invoice TEK/LD/2026/007 - Tekktopia Limited")
c.setAuthor("Tekktopia Limited")

def text(x, y, s, font="Calibri", size=9, color=INK, align="l", track=0):
    c.setFont(font, size)
    c.setFillColor(color)
    if track:
        total = stringWidth(s, font, size) + track * (len(s) - 1)
        cx = x - (total if align == "r" else total / 2 if align == "c" else 0)
        for ch in s:
            c.drawString(cx, y, ch)
            cx += stringWidth(ch, font, size) + track
        return
    if align == "r":
        c.drawRightString(x, y, s)
    elif align == "c":
        c.drawCentredString(x, y, s)
    else:
        c.drawString(x, y, s)

def hline(y, x0=ML, x1=RIGHT, w=0.5, color=LINE):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)

money = lambda v: f"{v:,.2f}"

# letterhead
top = H - 16 * mm
logo_h = 13.5 * mm
c.drawImage(str(LOGO), ML, top - logo_h, width=logo_h,
            height=logo_h, mask="auto")

nx = ML + logo_h + 4.5 * mm
text(nx, top - 5.4 * mm, "TEKKTOPIA LIMITED", "Calibri-Bold", 15.5, INK, track=1.2)
text(nx, top - 9.6 * mm, "Information Technology Services", "Calibri", 7.6, GRAY, track=0.3)

hy = top - 1.5 * mm
for i, s in enumerate([
    "43 Baale Street, Igbo-Efon, Lekki, Lagos, Nigeria",
    "+234 815 433 2992   |   billing@tekktopia.com",
    "www.tekktopia.com",
    "RC 7466800   |   TIN 31661991-0001",
]):
    text(RIGHT, hy - i * 3.9 * mm, s, "Calibri", 7.6, GRAY, "r")

rule_y = top - logo_h - 5 * mm
hline(rule_y, w=0.9, color=LINE2)
c.setStrokeColor(ORANGE); c.setLineWidth(2.2); c.line(ML, rule_y, ML + 11 * mm, rule_y)
c.setStrokeColor(BLUE);   c.line(ML + 11 * mm, rule_y, ML + 22 * mm, rule_y)

# title + meta
ty = rule_y - 12.5 * mm
text(ML, ty, "INVOICE", "Calibri-Bold", 19, INK, track=2.2)

meta = [
    ("Invoice No.",   "TEK/LD/2026/007"),
    ("Invoice Date",  "21 July 2026"),
    ("Payment Terms", "Net 10 days"),
    ("Due Date",      "31 July 2026"),
    ("Currency",      "US Dollar (USD)"),
]
my = ty + 3.2 * mm
label_x = RIGHT - 33 * mm
for i, (k, v) in enumerate(meta):
    yy = my - i * 4.6 * mm
    text(label_x, yy, k, "Calibri", 8, GRAY, "r")
    text(RIGHT, yy, v, "Calibri-Bold" if i == 0 else "Calibri", 8.6, INK, "r")

# bill to
by = ty - 12 * mm
text(ML, by, "BILL TO", "Calibri-Bold", 7.4, FAINT, track=1.1)
bill = [
    ("Netcom Africa Limited", "Calibri-Bold", 10.2, INK),
    ("Attn: Finance Department", "Calibri", 8.8, INK),
    ("6th Floor, South Atlantic Petroleum Towers,", "Calibri", 8.8, GRAY),
    ("1 Adeola Odeku Street, Victoria Island, Lagos, Nigeria", "Calibri", 8.8, GRAY),
    ("solutions@netcomafrica.com", "Calibri", 8.8, GRAY),
]
yy = by - 5.4 * mm
for s, f, sz, col in bill:
    text(ML, yy, s, f, sz, col)
    yy -= 4.5 * mm

# items table
t_top = yy - 5 * mm
col_sn   = ML
col_desc = ML + 10 * mm
col_qty  = RIGHT - 78 * mm
col_rate = RIGHT - 42 * mm
col_amt  = RIGHT

hline(t_top, w=1.0, color=LINE2)
hy = t_top - 5.6 * mm
text(col_sn, hy, "S/N", "Calibri-Bold", 7.6, INK, track=0.4)
text(col_desc, hy, "DESCRIPTION", "Calibri-Bold", 7.6, INK, track=0.6)
text(col_qty, hy, "QTY", "Calibri-Bold", 7.6, INK, "r", track=0.4)
text(col_rate, hy, "UNIT PRICE (USD)", "Calibri-Bold", 7.6, INK, "r", track=0.3)
text(col_amt, hy, "AMOUNT (USD)", "Calibri-Bold", 7.6, INK, "r", track=0.3)
hline(t_top - 8.4 * mm, w=0.7, color=LINE2)

items = [
    ("1", "Apex POB Software Implementation", 1, 6200.00),
    ("2", "ZKTeco Musterguard Integration \u2013 API Connector Licence", 1, 1250.00),
    ("3", "Support & Maintenance (MRC)", 1, 180.00),
]
row_h = 9.2 * mm
ry = t_top - 8.4 * mm
for i, (sn, desc, qty, rate) in enumerate(items):
    base = ry - row_h * (i + 1) + 3.3 * mm
    text(col_sn + 1.2 * mm, base, sn, "Calibri", 9)
    text(col_desc, base, desc, "Calibri", 9)
    text(col_qty, base, str(qty), "Calibri", 9, INK, "r")
    text(col_rate, base, money(rate), "Calibri", 9, INK, "r")
    text(col_amt, base, money(qty * rate), "Calibri", 9, INK, "r")
    hline(ry - row_h * (i + 1), w=0.4, color=LINE)

t_bot = ry - row_h * len(items)

# totals
subtotal = sum(q * r for _, _, q, r in items)
vat = round(subtotal * 0.075, 2)
total = subtotal + vat

tx_label = RIGHT - 62 * mm
sy = t_bot - 7 * mm
for k, v in [("Subtotal", money(subtotal)), ("VAT (7.5%)", money(vat))]:
    text(tx_label, sy, k, "Calibri", 9, GRAY)
    text(col_amt, sy, v, "Calibri", 9, INK, "r")
    sy -= 5.6 * mm

hline(sy + 2.4 * mm, x0=tx_label, w=0.7, color=LINE2)
sy -= 1.6 * mm
text(tx_label, sy, "TOTAL DUE (USD)", "Calibri-Bold", 9.6, INK, track=0.3)
text(col_amt, sy, "$" + money(total), "Calibri-Bold", 11, INK, "r")
hline(sy - 2.8 * mm, x0=tx_label, w=0.7, color=LINE2)

# amount in words
text(ML, t_bot - 7 * mm, "Amount in words:", "Calibri-Bold", 8, GRAY)
text(ML, t_bot - 11.4 * mm, "Eight Thousand, Two Hundred and Two US Dollars,", "Calibri-Italic", 8.6, INK)
text(ML, t_bot - 15.6 * mm, "Twenty-Five Cents Only.", "Calibri-Italic", 8.6, INK)

# naira payment reference
ny = sy - 13 * mm
box_h = 15.5 * mm
c.setStrokeColor(LINE)
c.setLineWidth(0.6)
c.setFillColor(BGROW)
c.roundRect(ML, ny - box_h, RIGHT - ML, box_h, 1.5, stroke=1, fill=1)
text(ML + 4 * mm, ny - 5.2 * mm, "NAIRA PAYMENT OPTION", "Calibri-Bold", 7.4, INK, track=0.9)
text(ML + 4 * mm, ny - 9.6 * mm,
     "Exchange rate reference:  US$1.00 = NGN 1,407.00  (indicative market rate as at 21 July 2026).",
     "Calibri", 8.4, INK)
ngn_total = total * 1407
text(ML + 4 * mm, ny - 13.4 * mm,
     f"Naira equivalent of total due:  NGN {money(ngn_total)}.  Naira payments should apply the prevailing rate on the payment date.",
     "Calibri", 8.4, GRAY)

# payment information
py = ny - box_h - 9 * mm
text(ML, py, "PAYMENT INFORMATION", "Calibri-Bold", 7.4, FAINT, track=1.1)
terms = [
    "Payment is due within 10 days of the invoice date, i.e. on or before 31 July 2026.",
    "Kindly send proof of payment to billing@tekktopia.com, quoting invoice number TEK/LD/2026/007.",
    "Please direct all enquiries regarding this invoice to your account manager or billing@tekktopia.com.",
]
yy = py - 5 * mm
for s in terms:
    text(ML, yy, s, "Calibri", 8.6, INK)
    yy -= 4.6 * mm

# account manager
am_y = yy - 4.5 * mm
text(ML, am_y, "ACCOUNT MANAGER", "Calibri-Bold", 7.4, FAINT, track=1.1)
text(ML, am_y - 5.2 * mm, "Boluwatife Oni", "Calibri-Bold", 9.2, INK)
text(ML, am_y - 9.8 * mm, "boluwatifeo@tekktopia.com   |   +234 903 659 9775", "Calibri", 8.6, GRAY)

# footer
fy = 18 * mm
hline(fy + 5.5 * mm, w=0.5, color=LINE)
text(W / 2, fy, "Thank you for your business.", "Calibri-Italic", 8, GRAY, "c")
text(W / 2, fy - 4.2 * mm,
     "Tekktopia Limited  |  RC 7466800  |  TIN 31661991-0001  |  www.tekktopia.com",
     "Calibri", 7, FAINT, "c")

c.save()
print("Wrote", OUT)
print("subtotal", subtotal, "vat", vat, "total", total, "ngn", ngn_total)
