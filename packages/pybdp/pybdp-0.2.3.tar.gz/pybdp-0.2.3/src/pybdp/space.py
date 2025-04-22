class Space:
    def __init__(self, json: dict):
        self.raw_data = json
        self.id = json["ID"]
        self.name = json["Name"]
        if "Description" in json:
            self.description = json["Description"]
        else:
            self.description = None

    def __repr__(self):
        return "< Space ID: {} Name: {} >".format(self.id, self.name)


def load_space(json: dict):
    return Space(json)
