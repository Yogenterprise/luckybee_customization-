frappe.ui.form.on('Purchase Invoice', {
	is_paid(frm) {
		console.log('hhhhhhhhhhhh')
	},
	custom_search_and_insert_item(frm) {
		if (frm.doc.custom_custom_purchase_item) {
			cur_frm.clear_table("items");

			for (let obj of frm.doc.custom_custom_purchase_item) {
				frappe.call({
					method: "luckybee_customization.luckybee_customization.doctype.purchase_invoice.search_and_insert_item",
					args: {
						'doc': frm.doc,
						'description': obj.description_of_good_and_services,
						'hsn': obj.hsnsac != null ? obj.hsnsac : "",
						'qty': obj.quantity != null ? obj.quantity : 0,
						'rate': obj.rate != null ? obj.rate : 0,
						'per': obj.per != null ? obj.per : "",
						'disc_perc': obj.disc_ != null ? obj.disc_ : "",
						'disc': obj.disc != null ? obj.disc : "",
						'gst': obj.gst != null ? obj.gst : "",
						'mrp': obj.mrp != null ? obj.mrp : "",
						'lrp': obj.lrp != null ? obj.lrp : "",
						'brand': obj.brand != null ? obj.brand : "",
						'group': obj.group != null ? obj.group : "",
						'category': obj.category != null ? obj.category : "",
						'sub_category': obj.sub_category != null ? obj.sub_category : "",

						//'Amount':obj.amount !=null ? obj.amount : "",
						// 'custom_purchase_item':obj.hsnsac
					},
					freeze: true,
					freeze_message: "loading items...",
					callback: function (r) {
						
						console.log(r.message, "r.message-------------")
						if(r.message){

							console.log(r.message, "r.message-------------")
							var item_row = cur_frm.add_child("items");
							item_row.item_code = r.message.item_code;
							item_row.item_name = r.message.item_name;
							item_row.qty = r.message.qty;
							item_row.uom = r.message.uom;
							item_row.rate = r.message.rate;
							item_row.amount = r.message.amount;
							cur_frm.refresh_fields("items") ;
						}
						
					}
				})

			}
		}
	}

})
