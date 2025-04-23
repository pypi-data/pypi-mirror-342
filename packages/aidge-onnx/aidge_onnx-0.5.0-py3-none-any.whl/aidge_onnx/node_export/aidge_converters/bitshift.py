"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import aidge_core
from onnx import helper
from aidge_onnx.node_export import auto_register_export

def DirectionAttrToString(attr):
    if(attr == aidge_core.BitShiftOp.BitShiftDirection.Right):
        return "RIGHT"
    return "LEFT"


@auto_register_export("BitShift")
def export_bitshift(
    aidge_node: aidge_core.Node,
    node_inputs_name,
    node_outputs_name,
    opset:int = None,
    verbose: bool = False,
    **kwargs) -> None:
    aidge_operator = aidge_node.get_operator()
    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="BitShift",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )

    onnx_node.attribute.append(
        helper.make_attribute(
            "direction",
            DirectionAttrToString(aidge_operator.attr.get_attr("BitShiftdirection"))
    ))
    return [onnx_node]
