frappe.ui.form.on('Sales Invoice', {
    validate: function(frm) {
        var totalCustomMRP = 0;
        
        frm.doc.items.forEach(function(item) {
            if (item.custom_mrp) {
                totalCustomMRP += parseFloat(item.custom_mrp) || 0;
            }
        });
        console.log('totalCustomMRP', totalCustomMRP);
        frm.set_value('custom_total_mrp', totalCustomMRP);
    }
});
