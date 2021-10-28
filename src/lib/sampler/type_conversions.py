class TypeConversions:
    # different cast option for the elements defined by selection below
    FIELD_SAMPLER_CAST_INT = "INT"
    FIELD_SAMPLER_CAST_FLOAT = "FLOAT"
    FIELD_SAMPLER_CAST_BOOL = "BOOL"
    FIELD_SAMPLER_CAST_STRING = "STRING"

    @staticmethod
    def convert(value: any, convert_type: str):
        if convert_type == TypeConversions.FIELD_SAMPLER_CAST_INT:
            return int(value)
        if convert_type == TypeConversions.FIELD_SAMPLER_CAST_FLOAT:
            return float(value)
        if convert_type == TypeConversions.FIELD_SAMPLER_CAST_BOOL:
            return str(str(value).lower() == "true").lower()
        if convert_type == TypeConversions.FIELD_SAMPLER_CAST_STRING:
            return "\"%s\"" % str(value)
        return value
