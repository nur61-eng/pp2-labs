import re
import json

text = open("raw.txt", encoding="utf-8").read()
prices = re.findall(r'\d+\s*x\s*([\d\s]+,\d+)', text)
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices]
products = re.findall(r'\d+\.\s*\n(.+)', text)
datetime = re.search(r'Время:\s*([\d\.]+\s[\d:]+)', text)
datetime = datetime.group(1) if datetime else None
payment = re.search(r'(Банковская карта|Наличные)', text)
payment = payment.group(1) if payment else None
total = re.search(r'ИТОГО:\s*([\d\s]+,\d+)', text)
if total:
    total = float(total.group(1).replace(" ", "").replace(",", "."))
else:
    total = None
data = {
    "products": products,
    "prices": prices,
    "total": total,
    "datetime": datetime,
    "payment_method": payment
}

print(json.dumps(data, indent=4, ensure_ascii=False))