def amf0_Get_Marker(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))

def amf0_Get_Object_Property(unhandled_Bytes):
    Object_Property_Dict = {}
    step = amf0_Get_UTF8_string_Len_Raw(unhandled_Bytes)
    unhandled_Bytes = step[0]
    name_Len_Raw = step[1]
    step = amf0_Get_UTF8_string_Raw(unhandled_Bytes,name_Len_Raw)
    unhandled_Bytes = step[0]
    name_String_Raw = step[1]
    Object_Property_Dict['name'] = {}
    Object_Property_Dict['name']['len'] = name_Len_Raw
    Object_Property_Dict['name']['string'] = name_String_Raw
    step = amf0_Get_Value_Type(unhandled_Bytes)
    unhandled_Bytes = step[0]
    Object_Property_Dict['value'] = step[1]
    return((unhandled_Bytes,Object_Property_Dict))

def amf0_Get_Value_Type_Body(unhandled_Bytes,marker_Raw,amf0_Data_Types):
    if(marker_Raw == amf0_Data_Types['name-to-marker']['number-marker']):
        return(amf0_Get_DOUBLE(unhandled_Bytes))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['boolean-marker']):
        return(amf0_Get_U8(unhandled_Bytes))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['string-marker']):
        step = amf0_Get_UTF8_string_Len_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        len_Raw = step[1]
        step = amf0_Get_UTF8_string_Raw(unhandled_Bytes,len_Raw)
        unhandled_Bytes = step[0]
        string = step[1]
        string_Value_Type_Body = {}
        string_Value_Type_Body['len'] = len_Raw
        string_Value_Type_Body['string'] = string
        return((unhandled_Bytes,string_Value_Type_Body))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['object-marker']):
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['movieclip-marker']):
        return((unhandled_Bytes,{}))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['null-marker']):
        return((unhandled_Bytes,b''))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['undefined-marker']):
        return((unhandled_Bytes,b''))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['reference-marker']):
        return(amf0_Get_U16(unhandled_Bytes))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['ecma-array-marker']):
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['object-end-marker']):
        return((unhandled_Bytes,b''))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['strict-array-marker']):
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['date-marker']):
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['long-string-marker']):
        step = amf0_Get_LUTF8_string_Len_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        len_Raw = step[1]
        step = amf0_Get_LUTF8_string_Raw(unhandled_Bytes,len_Raw)
        unhandled_Bytes = step[0]
        long_String = step[1]
        long_String_Value_Type_Body = {}
        long_String_Value_Type_Body['len'] = len_Raw
        long_String_Value_Type_Body['string'] = long_String
        return((unhandled_Bytes,long_String_Value_Type_Body))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['unsupported-marker']):
        return((unhandled_Bytes,b''))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['recordset-marker']):
        return((unhandled_Bytes,{}))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['xml-document-marker']):
        step = amf0_Get_LUTF8_string_Len_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        len_Raw = step[1]
        step = amf0_Get_LUTF8_string_Raw(unhandled_Bytes,len_Raw)
        unhandled_Bytes = step[0]
        xml_Document_Raw_L = step[1]
        xml_Document_Value_Type_Body = {}
        xml_Document_Value_Type_Body['len'] = len_Raw
        xml_Document_Value_Type_Body['string'] = xml_Document_Raw_L
        return((unhandled_Bytes,xml_Document_Value_Type_Body))
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['typed-object-marker']):
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['avmplus-object-marker']):
        return(amf3_Get_Value_Type(unhandled_Bytes))
    else:
        return(None)
