frappe.listview_settings['Wethaaq Contract'] = {
    get_indicator: function (doc) {
        let status_colors = {
            "Draft": "grey",
            "Review": "orange",
            "Signed": "blue",
            "Active": "green",
            "Expired": "red",
            "Terminated": "darkgrey",
            "Archived": "black"
        };

        let status = doc.status || "Draft";
        let color = status_colors[status] || "grey";

        return [__(status), color, "status,=," + status];
    }
};
