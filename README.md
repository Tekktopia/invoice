# Tekktopia Invoicing

Internal tooling for producing Tekktopia Limited invoices. Two ways to make an invoice live here: a browser-based editable template (no installation needed) and a Python script that regenerates the pixel-perfect PDF.

## What's in this repo

| Path | What it is |
|---|---|
| `index.html` | Self-contained editable invoice tool. Open it in any browser. |
| `generator/make_invoice.py` | Python (ReportLab) script that generates the static PDF version. |
| `assets/tekktopia-logo.png` | Company logo mark used by the generator. |
| `invoices/` | Issued invoices. Currently holds TEK/LD/2026/007 (Netcom Africa). |

## Using the invoice tool (`index.html`)

Open the file in Chrome or Edge. Everything on the page is click-to-edit: invoice number, dates, client details, line items, the VAT percentage and the exchange rate.

- **Add or remove line items** with the "+ Add line item" button; hover a row for the remove (×) control. Rows renumber automatically.
- **Totals recalculate live**, including the amount in words and the naira equivalent shown under the total.
- **USD / NGN switch** (top right, next to Download PDF) turns the document into a naira invoice: prices convert at the exchange rate on the page, headers and the amount in words switch to Naira/Kobo, and the exchange-rate box is hidden.
- **Download PDF** opens the browser's print dialog — choose "Save as PDF". The saved filename follows the invoice number on the page.
- Editing the invoice number at the top also updates the "quoting invoice number …" line in Payment Information.

Note: on Windows the page renders in genuine Calibri automatically.

## Regenerating the static PDF

```bash
pip install reportlab
python generator/make_invoice.py
```

The PDF is written into `invoices/`. Fonts: on Windows the script uses the system's Calibri; on Linux install the metric-compatible open equivalent first with `sudo apt install fonts-crosextra-carlito`. To change invoice contents, edit the clearly-labelled sections (meta, bill-to, items, terms) near the top of the script.

## Notes

- **Keep this repository private.** The template and the issued invoice contain client names and pricing.
- If you later want the team to use the tool from a URL instead of a local file, GitHub Pages can serve `index.html` directly (Settings → Pages). Pages on a private repository requires a paid GitHub plan; on a free plan the repo would have to be public, which is not recommended given the contents.
