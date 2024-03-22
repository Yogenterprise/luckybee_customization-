import frappe

@frappe.whitelist()
def get_fields(purchase_invoice):
    # BRAND_NAMES= ("DECO PRIDE", "JAYPEE", "ELEGANTE", "CLAY", "YERA", "TREO", "SIGNORAWARE", "SUNWELL", "ROYALWARE", "CORELLE", "GARUDA", "VAYA", "ASSR", "STEHLEN", "JCPL", "MELOWARE", "MEYER", "MARVEL", "MILTON", "ROXX", "CELLO", "M/W",  "CROWN",  "TAJ", "YAMASIN", "OCEAN", "CORELLE", "STEELO")
    pi = frappe.get_doc("Purchase Invoice", purchase_invoice)
    item_table= pi.items
    
    res_list= []
    for item in item_table:
        res = item.as_dict()
        item_doc = frappe.get_doc("Item", item.item_code)
       
        description = item.description        
        # brand = [b for b in BRAND_NAMES if b in description]
        # if brand:
        #     res["brand"] = brand[0]
        
        item_doc = frappe.get_doc("Item", item.item_code)        
        res["brand"] = item_doc.brand
        res["ean"] = item_doc.ean
        res["subcategory"] = item_doc.custom_sub_category
        
        res_list.append(res)
    return res_list

@frappe.whitelist()
def update_data(data):
    # frappe.log_error("incoming_data", data)
    # pi = frappe.get_doc("Purchase Invoice", data)
    # for item in pi.items:
    #     if item.item_code == item_code:
    #         item.price_list_rate = 3
    #         # item.save()
    #         pi.save()
    #         frappe.db.commit()
    #         # frappe.db.set_value("Purchase Invoice Item", item.name, {"price_list_rate" : 1})
    #         return item.price_list_rate
    frappe.log_error("Incoming data", data)
    return data
    
@frappe.whitelist()
def get_item(item_code):
    item = frappe.get_doc("Item", item_code)
    # res = {}
    # res["item_code"] = item.item_code
    # res["brand"] = item.brand
    # res["description"] = item.description
    # res["item_name"] = item.item_name
    # res['custom_asin'] = item.custom_asin
    # res['received_qty'] = item.received_qty
    return item
