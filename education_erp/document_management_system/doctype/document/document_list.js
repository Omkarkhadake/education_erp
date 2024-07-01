frappe.listview_settings['Document'] = {
    get_indicator: function(doc) {
        // Customize indicator color based on status
        if (doc.status == "Approved") {
            return [__("Approved"), "green", "status,=,Approved"];
        } else if(doc.status == "Pending") {
            return [__("Pending"), "grey", "status,=,Pending"];
        } else if(doc.status == "Rejected") {
            return [__("Rejected"), "red", "status,=,Rejected"];
        } else {
            return [__("Draft"), "darkgrey", "status,!=,Approved|Pending|Rejected"];
        }
    }
};