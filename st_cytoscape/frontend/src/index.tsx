import {
  Streamlit,
  RenderData
} from "streamlit-component-lib"
// @ts-ignore
import cytoscape from 'cytoscape';
// @ts-ignore
import fcose from 'cytoscape-fcose';
// @ts-ignore
import klay from 'cytoscape-klay';

cytoscape.use(fcose);
cytoscape.use(klay);

const div = document.body.appendChild(document.createElement("div"));
let args = '';

function updateComponent(cy: any) {
  Streamlit.setComponentValue({
    'nodes': cy.$('node:selected').map((x: any) => x['_private']['data']['id']),
    'edges': cy.$('edge:selected').map((x: any) => x['_private']['data']['id'])
  })
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail
  let newArgs = JSON.stringify(data.args);
  if (!data.args["key"] || args !== newArgs) {
    args = newArgs;

    // Update the dimension of the graph's container
    div.style.width = data.args["width"];
    div.style.height = data.args["height"];

    // Take into account the Streamlit theme
    let nodeColor: any[] = [];
    if (data.theme) {
      if (data.theme?.backgroundColor) {
        div.style.background = data.theme.backgroundColor;
      }
      nodeColor = [{
        selector: "node:selected",
        style: {
          backgroundColor: data.theme?.primaryColor
        }
      }, {
        selector: "node",
        style: {
          color: data.theme?.textColor,
          fontFamily: data.theme?.font
        }
      }, {
        selector: "edge:selected",
        style: {
          targetArrowColor: data.theme?.primaryColor,
          lineColor: data.theme?.primaryColor
        }
      }]
    }

    //Create the Cytoscape Graph
    let cy = cytoscape({
      container: div,
      elements: data.args["elements"],
      style: data.args["stylesheet"].concat(nodeColor),
      layout: data.args["layout"],
      selectionType: data.args["selectionType"],
      userZoomingEnabled: data.args["userZoomingEnabled"],
      userPanningEnabled: data.args["userPanningEnabled"],
      minZoom: data.args["minZoom"],
      maxZoom: data.args["maxZoom"],
    }).on('select unselect', function () {
      updateComponent(cy);
    });
    updateComponent(cy);
  }

  Streamlit.setFrameHeight()
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
