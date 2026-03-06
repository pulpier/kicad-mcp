"""Schematic file tools using kiutils — read/write .kicad_sch files."""

from kiutils.schematic import Schematic


def _load(filepath: str) -> Schematic:
    return Schematic.from_file(filepath)


def get_schematic_info(filepath: str) -> dict:
    """Get overview of a schematic file."""
    sch = _load(filepath)
    return {
        "filepath": sch.filePath,
        "version": sch.version,
        "generator": sch.generator,
        "uuid": sch.uuid,
        "paper": str(sch.paper),
        "counts": {
            "symbols": len(sch.schematicSymbols),
            "graphical_items": len(sch.graphicalItems),
            "labels": len(sch.labels),
            "global_labels": len(sch.globalLabels),
            "hierarchical_labels": len(sch.hierarchicalLabels),
            "junctions": len(sch.junctions),
            "no_connects": len(sch.noConnects),
            "bus_entries": len(sch.busEntries),
            "sheets": len(sch.sheets),
            "lib_symbols": len(sch.libSymbols),
            "images": len(sch.images),
            "texts": len(sch.texts),
            "text_boxes": len(sch.textBoxes),
            "shapes": len(sch.shapes),
        },
    }


def get_schematic_symbols(filepath: str) -> list[dict]:
    """Get all symbols in a schematic."""
    sch = _load(filepath)
    result = []
    for sym in sch.schematicSymbols:
        props = {}
        for p in sym.properties:
            props[p.key] = p.value

        result.append({
            "uuid": sym.uuid,
            "lib_id": sym.libId,
            "position": {"x": sym.position.X, "y": sym.position.Y, "angle": sym.position.angle},
            "unit": sym.unit,
            "mirror": sym.mirror,
            "dnp": sym.dnp,
            "in_bom": sym.inBom,
            "on_board": sym.onBoard,
            "properties": props,
            "pins": sym.pins,
        })
    return result


def get_schematic_labels(filepath: str) -> list[dict]:
    """Get all labels (local, global, hierarchical) in a schematic."""
    sch = _load(filepath)
    result = []

    for label in sch.labels:
        result.append({
            "type": "label",
            "uuid": label.uuid,
            "text": label.text,
            "position": {"x": label.position.X, "y": label.position.Y, "angle": label.position.angle},
        })

    for label in sch.globalLabels:
        result.append({
            "type": "global_label",
            "uuid": label.uuid,
            "text": label.text,
            "position": {"x": label.position.X, "y": label.position.Y, "angle": label.position.angle},
        })

    for label in sch.hierarchicalLabels:
        result.append({
            "type": "hierarchical_label",
            "uuid": label.uuid,
            "text": label.text,
            "position": {"x": label.position.X, "y": label.position.Y, "angle": label.position.angle},
        })

    return result


def get_schematic_sheets(filepath: str) -> list[dict]:
    """Get hierarchical sheet references."""
    sch = _load(filepath)
    result = []
    for sheet in sch.sheets:
        sheet_name = sheet.sheetName.value if sheet.sheetName else None
        file_name = sheet.fileName.value if sheet.fileName else None

        result.append({
            "uuid": sheet.uuid,
            "sheet_name": sheet_name,
            "file_name": file_name,
            "position": {"x": sheet.position.X, "y": sheet.position.Y},
            "size": {"width": sheet.width, "height": sheet.height},
            "pins": [{"name": p.name, "uuid": p.uuid} for p in sheet.pins],
        })
    return result


def get_schematic_wires(filepath: str) -> list[dict]:
    """Get all wires and buses (graphical items) in a schematic."""
    sch = _load(filepath)
    result = []
    for item in sch.graphicalItems:
        entry = {
            "uuid": item.uuid if hasattr(item, 'uuid') else None,
            "type": type(item).__name__,
        }
        if hasattr(item, 'points'):
            entry["points"] = [{"x": p.X, "y": p.Y} for p in item.points]
        result.append(entry)
    return result


def get_schematic_lib_symbols(filepath: str) -> list[dict]:
    """Get library symbols embedded in the schematic."""
    sch = _load(filepath)
    result = []
    for sym in sch.libSymbols:
        props = {}
        for p in sym.properties:
            props[p.key] = p.value

        result.append({
            "id": sym.id if hasattr(sym, 'id') else sym.entryName,
            "properties": props,
            "pins_count": sum(len(u.pins) for u in sym.units) if hasattr(sym, 'units') else 0,
        })
    return result
