def build_from_config(fields, prompt_fn):
    data = {}

    for name, required, cast, validate in fields:
        data[name] = prompt_fn(name, required, cast, validate)

    return {"data": data}

def build_update_from_config(id_field, id_label, fields, prompt_fn):
    entity_id = prompt_fn(id_label, required=True)

    data = {}

    for name, _, cast, validate in fields:
        if name == id_field:
            continue

        value = prompt_fn(
            name,
            required=False,
            cast=cast,
            validate=lambda v, val=validate: val(v) if (val and v is not None) else True
        )

        if value is not None:  # 🚀 ONLY include provided values
            data[name] = value

    return {
        id_field: entity_id,
        "data": data
    }

def build_ID_context(field_name, label, prompt_fn):
    return {
        field_name: prompt_fn(label, required=True)
    }

