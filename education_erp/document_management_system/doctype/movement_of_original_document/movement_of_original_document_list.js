frappe.listview_settings['Movement of Original Document'] = {
    get_indicator: function(doc) {
        // Customize indicator color based on status
        if (doc.status == "Approved") {
            return [__("Approved"), "green", "status,=,Approved"];
        } else if (doc.status == "Pending") {
            return [__("Pending"), "grey", "status,=,Pending"];
        } else if (doc.status == "Rejected") {
            return [__("Rejected"), "red", "status,=,Rejected"];
        } else if (doc.status == "Received") {
            return [__("Received"), "yellow", "status,=,Received"];
        } else if (doc.status == "Returned") {
            return [__("Returned"), "pink", "status,=,Returned"];
        }else {
            return [__("Draft"), "darkgrey", "status,!=,Approved|Pending|Rejected|Received|Returned"];
        }
    }
};