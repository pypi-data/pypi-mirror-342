class Block:
    def __init__(self, json: dict, spaces_map):
        self.raw_data = json
        self.id = json["ID"]
        self.name = json["Name"]
        if "Description" in json:
            self.description = json["Description"]
        else:
            self.description = None
        self.domain = json["Domain"]
        self.codomain = json["Codomain"]
        self._load_space_references(spaces_map)

    def _load_space_references(self, spaces_map):
        # Assert the space IDs are valid
        for space in self.domain:
            assert (
                space in spaces_map
            ), f"Space ID {space} referenced in {self.name} domain not found in spaces"

        for space in self.codomain:
            assert (
                space in spaces_map
            ), f"Space ID {space} referenced in {self.name} codomain not found in spaces"

        # Link the spaces
        self.domain = [spaces_map[space] for space in self.domain]
        self.codomain = [spaces_map[space] for space in self.codomain]

    def __repr__(self):
        return "< Block ID: {} Name: {} {}->{}>".format(
            self.id,
            self.name,
            [x.name for x in self.domain],
            [x.name for x in self.codomain],
        )


def load_block(json: dict, spaces_map):
    return Block(json, spaces_map)
