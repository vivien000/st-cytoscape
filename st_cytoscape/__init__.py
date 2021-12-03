import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "st_cytoscape", url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_cytoscape", path=build_dir)


def cytoscape(
    elements,
    stylesheet,
    width="100%",
    height="300px",
    layout={"name": "fcose", "animationDuration": 0},
    selection_type="additive",
    user_zooming_enabled=True,
    user_panning_enabled=True,
    min_zoom=1e-50,
    max_zoom=1e50,
    key=None,
):
    """Creates a new instance of a Cytoscape.js graph.

    Parameters
    ----------
    elements: list
        The list of nodes and edges of the graph
        (cf. https://js.cytoscape.org/#notation/elements-json)
    stylesheet: list
        The style used for the graph (cf. https://js.cytoscape.org/#style)
    width: string
        The CSS width attribute of the graph's container
    height: string
        The CSS height attribute of the graph's container
    layout: dict
        The layout options for the graph (cf. https://js.cytoscape.org/#layouts)
    seletion_type: string ("single" or "additive")
        Cf. https://js.cytoscape.org/#core/initialisation
    user_zooming_enabled: boolean
        Cf. https://js.cytoscape.org/#core/initialisation
    user_panning_enabled: boolean
        Cf. https://js.cytoscape.org/#core/initialisation
    min_zoom: float
        Cf. https://js.cytoscape.org/#core/initialisation
    max_zoom: float
        Cf. https://js.cytoscape.org/#core/initialisation
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        A dictionary containing the list of the ids of selected nodes ("nodes"
        key) and the list of the ids of the selected edges ("edges" key)
    """

    default = {"nodes": [], "edges": []}
    for e in elements:
        if "selected" in e:
            if e["selected"] and "data" in e and "id" in e["data"]:
                if "source" in e["data"]:
                    default["edges"].append(e["data"]["id"])
                else:
                    default["nodes"].append(e["data"]["id"])

    component_value = _component_func(
        elements=elements,
        stylesheet=stylesheet,
        width=width,
        height=height,
        layout=layout,
        selectionType=selection_type,
        userZoomingEnabled=user_zooming_enabled,
        userPanningEnabled=user_panning_enabled,
        minZoom=min_zoom,
        maxZoom=max_zoom,
        key=key,
        default=default,
    )
    return component_value


if not _RELEASE:
    import streamlit as st

    elements = [
        {"data": {"id": "X"}, "selected": True, "selectable": False},
        {"data": {"id": "Y"}},
        {"data": {"id": "Z"}},
        {"data": {"source": "X", "target": "Y", "id": "X➞Y"}},
        {"data": {"source": "Z", "target": "Y", "id": "Z➞Y"}},
        {"data": {"source": "Z", "target": "X", "id": "Z➞X"}},
    ]

    stylesheet = [
        {"selector": "node", "style": {"label": "data(id)", "width": 20, "height": 20}},
        {
            "selector": "edge",
            "style": {
                "width": 3,
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
            },
        },
    ]

    selected = cytoscape(elements, stylesheet, key="graph")

    st.markdown("**Selected nodes**: %s" % (", ".join(selected["nodes"])))
    st.markdown("**Selected edges**: %s" % (", ".join(selected["edges"])))
