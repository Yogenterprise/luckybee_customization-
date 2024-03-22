// Copyright (c) 2024, bizmap technologies pvt ltd and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Sales By Category"] = {
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
		}


	]
};



