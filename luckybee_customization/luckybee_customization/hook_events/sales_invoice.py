def set_total_mrp(doc, method):
    total_mrp = 0
    for item in doc.items:
        total_mrp += int(item.custom_mrp)
    doc.custom_total_mrp = total_mrp