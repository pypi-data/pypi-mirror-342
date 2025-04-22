class Wire:
    def __init__(self, json: dict, processors_map: dict, spaces_map: dict):
        self.raw_data = json
        self.id = json["ID"]
        self._load_parent(json["Parent"], spaces_map)
        self._load_source(json["Source"], processors_map)
        self._load_target(json["Target"], processors_map)

    def _load_parent(self, parent, spaces_map):
        assert (
            parent in spaces_map
        ), "The parent space ID of {} is not valid for wire of {}".format(
            parent, self.id
        )
        self.parent = spaces_map[parent]

    def _load_source(self, source, processors_map):
        assert (
            source["Processor"] in processors_map
        ), "The source processor ID of {} is not valid for wire of {}".format(
            source["Processor"], self.id
        )
        processor = processors_map[source["Processor"]]
        assert source["Index"] < len(
            processor.terminals
        ), "Index of {} is out of range for the 0-indexed array of terminals in {} (length={}). Error encountered on wire {}.".format(
            source["Index"], processor.name, len(processor.terminals), self.id
        )
        a = processor.terminals[source["Index"]]
        b = self.parent
        assert (
            a == b
        ), "The terminal space {} of processor {} does not match the wire space {} for wire {}".format(
            a, processor.name, b, self.id
        )
        self.source = {"Processor": processor, "Index": source["Index"]}

    def _load_target(self, target, processors_map):
        assert (
            target["Processor"] in processors_map
        ), "The target processor ID of {} is not valid for wire of {}".format(
            target["Processor"], self.id
        )
        processor = processors_map[target["Processor"]]
        assert target["Index"] < len(
            processor.ports
        ), "Index of {} is out of range for the 0-indexed array of terminals in {} (length={}). Error encountered on wire {}.".format(
            target["Index"], processor.name, len(processor.ports), self.id
        )

        a = processor.ports[target["Index"]]
        b = self.parent
        assert (
            a == b
        ), "The port space {} of processor {} does not match the wire space {} for wire {}".format(
            a, processor.name, b, self.id
        )

        self.target = {"Processor": processor, "Index": target["Index"]}

    def __repr__(self):
        return "< Wire ID: {} Space: {} Source: ({}, {}) Target: ({}, {}) >".format(
            self.id,
            self.parent.name,
            self.source["Processor"].name,
            self.source["Index"],
            self.target["Processor"].name,
            self.target["Index"],
        )

    def create_mermaid_graphic(self, out, terminals_map, ports_map):
        out += "{} ---> {}\n".format(
            terminals_map[self.source["Processor"].id][self.source["Index"]],
            ports_map[self.target["Processor"].id][self.target["Index"]],
        )
        return out


def load_wire(json, blocks_map, spaces_map):
    return Wire(json, blocks_map, spaces_map)
