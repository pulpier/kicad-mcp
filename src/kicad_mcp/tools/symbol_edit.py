"""Symbol editing tools for .kicad_sch files via kiutils."""

import copy
import uuid as _uuid
from kiutils.schematic import Schematic
from kiutils.items.common import Position, Property


def _load(filepath: str) -> Schematic:
    return Schematic.from_file(filepath)


def _find_symbol(sch: Schematic, reference: str = None, uuid: str = None):
    """Find a symbol by reference designator or UUID. Returns (index, symbol) or raises."""
    for i, sym in enumerate(sch.schematicSymbols):
        if uuid and sym.uuid == uuid:
            return i, sym
        if reference:
            for p in sym.properties:
                if p.key == "Reference" and p.value == reference:
                    return i, sym
    ident = reference or uuid
    raise ValueError(f"Symbol not found: {ident}")


def _sym_summary(sym) -> dict:
    props = {p.key: p.value for p in sym.properties}
    return {
        "uuid": sym.uuid,
        "lib_id": sym.libId,
        "reference": props.get("Reference"),
        "value": props.get("Value"),
        "position": {"x": sym.position.X, "y": sym.position.Y, "angle": sym.position.angle},
    }


def move_symbol(filepath: str, reference: str = None, uuid: str = None,
                x: float = None, y: float = None, angle: float = None) -> dict:
    """Move a symbol to a new position.

    Identify the symbol by reference (e.g. "R1") or UUID.
    Only provided coordinates are changed; others stay the same.
    """
    sch = _load(filepath)
    _, sym = _find_symbol(sch, reference, uuid)
    if x is not None:
        sym.position.X = x
    if y is not None:
        sym.position.Y = y
    if angle is not None:
        sym.position.angle = angle
    sch.to_file()
    return {"status": "moved", "symbol": _sym_summary(sym)}


def set_symbol_property(filepath: str, key: str, value: str,
                        reference: str = None, uuid: str = None) -> dict:
    """Set a property on a symbol (e.g. Reference, Value, Footprint).

    Identify the symbol by reference or UUID.
    If the property doesn't exist, it is added.
    """
    sch = _load(filepath)
    _, sym = _find_symbol(sch, reference, uuid)
    for p in sym.properties:
        if p.key == key:
            p.value = value
            sch.to_file()
            return {"status": "updated", "key": key, "value": value, "symbol": _sym_summary(sym)}
    # Property doesn't exist — add it
    new_prop = Property(key=key, value=value, id=len(sym.properties))
    new_prop.position = Position(X=sym.position.X, Y=sym.position.Y)
    sym.properties.append(new_prop)
    sch.to_file()
    return {"status": "added", "key": key, "value": value, "symbol": _sym_summary(sym)}


def set_symbol_properties(filepath: str, properties: dict,
                          reference: str = None, uuid: str = None) -> dict:
    """Set multiple properties on a symbol at once.

    Args:
        properties: Dict of key-value pairs, e.g. {"Value": "10k", "Footprint": "R_0603"}
    """
    sch = _load(filepath)
    _, sym = _find_symbol(sch, reference, uuid)
    for key, value in properties.items():
        found = False
        for p in sym.properties:
            if p.key == key:
                p.value = value
                found = True
                break
        if not found:
            new_prop = Property(key=key, value=value, id=len(sym.properties))
            new_prop.position = Position(X=sym.position.X, Y=sym.position.Y)
            sym.properties.append(new_prop)
    sch.to_file()
    return {"status": "updated", "properties": properties, "symbol": _sym_summary(sym)}


def delete_symbol(filepath: str, reference: str = None, uuid: str = None) -> dict:
    """Delete a symbol from the schematic.

    Identify the symbol by reference or UUID.
    Warning: does NOT remove connected wires or labels.
    """
    sch = _load(filepath)
    idx, sym = _find_symbol(sch, reference, uuid)
    summary = _sym_summary(sym)
    sch.schematicSymbols.pop(idx)
    sch.to_file()
    return {"status": "deleted", "symbol": summary}


def duplicate_symbol(filepath: str, new_reference: str,
                     x: float = None, y: float = None,
                     reference: str = None, uuid: str = None) -> dict:
    """Duplicate a symbol with a new reference designator.

    The duplicate gets a new UUID and reference. Position defaults to
    the original offset by (10, 0) if not specified.
    """
    sch = _load(filepath)
    _, sym = _find_symbol(sch, reference, uuid)
    new_sym = copy.deepcopy(sym)
    new_sym.uuid = str(_uuid.uuid4())
    new_sym.position.X = x if x is not None else sym.position.X + 10
    new_sym.position.Y = y if y is not None else sym.position.Y
    # Update reference
    for p in new_sym.properties:
        if p.key == "Reference":
            p.value = new_reference
            break
    # Update pin UUIDs
    for pin_key in list(new_sym.pins.keys()):
        new_sym.pins[pin_key] = str(_uuid.uuid4())
    sch.schematicSymbols.append(new_sym)
    sch.to_file()
    return {"status": "duplicated", "original": _sym_summary(sym), "new": _sym_summary(new_sym)}


def mirror_symbol(filepath: str, axis: str = "y",
                  reference: str = None, uuid: str = None) -> dict:
    """Mirror a symbol along an axis.

    Args:
        axis: "x" or "y" (default "y")
    """
    sch = _load(filepath)
    _, sym = _find_symbol(sch, reference, uuid)
    if axis.lower() == "x":
        sym.mirror = "x"
    elif axis.lower() == "y":
        sym.mirror = "y"
    else:
        return {"error": f"Invalid axis: {axis}. Use 'x' or 'y'."}
    sch.to_file()
    return {"status": "mirrored", "axis": axis, "symbol": _sym_summary(sym)}


def set_symbol_dnp(filepath: str, dnp: bool,
                   reference: str = None, uuid: str = None) -> dict:
    """Set or clear the Do-Not-Populate flag on a symbol."""
    sch = _load(filepath)
    _, sym = _find_symbol(sch, reference, uuid)
    sym.dnp = dnp
    sch.to_file()
    return {"status": "updated", "dnp": dnp, "symbol": _sym_summary(sym)}
