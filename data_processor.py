from collections import defaultdict

def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # ✅ must have 8 columns
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, customer, region = parts

        try:
            transaction = {
                "TransactionID": tid.strip(),
                "Date": date.strip(),
                "ProductID": pid.strip(),
                "ProductName": pname.replace(",", "").strip(),
                "Quantity": int(qty.replace(",", "").strip()),
                "UnitPrice": float(price.replace(",", "").strip()),
                "CustomerID": customer.strip(),
                "Region": region.strip()
            }
            transactions.append(transaction)
        except:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid_count = 0

    for t in transactions:
        try:
            if not t.get("CustomerID") or not t.get("Region"):
                invalid_count += 1
                continue
            if t["Quantity"] <= 0 or t["UnitPrice"] <= 0:
                invalid_count += 1
                continue
            if not t["TransactionID"].startswith("T"):
                invalid_count += 1
                continue

            amount = t["Quantity"] * t["UnitPrice"]

            if region and t["Region"] != region:
                continue
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue

            valid.append(t)

        except:
            invalid_count += 1

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid)
    }

    return valid, invalid_count, summary


def calculate_total_revenue(transactions):
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total


def region_wise_sales(transactions):
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    for region in region_data:
        sales = region_data[region]["total_sales"]
        region_data[region]["percentage"] = round((sales / total_revenue) * 100, 2) if total_revenue > 0 else 0

    sorted_regions = dict(sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True))
    return sorted_regions


def top_selling_products(transactions, n=5):
    product_summary = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if name not in product_summary:
            product_summary[name] = {"qty": 0, "revenue": 0.0}

        product_summary[name]["qty"] += qty
        product_summary[name]["revenue"] += revenue

    product_list = []
    for name, info in product_summary.items():
        product_list.append((name, info["qty"], round(info["revenue"], 2)))

    product_list.sort(key=lambda x: x[1], reverse=True)
    return product_list[:n]


def customer_analysis(transactions):
    customers = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]

        if cid not in customers:
            customers[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[cid]["total_spent"] += amount
        customers[cid]["purchase_count"] += 1
        customers[cid]["products_bought"].add(t["ProductName"])

    for cid in customers:
        total = customers[cid]["total_spent"]
        count = customers[cid]["purchase_count"]
        customers[cid]["avg_order_value"] = round(total / count, 2) if count > 0 else 0
        customers[cid]["products_bought"] = sorted(list(customers[cid]["products_bought"]))
        customers[cid]["total_spent"] = round(customers[cid]["total_spent"], 2)

    sorted_customers = dict(sorted(customers.items(), key=lambda x: x[1]["total_spent"], reverse=True))
    return sorted_customers


def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["unique_customers"].add(t["CustomerID"])

    for date in daily:
        daily[date]["revenue"] = round(daily[date]["revenue"], 2)
        daily[date]["unique_customers"] = len(daily[date]["unique_customers"])

    sorted_daily = dict(sorted(daily.items(), key=lambda x: x[0]))
    return sorted_daily


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = -1
    peak_count = 0

    for date, info in daily.items():
        if info["revenue"] > peak_revenue:
            peak_revenue = info["revenue"]
            peak_date = date
            peak_count = info["transaction_count"]

    return (peak_date, peak_revenue, peak_count)


def low_performing_products(transactions, threshold=10):
    product_summary = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = t["Quantity"] * t["UnitPrice"]

        if name not in product_summary:
            product_summary[name] = {"qty": 0, "revenue": 0.0}

        product_summary[name]["qty"] += qty
        product_summary[name]["revenue"] += revenue

    low_list = []
    for name, info in product_summary.items():
        if info["qty"] < threshold:
            low_list.append((name, info["qty"], round(info["revenue"], 2)))

    low_list.sort(key=lambda x: x[1])
    return low_list
