import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(r"\d+", text)
print("Prices:", prices)

date = re.search(r"\d{2}\.\d{2}\.\d{4}", text)
if date:
    print("Date:", date.group())

time = re.search(r"\d{2}:\d{2}", text)
if time:
    print("Time:", time.group())

payment = re.search(r"CARD|CASH|VISA|MASTERCARD", text)
if payment:
    print("Payment:", payment.group())

lines = text.split("\n")
print("Products:")

for line in lines:
    product = re.match(r"([A-Za-z]+)\s+(\d+)", line)
    if product:
        print("Name:", product.group(1), "- Price:", product.group(2))