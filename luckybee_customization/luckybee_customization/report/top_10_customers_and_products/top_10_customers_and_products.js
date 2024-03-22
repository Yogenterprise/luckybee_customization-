
frappe.query_reports["Top 10 Customers And Products"] = {
	"filters": [

		{
			'label':'From Date',
			'fieldname':'from_date',
			'fieldtype':'Date',
			"reqd": 1,                   // Make field required will limit the record or data in the report
			'width':80
		},
		{
			'label':'To Date',
			'fieldname':'to_date',
			'fieldtype':'Date',
			"reqd": 1,
			'width':80
		},
		{
			'label': 'Category',
			'fieldname': 'category',
			'fieldtype': 'Select',
			'options': [ 
				{"value": "Customer", "label": __("Customer")},
				{"value": "Product", "label": __("Product")}
			],
			'reqd': 1,
			'width': 80
		}
		


	]
};



