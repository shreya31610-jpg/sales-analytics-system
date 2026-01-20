from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data


def main():
    print("======================================")
    print("        SALES ANALYTICS SYSTEM         ")
    print("======================================")

    print("\n[1/6] Reading sales data file...")
    raw_lines = read_sales_data("data/sales_data.txt")
    print(f"✅ Successfully read {len(raw_lines)} lines")

    print("\n[2/6] Parsing transactions...")
    parsed = parse_transactions(raw_lines)
    print(f"✅ Parsed {len(parsed)} transactions")

    print("\n[3/6] Validating transactions...")
    valid, invalid, summary = validate_and_filter(parsed)
    print(f"✅ Valid records: {len(valid)}")
    print(f"❌ Invalid removed: {invalid}")

    print("\n[4/6] Fetching products from API...")
    api_products = fetch_all_products()
    print(f"✅ Fetched {len(api_products)} products")

    print("\n[5/6] Enriching sales data...")
    product_mapping = create_product_mapping(api_products)
    enriched = enrich_sales_data(valid, product_mapping)

    matched = sum(1 for t in enriched if t.get("API_Match"))
    print(f"✅ Enriched {matched}/{len(enriched)} transactions")

    # ✅ Analytics Calculations
    total_revenue = calculate_total_revenue(valid)
    region_stats = region_wise_sales(valid)
    top_products = top_selling_products(valid, n=5)
    customers = customer_analysis(valid)
    daily_stats = daily_sales_trend(valid)
    peak_day = find_peak_sales_day(valid)
    low_products = low_performing_products(valid, threshold=10)

    print("\n[6/6] Writing report...")

    with open("output/sales_report.txt", "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("==================================================\n\n")

        f.write("1) DATA SUMMARY\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Lines Read: {len(raw_lines)}\n")
        f.write(f"Transactions Parsed: {len(parsed)}\n")
        f.write(f"Valid Transactions: {len(valid)}\n")
        f.write(f"Invalid Removed: {invalid}\n\n")

        f.write("2) TOTAL REVENUE\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Total Revenue: {round(total_revenue, 2)}\n\n")

        f.write("3) REGION WISE SALES\n")
        f.write("--------------------------------------------------\n")
        for region, info in region_stats.items():
            f.write(
                f"{region}: Revenue={round(info['total_sales'],2)}, "
                f"Transactions={info['transaction_count']}, "
                f"Share={info['percentage']}%\n"
            )
        f.write("\n")

        f.write("4) TOP 5 SELLING PRODUCTS\n")
        f.write("--------------------------------------------------\n")
        for name, qty, rev in top_products:
            f.write(f"{name} | Quantity Sold: {qty} | Revenue: {rev}\n")
        f.write("\n")

        f.write("5) CUSTOMER ANALYSIS (TOP 5 CUSTOMERS)\n")
        f.write("--------------------------------------------------\n")
        top_5_customers = list(customers.items())[:5]
        for cid, info in top_5_customers:
            f.write(
                f"{cid} | Total Spent: {info['total_spent']} | "
                f"Purchases: {info['purchase_count']} | "
                f"Avg Order: {info['avg_order_value']}\n"
            )
        f.write("\n")

        f.write("6) DAILY SALES TREND\n")
        f.write("--------------------------------------------------\n")
        for date, info in daily_stats.items():
            f.write(
                f"{date} | Revenue: {info['revenue']} | "
                f"Transactions: {info['transaction_count']} | "
                f"Unique Customers: {info['unique_customers']}\n"
            )
        f.write("\n")

        f.write("7) PEAK SALES DAY\n")
        f.write("--------------------------------------------------\n")
        f.write(f"Peak Day: {peak_day[0]}\n")
        f.write(f"Revenue: {peak_day[1]}\n")
        f.write(f"Transactions: {peak_day[2]}\n\n")

        f.write("8) LOW PERFORMING PRODUCTS (Quantity < 10)\n")
        f.write("--------------------------------------------------\n")
        if len(low_products) == 0:
            f.write("No low performing products found.\n")
        else:
            for name, qty, rev in low_products:
                f.write(f"{name} | Qty Sold: {qty} | Revenue: {rev}\n")
        f.write("\n")

        f.write("9) API ENRICHMENT SUMMARY\n")
        f.write("--------------------------------------------------\n")
        f.write(f"API Products Fetched: {len(api_products)}\n")
        f.write(f"Transactions Enriched: {matched}/{len(enriched)}\n")
        f.write("NOTE: DummyJSON product IDs may not match local ProductID format.\n")

    print("\n✅ DONE! Report created: output/sales_report.txt")


if __name__ == "__main__":
    main()
