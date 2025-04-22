from IPython.display import Markdown, display


class Processor:

    def __init__(self, json: dict, blocks_map: dict, spaces_map: dict):
        self.raw_data = json
        self.id = json["ID"]
        self.name = json["Name"]
        if "Description" in json:
            self.description = json["Description"]
        else:
            self.description = None

        self._load_parent(json["Parent"], blocks_map)
        self._load_ports(json["Ports"], spaces_map)
        self._load_terminals(json["Terminals"], spaces_map)
        self.port_wires = []
        self.terminal_wires = []
        self.wires = []

        if "Subsystem" in json:
            # This will be processed in after the project is loaded
            self.subsystem = json["Subsystem"]
        else:
            self.subsystem = None

    def _load_parent(self, parent, blocks_map):
        assert (
            parent in blocks_map
        ), "The parent block ID of {} is not valid for processor of {}".format(
            parent, self.name
        )
        self.parent = blocks_map[parent]

    def _load_ports(self, ports, spaces_map):
        bad_ports = [space for space in ports if space not in spaces_map]
        assert (
            len(bad_ports) == 0
        ), "The processor {} references port IDs of {} which are not valid port IDs".format(
            self.name, bad_ports
        )
        self.ports = [spaces_map[port] for port in ports]

        assert (
            self.ports == self.parent.domain
        ), "The ports of {} for the processor {} do not match the domain of {} that its parent block {} has".format(
            self.ports, self.name, self.parent.domain, self.parent.name
        )

    def _load_terminals(self, terminals, spaces_map):
        bad_terminals = [space for space in terminals if space not in spaces_map]
        assert (
            len(bad_terminals) == 0
        ), "The processor {} references terminal IDs of {} which are not valid port IDs".format(
            self.name, bad_terminals
        )
        self.terminals = [spaces_map[terminal] for terminal in terminals]

        assert (
            self.terminals == self.parent.codomain
        ), "The terminals of {} for the processor {} do not match the codomain of {} that its parent block {} has".format(
            self.terminals, self.name, self.parent.codomain, self.parent.name
        )

    def _load_subsytem(self, systems_map, processor_map):
        if not self.subsystem:
            return
        assert (
            self.subsystem["System ID"] in systems_map
        ), "Subsystem ID of {} used by the composite processor {} is not in the project".format(
            self.subsystem["System ID"], self.id
        )

        pm = self.subsystem["Port Mappings"]
        tm = self.subsystem["Terminal Mappings"]
        self.subsystem = systems_map[self.subsystem["System ID"]]

        open_ports = self.subsystem.get_open_ports()
        open_ports = {(x[0].id, x[1]): False for x in open_ports}
        terminals = self.subsystem.get_available_terminals(open_only=False)
        terminals = set([(x[0].id, x[1]) for x in terminals])

        self.subsytem_port_mappings = []
        for x in pm:
            key = (x["Processor"], x["Index"])
            assert (
                key in open_ports
            ), "Error in loading subsystem for composite processor {} - {} is not an open port".format(
                self.id, key
            )
            assert not open_ports[
                key
            ], "Error in loading subsystem for composite processor {} - {} is already used as a port".format(
                self.id, key
            )
            self.subsytem_port_mappings.append(
                {"Processor": processor_map[x["Processor"]], "Index": x["Index"]}
            )

        self.subsytem_terminal_mappings = []
        for x in tm:
            key = (x["Processor"], x["Index"])
            assert (
                key in terminals
            ), "Error in loading subsystem for composite processor {} - {} is not a valid terminal".format(
                self.id, key
            )
            self.subsytem_terminal_mappings.append(
                {"Processor": processor_map[x["Processor"]], "Index": x["Index"]}
            )

    def __repr__(self):
        return "< Processor ID: {} Name: {} {}->{}>".format(
            self.id,
            self.name,
            [x.name for x in self.ports],
            [x.name for x in self.terminals],
        )

    def get_shape(self):
        return self.parent

    def create_mermaid_graphic(
        self,
        out="",
        processor_i=0,
        processor_map={},
        ports_map={},
        terminals_map={},
        top_level=True,
        system_i=0,
    ):
        subgraph = "G{}".format(processor_i)
        out += "subgraph G{}[{} - {} Block]\ndirection LR\n".format(
            processor_i, self.name, self.parent.name
        )
        out += "X{}[{}]\n".format(processor_i, self.name)
        processor_map[self.id] = "X{}".format(processor_i)
        ports_map[self.id] = {}
        terminals_map[self.id] = {}
        out += "subgraph {}P[Ports]\ndirection TB\n".format(subgraph)

        l = []
        for i, port in enumerate(self.ports):
            ports_map[self.id][i] = "X{}P{}[{}]".format(
                processor_map[self.id], i, port.name
            )
            out += "{}\n".format(ports_map[self.id][i])
            l.append(
                "{} o--o {}\n".format(ports_map[self.id][i], processor_map[self.id])
            )
        out += "end\n"
        out += "".join(l)

        l = []
        out += "subgraph {}T[Terminals]\ndirection TB\n".format(subgraph)
        for i, terminal in enumerate(self.terminals):
            terminals_map[self.id][i] = "X{}T{}[{}]".format(
                processor_map[self.id], i, terminal.name
            )
            out += "{}\n".format(terminals_map[self.id][i])
            l.append(
                "{} o--o {}\n".format(processor_map[self.id], terminals_map[self.id][i])
            )
        out += "end\n"
        out += "".join(l)
        out += "end\n"

        processor_i += 1
        if top_level:
            out = """```mermaid
---
config:
    layout: elk
---
graph LR
{}
```""".format(
                out
            )

        return out, processor_i, system_i

    def create_mermaid_graphic_composite(
        self,
        out="",
        processor_i=0,
        system_i=0,
        top_level=True,
        processor_map={},
        ports_map={},
        terminals_map={},
    ):
        if self.is_primitive():
            return self.create_mermaid_graphic(
                out=out,
                processor_i=processor_i,
                processor_map=processor_map,
                ports_map=ports_map,
                terminals_map=terminals_map,
                top_level=top_level,
                system_i=system_i,
            )
        subgraph = "GC{}".format(processor_i)
        out += "subgraph GC{}[{} - {} Block]\ndirection LR\n".format(
            processor_i, self.name, self.parent.name
        )
        processor_i += 1

        out, processor_i, system_i = self.subsystem.create_mermaid_graphic(
            out=out,
            system_i=system_i,
            top_level=False,
            processor_map=processor_map,
            ports_map=ports_map,
            terminals_map=terminals_map,
            processor_i=processor_i,
        )
        ports_map[self.id] = {}
        terminals_map[self.id] = {}
        out += "subgraph {}P[Ports]\ndirection TB\n".format(subgraph)
        l = []
        for i, port in enumerate(self.ports):
            ports_map[self.id][i] = "X{}P{}[{}]".format(system_i, i, port.name)
            out += "{}\n".format(ports_map[self.id][i])
            interior = self.subsytem_port_mappings[i]
            interior = ports_map[interior["Processor"].id][interior["Index"]]

            l.append("{} --> {}\n".format(ports_map[self.id][i], interior))
        out += "end\n"
        out += "".join(l)

        l = []
        out += "subgraph {}T[Terminals]\ndirection TB\n".format(subgraph)
        for i, terminal in enumerate(self.terminals):
            terminals_map[self.id][i] = "X{}T{}[{}]".format(system_i, i, terminal.name)
            out += "{}\n".format(terminals_map[self.id][i])

            interior = self.subsytem_terminal_mappings[i]
            interior = terminals_map[interior["Processor"].id][interior["Index"]]

            l.append("{} --> {}\n".format(interior, terminals_map[self.id][i]))
        out += "end\n"
        out += "".join(l)

        out += "end\n"
        if top_level:
            out = """```mermaid
---
config:
    layout: elk
---
graph LR
{}
```""".format(
                out
            )
        processor_i += 1
        return out, processor_i, system_i

    def is_primitive(self):
        return self.subsystem is None

    def get_system(self):
        if self.is_primitive():
            return None
        else:
            return self.subsystem

    def display_mermaid_graphic(self, composite=False):
        if composite:
            display(Markdown(self.create_mermaid_graphic_composite()[0]))
        else:
            display(Markdown(self.create_mermaid_graphic()[0]))

    def find_potential_wires(self, processor2):
        port_wires = []
        terminal_wires = []

        d = {}
        for i, port in enumerate(self.ports):
            if port.id not in d:
                d[port.id] = [i]
            else:
                d[port.id].append(i)
        for i, terminal in enumerate(processor2.terminals):
            if terminal.id in d:
                for j in d[terminal.id]:
                    port_wires.append(
                        {
                            "Parent": terminal.id,
                            "Source": {"Processor": processor2.id, "Index": i},
                            "Target": {"Processor": self.id, "Index": j},
                        }
                    )

        d = {}
        for i, terminal in enumerate(self.terminals):
            if terminal.id not in d:
                d[terminal.id] = [i]
            else:
                d[terminal.id].append(i)
        for i, port in enumerate(processor2.ports):
            if port.id in d:
                for j in d[port.id]:
                    terminal_wires.append(
                        {
                            "Parent": port.id,
                            "Source": {"Processor": self.id, "Index": j},
                            "Target": {"Processor": processor2.id, "Index": i},
                        }
                    )
        return {"Ports": port_wires, "Terminals": terminal_wires}

    def find_potential_subsystems_mappings(self, system):
        port_mappings = []
        terminal_mappings = []

        possible_ports = system.get_open_ports()
        possible_terminals = system.get_available_terminals()

        possible_ports2 = {}
        possible_terminals2 = {}
        for p in possible_ports:
            space = p[2].id
            data = {"Processor": p[0].id, "Index": p[1]}
            if space in possible_ports2:
                possible_ports2[space].append(data)
            else:
                possible_ports2[space] = [data]
        for p in possible_terminals:
            space = p[2].id
            data = {"Processor": p[0].id, "Index": p[1]}
            if space in possible_terminals2:
                possible_terminals2[space].append(data)
            else:
                possible_terminals2[space] = [data]

        for i, port in enumerate(self.ports):
            if port.id in possible_ports2:
                port_mappings.append(possible_ports2[port.id])
            else:
                port_mappings.append([])
        for i, terminal in enumerate(self.terminals):
            if terminal.id in possible_terminals2:
                terminal_mappings.append(possible_terminals2[terminal.id])
            else:
                terminal_mappings.append([])

        return {"Port Mappings": port_mappings, "Terminal Mappings": terminal_mappings}


def load_processor(json, blocks_map, spaces_map):
    return Processor(json, blocks_map, spaces_map)
