"""Wire, label, and junction editing tools for .kicad_sch files via kiutils."""

import uuid as _uuid
from kiutils.schematic import Schematic
from kiutils.items.schitems import Connection, Junction, LocalLabel, GlobalLabel
from kiutils.items.common import Position


def _load(filepath: str) -> Schematic:
    return Schematic.from_file(filepath)


def add_wire(filepath: str, x1: float, y1: float, x2: float, y2: float) -> dict:
    """Add a wire between two points."""
    sch = _load(filepath)
    wire = Connection(
        type="wire",
        points=[Position(X=x1, Y=y1), Position(X=x2, Y=y2)],
        uuid=str(_uuid.uuid4()),
    )
    sch.graphicalItems.append(wire)
    sch.to_file()
    return {
        "status": "added",
        "uuid": wire.uuid,
        "points": [{"x": x1, "y": y1}, {"x": x2, "y": y2}],
    }


def add_wire_path(filepath: str, points: list[dict]) -> dict:
    """Add a multi-segment wire path. Each segment connects consecutive points.

    Args:
        points: List of {"x": float, "y": float} dicts, minimum 2 points.
    """
    if len(points) < 2:
        return {"error": "Need at least 2 points"}
    sch = _load(filepath)
    uuids = []
    for i in range(len(points) - 1):
        wire = Connection(
            type="wire",
            points=[
                Position(X=points[i]["x"], Y=points[i]["y"]),
                Position(X=points[i + 1]["x"], Y=points[i + 1]["y"]),
            ],
            uuid=str(_uuid.uuid4()),
        )
        sch.graphicalItems.append(wire)
        uuids.append(wire.uuid)
    sch.to_file()
    return {"status": "added", "segments": len(uuids), "uuids": uuids}


def delete_wire(filepath: str, uuid: str) -> dict:
    """Delete a wire by UUID."""
    sch = _load(filepath)
    for i, item in enumerate(sch.graphicalItems):
        if hasattr(item, "uuid") and item.uuid == uuid:
            sch.graphicalItems.pop(i)
            sch.to_file()
            return {"status": "deleted", "uuid": uuid}
    return {"error": f"Wire not found: {uuid}"}


def add_junction(filepath: str, x: float, y: float) -> dict:
    """Add a junction at a point where wires cross."""
    sch = _load(filepath)
    junction = Junction(
        position=Position(X=x, Y=y),
        uuid=str(_uuid.uuid4()),
    )
    sch.junctions.append(junction)
    sch.to_file()
    return {"status": "added", "uuid": junction.uuid, "position": {"x": x, "y": y}}


def delete_junction(filepath: str, uuid: str) -> dict:
    """Delete a junction by UUID."""
    sch = _load(filepath)
    for i, j in enumerate(sch.junctions):
        if j.uuid == uuid:
            sch.junctions.pop(i)
            sch.to_file()
            return {"status": "deleted", "uuid": uuid}
    return {"error": f"Junction not found: {uuid}"}


def add_label(filepath: str, text: str, x: float, y: float,
              angle: float = 0) -> dict:
    """Add a local net label at a position."""
    sch = _load(filepath)
    label = LocalLabel(
        text=text,
        position=Position(X=x, Y=y, angle=angle),
        uuid=str(_uuid.uuid4()),
    )
    sch.labels.append(label)
    sch.to_file()
    return {"status": "added", "uuid": label.uuid, "text": text,
            "position": {"x": x, "y": y, "angle": angle}}


def add_global_label(filepath: str, text: str, x: float, y: float,
                     angle: float = 0, shape: str = "input") -> dict:
    """Add a global label at a position.

    Args:
        shape: One of "input", "output", "bidirectional", "tri_state", "passive"
    """
    sch = _load(filepath)
    label = GlobalLabel(
        text=text,
        shape=shape,
        position=Position(X=x, Y=y, angle=angle),
        uuid=str(_uuid.uuid4()),
    )
    sch.globalLabels.append(label)
    sch.to_file()
    return {"status": "added", "uuid": label.uuid, "text": text, "shape": shape,
            "position": {"x": x, "y": y, "angle": angle}}


def delete_label(filepath: str, uuid: str) -> dict:
    """Delete a label (local or global) by UUID."""
    sch = _load(filepath)
    for i, l in enumerate(sch.labels):
        if l.uuid == uuid:
            sch.labels.pop(i)
            sch.to_file()
            return {"status": "deleted", "uuid": uuid, "type": "local"}
    for i, l in enumerate(sch.globalLabels):
        if l.uuid == uuid:
            sch.globalLabels.pop(i)
            sch.to_file()
            return {"status": "deleted", "uuid": uuid, "type": "global"}
    return {"error": f"Label not found: {uuid}"}


def move_label(filepath: str, uuid: str, x: float = None, y: float = None,
               angle: float = None) -> dict:
    """Move a label (local or global) to a new position."""
    sch = _load(filepath)
    for label_list, label_type in [(sch.labels, "local"), (sch.globalLabels, "global")]:
        for l in label_list:
            if l.uuid == uuid:
                if x is not None:
                    l.position.X = x
                if y is not None:
                    l.position.Y = y
                if angle is not None:
                    l.position.angle = angle
                sch.to_file()
                return {"status": "moved", "uuid": uuid, "type": label_type, "text": l.text,
                        "position": {"x": l.position.X, "y": l.position.Y, "angle": l.position.angle}}
    return {"error": f"Label not found: {uuid}"}
