def get_schema(df):
    naming_correspondence = {"object":"string", "float64":"float", "int64":"int", "uint8":"int"}
    return [{"name":column, "type":[naming_correspondence[str(df[column].dtype)] \
                                    if str(df[column].dtype) in naming_correspondence.keys() \
                                    else str(df[column].dtype), "null"]} \
                for column in df.columns]