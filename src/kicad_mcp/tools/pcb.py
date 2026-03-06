"""PCB file tools using kiutils — read/write .kicad_pcb files."""

from kiutils.board import Board


def _load(filepath: str) -> Board:
    return Board.from_file(filepath)


def get_pcb_info(filepath: str) -> dict:
    """Get overview of a PCB file."""
    board = _load(filepath)

    # Count trace types
    from collections import Counter
    trace_types = Counter(type(t).__name__ for t in board.traceItems)

    return {
        "filepath": board.filePath,
        "version": board.version,
        "generator": board.generator,
        "paper": str(board.paper),
        "general": {
            "thickness": board.general.thickness,
        },
        "layers": [{"name": l.name, "type": l.type, "id": l.ordinal} for l in board.layers],
        "counts": {
            "footprints": len(board.footprints),
            "tracks": trace_types.get("Segment", 0),
            "vias": trace_types.get("Via", 0),
            "arcs": trace_types.get("Arc", 0),
            "nets": len(board.nets),
            "zones": len(board.zones),
            "graphic_items": len(board.graphicItems),
            "dimensions": len(board.dimensions),
            "groups": len(board.groups),
        },
    }


def get_pcb_footprints(filepath: str) -> list[dict]:
    """Get all footprints in a PCB."""
    board = _load(filepath)
    result = []
    for fp in board.footprints:
        props = fp.properties if isinstance(fp.properties, dict) else {}

        result.append({
            "lib_id": fp.libId,
            "reference": props.get("Reference", ""),
            "value": props.get("Value", ""),
            "position": {"x": fp.position.X, "y": fp.position.Y, "angle": fp.position.angle},
            "layer": fp.layer,
            "locked": fp.locked,
            "pads_count": len(fp.pads),
            "path": fp.path,
            "description": fp.description,
        })
    return result


def get_pcb_nets(filepath: str) -> list[dict]:
    """Get all nets in a PCB."""
    board = _load(filepath)
    return [{"number": net.number, "name": net.name} for net in board.nets]


def get_pcb_tracks(filepath: str) -> list[dict]:
    """Get all tracks (segments, vias, arcs) in a PCB."""
    board = _load(filepath)
    result = []
    for item in board.traceItems:
        entry = {"type": type(item).__name__}
        if hasattr(item, 'start'):
            entry["start"] = {"x": item.start.X, "y": item.start.Y}
        if hasattr(item, 'end'):
            entry["end"] = {"x": item.end.X, "y": item.end.Y}
        if hasattr(item, 'position'):
            entry["position"] = {"x": item.position.X, "y": item.position.Y}
        if hasattr(item, 'width'):
            entry["width"] = item.width
        if hasattr(item, 'size'):
            entry["size"] = item.size
        if hasattr(item, 'layer'):
            entry["layer"] = item.layer
        if hasattr(item, 'layers'):
            entry["layers"] = item.layers
        if hasattr(item, 'net'):
            entry["net"] = item.net
        result.append(entry)
    return result


def get_pcb_zones(filepath: str) -> list[dict]:
    """Get all copper zones in a PCB."""
    board = _load(filepath)
    result = []
    for zone in board.zones:
        result.append({
            "uuid": zone.uuid if hasattr(zone, 'uuid') else None,
            "net": zone.net if hasattr(zone, 'net') else None,
            "net_name": zone.netName if hasattr(zone, 'netName') else None,
            "layer": zone.layer if hasattr(zone, 'layer') else None,
            "layers": zone.layers if hasattr(zone, 'layers') else None,
        })
    return result


def get_pcb_layers(filepath: str) -> list[dict]:
    """Get board layer definitions."""
    board = _load(filepath)
    return [{"id": l.ordinal, "name": l.name, "type": l.type, "user_name": l.userName if hasattr(l, 'userName') else None} for l in board.layers]


def get_pcb_setup(filepath: str) -> dict:
    """Get board setup (stackup, design rules, etc.)."""
    board = _load(filepath)
    setup = board.setup
    result = {
        "thickness": board.general.thickness,
    }
    if setup.stackup:
        result["stackup"] = {
            "layers": [{
                "name": sl.name,
                "type": sl.type,
                "thickness": sl.thickness if hasattr(sl, 'thickness') else None,
                "material": sl.material if hasattr(sl, 'material') else None,
            } for sl in setup.stackup.layers]
        }
    return result
