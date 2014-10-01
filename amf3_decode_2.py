def amf3_Get_Marker(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))


def amf3_Get_Value_Type(unhandled_Bytes,amf3_Data_Types)
    Value_Type_Dict = {}
    step = amf3_Get_Marker(unhandled_Bytes)
    unhandled_Bytes = step[0]
    marker_Raw = step[1]
    Value_Type_Dict['marker'] = marker_Raw 
    step = amf0_Get_Value_Type_Body(unhandled_Bytes,marker_Raw,amf3_Data_Types)
    unhandled_Bytes = step[0]
    value_Type_Body = step[1]
    Value_Type_Dict['value-type-body'] = value_Type_Body
    return((unhandled_Bytes,Value_Type_Dict))

