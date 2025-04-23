DAY = 86400

# ==============______GET PRETTY RESPRESENTATION______=========================================================================================== GET PRETTY RESPRESENTATION
def get_pretty_representation(desc: dict) -> str:
    """Returns json dumped text of given dict"""
    import json

    return json.dumps(desc, indent=4, ensure_ascii=False)


