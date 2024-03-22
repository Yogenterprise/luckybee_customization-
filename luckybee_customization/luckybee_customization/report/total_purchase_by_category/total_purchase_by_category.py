import frappe

from frappe import _

def execute(filters=None):
	columns,data = get_columns(filters),get_data(filters)
	chart=get_chart_data(data)

	return columns, data,None,chart

def get_data(filters):
	from_date =filters.from_date
	to_date =filters.to_date
	data = frappe.db.sql("""
							SELECT 
								item.custom_category,
								SUM(stock.stock_value_difference) AS total_valuation_rate
							FROM
								`tabStock Ledger Entry` AS stock
							LEFT JOIN
								`tabItem` AS item ON stock.item_code = item.name
							WHERE
								stock.voucher_type = 'Purchase Invoice' or stock.voucher_type = 'Purchase Invoice'
								AND stock.posting_date BETWEEN %(from_date)s AND %(to_date)s
							GROUP BY
								item.custom_category ;
						""" ,({"from_date":str(from_date),"to_date":str(to_date)}),as_dict=1)


	# data = [{**x,**{"net_balance":x.total_deposited_amount-x.total_purchase_cost,"outstanding_deposit":0}} for x in data]
	frappe.log_error("from_date",from_date)
	frappe.log_error("to_date",to_date)
	frappe.log_error("data",data)
	frappe.log_error("filters",filters)
	return data
	

	
def get_columns(filters):
	columns = [
		 {
			"label":_("Category"),
			"fieldname": "custom_category",       # filedname should match with the values in SELECT clause of query
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label":_("Total Purchase"),
			"fieldname": "total_valuation_rate",
			"fieldtype": "Float",          # link field will redirect the user to the source doctype
			"width": 200,
		}
		]
	
	return columns


def get_chart_data(data):
	frappe.log_error("chartdata",data)
	if not data:
		return None
	labels=[]
	datasets=[{'values':[]}]
	for i in data:
		datasets[0]['values'].append(i.get('total_valuation_rate'))
		labels.append(i.get('custom_category'))
	
	chart={
		'data':{
			'labels':labels,
			'datasets':datasets
		},
		'type':'bar',
		'height':300
	}
	frappe.log_error("datasets",datasets)
	frappe.log_error("labels",labels)
	return chart


