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


//  Testing 

// frappe.listview_settings['Document'] = {
//     refresh: function(listview) {
//         function showApproveButton() {
//             const checked_items = listview.get_checked_items();
//             console.log("Checked items:", checked_items.length);

//             // Check if any checkboxes are selected
//             if (checked_items.length > 0) {
//                 // Fetch details for checked items including approving_authority_id
//                 frappe.call({
//                     method: "frappe.client.get_list",
//                     args: {
//                         doctype: "Document",
//                         fields: ["name", "status", "approving_authority_id"],
//                         filters: {
//                             name: ["in", checked_items.map(doc => doc.name)]
//                         }
//                     },
//                     callback: function(r) {
//                         if (!r.exc && r.message) {
//                             const documents = r.message;
//                             console.log("Fetched documents:", documents);

//                             // Check if all selected documents can be approved
//                             const can_show_button = documents.every(doc => {
//                                 const condition = doc.status === 'Pending' && frappe.session.user === doc.approving_authority_id;
//                                 console.log(`Checking document: ${doc.name}, Status: ${doc.status}, Approving Authority: ${doc.approving_authority_id}, Condition: ${condition}`);
//                                 return condition;
//                             });

//                             console.log("Can show button:", can_show_button);

//                             // Add or remove Approve button based on conditions
//                             if (can_show_button) {
//                                 const func = function() {
//                                     frappe.confirm("Are you sure you want to approve the selected documents?", function () {
//                                         console.log('checked items', documents.length)
//                                         const promises = documents.map(doc => {
//                                             console.log("message called ",doc.name)
//                                             static_name=doc.name
//                                             //checked_items.shift()
                                            
//                                             return frappe.call({
//                                                 method: "frappe.client.set_value",
//                                                 args: {
//                                                     doctype: "Document",
//                                                     name: static_name,
//                                                     fieldname: "status",
//                                                     value: "Approved"
//                                                 },
//                                             });
//                                         });

//                                         Promise.all(promises).then(() => {
//                                             listview.refresh();
//                                             // After approval, re-check and re-display the Approve button
//                                             showApproveButton();
//                                         });
//                                     });
//                                 }
//                                 if (!listview.page.inner_toolbar.find(".custom-approve-btn").length) {
//                                     // Approve button does not exist, add a new inner button
//                                     let approve_btn = listview.page.add_inner_button("Approve", func);
//                                     approve_btn.addClass("custom-approve-btn");
//                                     console.log("Approve button added.");
//                                 } else {
//                                     // Approve button already exists, update the callback on the inner button instance
     
//                                 }
//                             } else {
//                                 listview.page.inner_toolbar.find(".custom-approve-btn").remove();
//                                 console.log("Approve button removed.");
//                             }
//                         } else {
//                             console.error("Error fetching documents:", r.exc);
//                         }
//                     }
//                 });
//             } else {
//                 // If no checkboxes are selected, remove the Approve button
//                 listview.page.inner_toolbar.find(".custom-approve-btn").remove();
//                 console.log("No checked items. Approve button removed.");
//             }
//         }

//         // Re-check whenever the selection changes
//         $(document).on('change', '.list-row-checkbox', function() {
//             showApproveButton();
//         });

//         // Initial check when the list view is refreshed
//         showApproveButton();
//     },
//     get_indicator: function(doc) {
//         // Customize indicator color based on status
//         if (doc.status === "Approved") {
//             return [__("Approved"), "green", "status,=,Approved"];
//         } else if (doc.status === "Pending") {
//             return [__("Pending"), "grey", "status,=,Pending"];
//         } else if (doc.status === "Rejected") {
//             return [__("Rejected"), "red", "status,=,Rejected"];
//         } else {
//             return [__("Draft"), "darkgrey", "status,!=,Approved|Pending|Rejected"];
//         }
//     }
// };

