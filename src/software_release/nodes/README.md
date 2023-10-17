# Node Components

A `Node` is a high-level object which act as a node in sequence of nodes.  
Each node is part of a `Release Wizard` and does the following:  
- receives the input `request` instance
- processes the `request` based on the node logic
- passes the `request` to the next handler if any


`Nodes` implemented without constructor arguments means it can be included  
in a `Release Wizard Config` without any arguments.

Implemented [Node Components](node_components) are in the [node_components](node_components) package.
