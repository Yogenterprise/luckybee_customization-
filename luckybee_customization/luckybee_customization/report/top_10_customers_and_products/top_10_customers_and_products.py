import frappe

from frappe import _

def execute(filters=None):
	data=get_data(filters)
	category=filters.category
	if category=='Customer':
		columns=get_columns_for_customers(filters)
	if category=='Product':
		columns=get_columns_for_product(filters)

	return columns, data



	

def get_data(filters):
	from_date =filters.from_date
	to_date =filters.to_date
	category=filters.category
	if category=='Customer':
		data=frappe.db.sql("""
							SELECT 
								si.customer AS customer_name,
								SUM(si.total_qty) AS total_quantity,
								SUM(si.total) AS total_amount
							FROM 
								`tabSales Invoice` AS si
							WHERE 
								si.posting_date BETWEEN %(from_date)s AND %(to_date)s AND si.status='Paid'
							GROUP BY  
								si.customer
							ORDER BY 
								Total_Quantity DESC, Total_Amount DESC
							LIMIT 10;
							""",({"from_date":str(from_date),"to_date":str(to_date)}),as_dict=1)

	if category=='Product':
		data=frappe.db.sql("""
								SELECT 
								item.item_name AS item_name,
								ABS(SUM(stock.stock_value_difference)) AS AMOUNT,
								ABS(SUM(stock.actual_qty)) AS QTY
							FROM
								`tabStock Ledger Entry` AS stock
							LEFT JOIN
								`tabItem` AS item ON stock.item_code = item.name
							WHERE
								(stock.voucher_type = 'Sales Invoice')
								AND stock.posting_date BETWEEN %(from_date)s  AND %(to_date)s
							GROUP BY
								item.item_name
							ORDER BY 
								AMOUNT DESC, QTY DESC
							LIMIT 10;""",({"from_date":str(from_date),"to_date":str(to_date)}),as_dict=1)

	frappe.log_error("from_date",from_date)
	frappe.log_error("to_date",to_date)
	frappe.log_error("data",data)
	frappe.log_error("filters",filters)
	frappe.log_error("category",category)
	return data
	

	
def get_columns_for_customers(filters):
	columns = [
		 {
			"label":_("Customer Name"),
			"fieldname": "customer_name",       # filedname should match with the values in SELECT clause of query
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label":_("QTY"),
			"fieldname": "total_quantity",
			"fieldtype": "Float",          # link field will redirect the user to the source doctype
			"width": 200,
		},
		{
			"label":_("Amount"),
			"fieldname": "total_amount",
			"fieldtype": "Float",          # link field will redirect the user to the source doctype
			"width": 200,
		}
		]
	
	return columns


def get_columns_for_product(filters):
	columns = [
		 {
			"label":_("Item Name"),
			"fieldname": "item_name",       # filedname should match with the values in SELECT clause of query
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label":_("QTY"),
			"fieldname": "QTY",
			"fieldtype": "Float",          # link field will redirect the user to the source doctype
			"width": 200,
		},
		{
			"label":_("Amount"),
			"fieldname": "AMOUNT",
			"fieldtype": "Float",          # link field will redirect the user to the source doctype
			"width": 200,
		}
		]
	
	return columns



