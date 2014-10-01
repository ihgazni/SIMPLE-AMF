def amf0_Get_Marker(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))


def amf0_Get_Value_Type(unhandled_Bytes,amf0_Data_Types)
    Value_Type_Dict = {}
    step = amf0_Get_Marker(unhandled_Bytes)
    unhandled_Bytes = step[0]
    marker_Raw = step[1]
    Value_Type_Dict['marker'] = marker_Raw 
    step = amf0_Get_Value_Type_Body(unhandled_Bytes,marker_Raw,amf0_Data_Types)
    unhandled_Bytes = step[0]
    value_Type_Body = step[1]
    Value_Type_Dict['value-type-body'] = value_Type_Body
    return((unhandled_Bytes,Value_Type_Dict))







def amf0_Get_Object_Property(unhandled_Bytes,amf0_Data_Types):
    '''object-property = (UTF-8 value-type) |  (UTF-8-empty object-end-marker)'''
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
    step = amf0_Get_Value_Type(unhandled_Bytes,amf0_Data_Types)
    unhandled_Bytes = step[0]
    Object_Property_Dict['value'] = step[1]
    return((unhandled_Bytes,Object_Property_Dict))


def amf0_Get_Value_Type_Body(unhandled_Bytes,marker_Raw,amf0_Data_Types):
    # number-type = number-marker DOUBLE 
    if(marker_Raw == amf0_Data_Types['name-to-marker']['number-marker']):
        return(amf0_Get_DOUBLE(unhandled_Bytes))
    # boolean-type = boolean-marker U8
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['boolean-marker']):
        return(amf0_Get_U8(unhandled_Bytes))
    # string-type  = string-marker UTF-8
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
    # anonymous-object-type = object-marker *(object-property)
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['object-marker']):
        anonymous_Object_Value_Type_Body = {}
        seq = 1
        step = amf0_Get_Object_Property(unhandled_Bytes)
        unhandled_Bytes = step[0]
        anonymous_Object_Value_Type_Body[seq] = step[1]
        while(not(anonymous_Object_Value_Type_Body[seq]['value']['marker']==b'\x09'})):
            seq = seq + 1
            step = amf0_Get_Object_Property(unhandled_Bytes,amf0_Data_Types)
            unhandled_Bytes = step[0]
            anonymous_Object_Value_Type_Body[seq] = step[1]
        return((unhandled_Bytes,anonymous_Object_Value_Type_Body))
    # This type is not supported and is reserved for future use.
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['movieclip-marker']):
        return((unhandled_Bytes,{}))
    # null-type = null-marker
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['null-marker']):
        return((unhandled_Bytes,b''))
    # undefined-type = undefined-marker
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['undefined-marker']):
        return((unhandled_Bytes,b''))
    # reference-type = reference-marker U16 
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['reference-marker']):
        return(amf0_Get_U16(unhandled_Bytes))
    # ecma-array-type = associative-count *(object-property)
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['ecma-array-marker']):
        ecma_Array_Value_Type_Body = {} 
        step = amf0_Get_U32(unhandled_Bytes)
        unhandled_Bytes = step[0]
        associative_Count_Raw = step[1]
        associative_Count =  amf0_U32_to_INT(associative_Count_Raw)
        for i in range(1,associative_Count+1):
            step = amf0_Get_Object_Property(unhandled_Bytes,amf0_Data_Types)
            unhandled_Bytes = step[0]
            ecma_Array_Value_Type_Body[i] = step[1]
        return((unhandled_Bytes,ecma_Array_Value_Type_Body))
    # Object End Type The object-end-marker is used in a special type that signals the end of a set of object properties in an anonymous object or typed object or associative array. 
    # It is not expected outside of these types. 
    # This marker is always preceded by an empty UTF-8 string and together forms the object end type.  
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['object-end-marker']):
        return((unhandled_Bytes,b''))
    # strict-array-type = array-count *(value-type)
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['strict-array-marker']):
        strict_Array_Value_Type_Body = {} 
        step = amf0_Get_U32(unhandled_Bytes)
        unhandled_Bytes = step[0]
        array_Count_Raw = step[1]
        array_Count =  amf0_U32_to_INT(associative_Count_Raw)
        for i in range(1,associative_Count+1):
            step = amf0_Get_Value_Type(unhandled_Bytes,amf0_Data_Types)
            unhandled_Bytes = step[0]
            strict_Array_Value_Type_Body[i] = step[1]
        return((unhandled_Bytes,strict_Array_Value_Type_Body))
    # date-type = date-marker DOUBLE time-zone
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['date-marker']):
        date_Value_Type_Body = {}
        step = amf0_Get_DOUBLE(unhandled_Bytes)
        unhandled_Bytes = step[0]
        time_Raw = step[1]
        step = amf0_Get_S16(unhandled_Bytes)
        unhandled_Bytes = step[0]
        timezone_Raw = step[1]
        date_Value_Type_Body['time'] = time_Raw
        date_Value_Type_Body['timezone'] = timezone_Raw
        return((unhandled_Bytes,date_Value_Type_Body))
    # long-string-type = long-string-marker UTF-8-long 
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
    # Unsupported Type If a type cannot be serialized a special unsupported marker can be used in place of the type. 
    # Some endpoints may throw an error on encountering this type marker. 
    # No further information is encoded for this type. 
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['unsupported-marker']):
        return((unhandled_Bytes,b''))
    # RecordSet Type This type is not supported and is reserved for future use. 
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['recordset-marker']):
        return((unhandled_Bytes,{}))
    # xml-document-type = xml-document-marker UTF-8-long
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
    # class-name = UTF-8 
    # object-type = object-marker class-name *(object-property)
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['typed-object-marker']):
        typed_Object_Value_Type_Body = {}
        typed_Object_Value_Type_Body['class-name'] = {} 
        step = amf0_Get_UTF8_string_Len_Raw(unhandled_Bytes)
        unhandled_Bytes = step[0]
        class_Name_Len_Raw = step[1]
        step = amf0_Get_UTF8_string_Raw(unhandled_Bytes,class_Name_Len_Raw)
        unhandled_Bytes = step[0]
        class_Name_Raw = step[1]
        typed_Object_Value_Type_Body['class-name']['len'] = class_Name_Len_Raw
        typed_Object_Value_Type_Body['class-name']['string'] = class_Name_Raw
        typed_Object_Value_Type_Body['object-property-dict'] = {}
        seq = 1
        step = amf0_Get_Object_Property(unhandled_Bytes)
        unhandled_Bytes = step[0]
        typed_Object_Value_Type_Body['object-property-dict'][seq] = step[1]
        while(not(typed_Object_Value_Type_Body['object-property-dict'][seq]['value']['marker']==b'\x09'})):
            seq = seq + 1
            step = amf0_Get_Object_Property(unhandled_Bytes,amf0_Data_Types)
            unhandled_Bytes = step[0]
            typed_Object_Value_Type_Body['object-property-dict'][seq] = step[1]
        return((unhandled_Bytes,typed_Object_Value_Type_Body))
    # AVM+ Type Marker With the introduction of AMF 3 in Flash Player 9 to support ActionScript 3.0 and the new AVM+, 
    # the AMF 0 format was extended to allow an AMF 0 encoding context to be switched to AMF 3. 
    # To achieve this, a new type marker was added to AMF 0, the avmplus-object-marker. 
    # The presence of this marker signifies that the following Object is formatted in AMF 3 (See [AMF3]).       
    elif(marker_Raw == amf0_Data_Types['name-to-marker']['avmplus-object-marker']):
        return(amf3_Get_Value_Type(unhandled_Bytes))
    else:
        return(None)
