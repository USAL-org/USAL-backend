from usal.api.schema.request.university_request import StateRequest


GelDBType = str
InputModel = type
SheetName = str | None

DefaultDataMapping = dict[str, list[tuple[GelDBType, InputModel, SheetName]]]


FieldMapping = dict[str, str]


def get_field_mapping(input_model: InputModel) -> FieldMapping:
    """Generate a mapping from input model fields to EdgeDB properties.

    By default, assumes field names match exactly. Override this for custom mappings.
    """
    return {field: field for field in input_model.__annotations__}


DEFAULT_DATA_DICT: DefaultDataMapping = {
    "usal/defaults/data/states_with_country.xlsx": [
        (
            "State",
            StateRequest,
            "usa_states",
        ),
    ],
}
