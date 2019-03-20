/**
 * The content of coloredPanels is used to parse the following markdown into a colored panel
 * <div class="note">
 *      [predefined-title]
 *      body of the note ...
 * </div>
 *
 * In order for the above to be presented as a colored panel, `predefined-title` placed in `[]`
 * must map to one object in the following `coloredPanels` object.
 *
 * The `className` property is in accordance with Twitter Bootstrap's labels: https://getbootstrap.com/docs/4.3/components/alerts/
 */

coloredPanels = {
    important: {
        className: "warning",
        icon: {
            name: "fa fa-star",
            color: "#f1c40f"
        }
    },
    note: {
        className: "info",
        icon: {
            name: "fa fa-info-circle",
            color: "#2980b9"
        }
    },
    advanced: {
        className: "success",
        icon: {
            name: "fas fa-lightbulb",
            color: "#27ae60"
        }
    },
    warning: {
        className: "danger",
        icon: {
            name: "fa fa-exclamation-triangle",
            color: "#F75E62"
        }
    }
}