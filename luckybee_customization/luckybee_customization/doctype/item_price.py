import frappe

def before_save(doc,method):
    Doc=frappe.get_doc("Item",doc.item_code)
    child_tbl=Doc.append('custom_item_price_details',{})
    child_tbl.item_price=doc.name
    child_tbl.item_code=doc.item_code
    child_tbl.uom=doc.uom
    child_tbl.price_list=doc.price_list
    child_tbl.rate=doc.price_list_rate
    Doc.save()
