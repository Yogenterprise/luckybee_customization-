frappe.ui.form.on('Purchase Invoice', {
    is_paid(frm) {
        console.log('hhhhhhhhhhhh');
    },
    custom_search_and_insert_item(frm) {
        if (frm.doc.custom_custom_purchase_item) {
            cur_frm.clear_table("items");
            console.log(frm.doc.custom_is_asin);
            if (frm.doc.custom_is_asin === 1) {
                for (let obj of frm.doc.custom_custom_purchase_item) {
                    frappe.call({
                        method: "luckybee_customization.luckybee_customization.doctype.asin_purchase_invoice.search_and_insert_item",
                        args: {
                            'doc': frm.doc,
                            'description': obj.description_of_good_and_services,
                            'hsn': obj.hsnsac != null ? obj.hsnsac : "",
                            'qty': obj.quantity != null ? obj.quantity : 0,
                            'rate': obj.rate != null ? obj.rate : 0,
                            'per': obj.per != null ? obj.per : "",
                            // 'disc_perc': obj.disc_ != null ? obj.disc_ : "",
                            // 'disc': obj.disc != null ? obj.disc : "",
                            // 'gst': obj.gst != null ? obj.gst : "",
                            'mrp': obj.mrp != null ? obj.mrp : "",
                            'lrp': obj.lrp != null ? obj.lrp : "",
                            'brand': obj.brand != null ? obj.brand : "",
                            'group': obj.group != null ? obj.group : "",
                            'category': obj.category != null ? obj.category : "",
                            'sub_category': obj.sub_category != null ? obj.sub_category : "",
                            'custom_asin': obj.custom_asin != null ? obj.custom_asin : "",
                            'custom_box_number': obj.custom_box_number != null ? obj.custom_box_number : "",
                            "custom_ean": obj.custom_ean != null ? obj.custom_ean : ""
                        },
                        freeze: true,
                        freeze_message: "loading items...",
                        callback: function (r) {
                            console.log(r.message, "r.message-------------");
                            if (r.message) {
                                console.log(r.message, "r.message-------------");
                                var item_row = cur_frm.add_child("items");
                                item_row.item_code = r.message.item_code;
                                item_row.item_name = r.message.item_name;
                                item_row.qty = r.message.qty;
                                item_row.uom = r.message.uom;
                                item_row.rate = r.message.rate;
                                item_row.amount = r.message.amount;
                                item_row.custom_reviewsrating = r.message.reviews_rating;
                                item_row.custom_new_current = r.message.new_current;
                                item_row.custom_box_number = r.message.custom_box_number;
                                item_row.custom_asin = r.message.custom_asin;
                                // item_row.rate = r.message.rate;
                                item_row.custom_reviews_count = r.message.custom_reviews_count;
                                cur_frm.refresh_fields("items");
                                for (let item of cur_frm.doc.custom_custom_purchase_item) {
                                    if (item.description_of_good_and_services === r.message.item_name) {
                                        item.custom_reviewsrating = r.message.reviews_rating;
                                    }
                                }
                            }
                        }
                    });
                }
                let fi = frm.doc.custom_custom_purchase_item[0];
                if (fi.custom_asin == null && fi.custom_ean == null) {
                    let fields = [];
                }
            } else {
                for (let obj of frm.doc.custom_custom_purchase_item) {
					console.log("non asin mmethod is calling")
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
                            'sub_category': obj.sub_category != null ? obj.sub_category : ""
                        },
                        freeze: true,
                        freeze_message: "loading items...",
                        callback: function (r) {
                            console.log(r.message, "r.message-------------");
                            if (r.message) {
                                console.log(r.message, "r.message-------------");
                                var item_row = cur_frm.add_child("items");
                                item_row.item_code = r.message.item_code;
                                item_row.item_name = r.message.item_name;
                                item_row.qty = r.message.qty;
                                item_row.uom = r.message.uom;
                                item_row.rate = r.message.rate;
                                item_row.amount = r.message.amount;
                                cur_frm.refresh_fields("items");
                               
                            }
                        }
                    });
                }
                
            }
        }
    }
});
