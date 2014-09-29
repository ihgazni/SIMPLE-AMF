def get_unhandled_Bytes(filename):
    fd = open(filename,'rb')
    return(fd.read())
    fd.close()

filename = '.amf0'
unhandled_Bytes = get_unhandled_Bytes(filename)
amf_packet = {}
######################################################################
#amf-packet = version header-count *(header-type) message- count *(message-type) 
######################################################################
def get_U16(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U16_raw) = (unhandled_Bytes[2:],unhandled_Bytes[0:2])
    return((unhandled_Bytes,U16_raw))

def U16_to_Int(U16_raw):
    return(U16_raw[0] * 16 + U16_raw[1])

######################################################################
{
\x00\x03 ----version       U16  get_U16(unhandled_Bytes)  
}
######################################################################
step = get_U16(unhandled_Bytes)
amf_packet['version'] = step[1]
unhandled_Bytes = step[0]
#########################################################################
{
\x00\x00 ----head-count    U16  get_U16(unhandled_Bytes)   
}
#########################################################################
# header-type = header-name must-understand header-length  value-type 
def get_U8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))

def get_Header_Type(unhandled_Bytes):
    head_Type = {}
    head_Type['header-name'] = {}
    step = get_U16(unhandled_Bytes)
    head_Type['header-name']['len'] = step[1]
    unhandled_Bytes = step[0]
    head_Type['header-name']['name'] = b''
    for i in range(0,head_Type['header-name']['len']):
        step = get_UTF8_char(unhandled_Bytes)
        unhandled_Bytes = step[0]
        head_Type['header-name']['name'] =head_Type['header-name']['name'] + step[1]
    step = get_U8(unhandled_Bytes)
    head_Type['must-understand'] = step[1]
    unhandled_Bytes = step[0]
    step = get_U32(unhandled_Bytes)
    head_Type['header-length'] = step[1]
    unhandled_Bytes = step[0]
    step = get_Value_Type(unhandled_Bytes)
    head_Type['value-type'] = step[1]
    unhandled_Bytes = step[0]
    return((unhandled_Bytes,head_Type))

step = get_U16(unhandled_Bytes)
amf_packet['head-count'] = step[1]
unhandled_Bytes = step[0]
head_Count = U16_to_Int(amf_packet['head-count'])
amf_packet['head-type_Dict'] = {}
for i in range(1,head_Count+1):
    step = get_Header_Type(unhandled_Bytes)
    unhandled_Bytes = step[0]
    amf_packet['head-type_Dict'][i] = step[1]
###############################################################################
{
\x00\x01 ----message-count U16  get_U16(unhandled_Bytes)  
}
step = get_U16(unhandled_Bytes)
amf_packet['message-count'] = step[1]
unhandled_Bytes = step[0]
head_Count = U16_to_Int(amf_packet['message-count'])
amf_packet['message-type_Dict'] = {}
for i in range(1,head_Count+1):
    step = get_Message_Type(unhandled_Bytes)
    unhandled_Bytes = step[0]
    amf_packet['message-type_Dict'][i] = step[1]

###########################################################

def get_UTF8_char(unhandled_Bytes):
    if(unhandled_Bytes[0] < 128):
        if(unhandled_Bytes[0] < 128):
            unhandled_Bytes = unhandled_Bytes[1:]
            handled_Bytes = unhandled_Bytes[0:1]
            return((unhandled_Bytes,handled_Bytes))
        else:
            return(None)
    elif((unhandled_Bytes[0] > 193) & (unhandled_Bytes[0] < 224)):
        if((unhandled_Bytes[0] > 193) & (unhandled_Bytes[0] < 224) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192)):
            unhandled_Bytes = unhandled_Bytes[2:]
            handled_Bytes = unhandled_Bytes[0:2]
            return((unhandled_Bytes,handled_Bytes))
        else:
            return(None)
    elif((unhandled_Bytes[0] > 223) & (unhandled_Bytes[0] < 240)):
        if((unhandled_Bytes[0] == 224) & (unhandled_Bytes[1] > 159) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            unhandled_Bytes = unhandled_Bytes[3:]
            handled_Bytes = unhandled_Bytes[0:3]
            return((unhandled_Bytes,handled_Bytes))
        elif((unhandled_Bytes[0] > 224) &(unhandled_Bytes[0] < 237) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            unhandled_Bytes = unhandled_Bytes[3:]
            handled_Bytes = unhandled_Bytes[0:3]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] == 237) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 160) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            unhandled_Bytes = unhandled_Bytes[3:]
            handled_Bytes = unhandled_Bytes[0:3]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] > 237) &(unhandled_Bytes[0] < 240) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192)):
            unhandled_Bytes = unhandled_Bytes[3:]
            handled_Bytes = unhandled_Bytes[0:3]
            return(unhandled_Bytes,handled_Bytes)
        else:
            return(None)
    elif(unhandled_Bytes[0] > 240):
        if((unhandled_Bytes[0] == 240) & (unhandled_Bytes[1] > 143) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192) & (unhandled_Bytes[3] > 127) & (unhandled_Bytes[3] < 192)):
            unhandled_Bytes = unhandled_Bytes[4:]
            handled_Bytes = unhandled_Bytes[0:4]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] > 240) &(unhandled_Bytes[0] < 244) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 192) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192) & (unhandled_Bytes[3] > 127) & (unhandled_Bytes[3] < 192)):
            unhandled_Bytes = unhandled_Bytes[4:]
            handled_Bytes = unhandled_Bytes[0:4]
            return(unhandled_Bytes,handled_Bytes)
        elif((unhandled_Bytes[0] == 244) & (unhandled_Bytes[1] > 127) & (unhandled_Bytes[1] < 144) & (unhandled_Bytes[2] > 127) & (unhandled_Bytes[2] < 192) & (unhandled_Bytes[3] > 127) & (unhandled_Bytes[3] < 192) ):
            unhandled_Bytes = unhandled_Bytes[4:]
            handled_Bytes = unhandled_Bytes[0:4]
            return(unhandled_Bytes,handled_Bytes)
        else:
            return(None)
    else:
        return(None)
 
def get_UTF8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = get_U16(unhandled_Bytes)
    handled_Bytes = handled_Bytes + count_raw
    count = U16_to_Int(count_Raw)
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))

def UTF8_to_String(UTF8_raw):
    return(UTF8_raw[1][2:].decode('utf-8'))

###################################################################
#message-type = target-uri response-uri message-length value-type 
###########################################################

def get_Message_Type(unhandled_Bytes):
    message_Type = {}
    message_Type['target-uri'] = {}
    step = get_U16(unhandled_Bytes)
    message_Type['target-uri']['len'] = step[1]
    unhandled_Bytes = step[0]
    message_Type['target-uri']['uri'] = b''
    for i in range(0,message_Type['target-uri']['len']):
        step = get_UTF8_char(unhandled_Bytes)
        unhandled_Bytes = step[0]
        message_Type['target-uri']['uri'] = message_Type['target-uri']['uri'] + step[1]
    message_Type['response-uri'] = {}
    step = get_U16(unhandled_Bytes)
    message_Type['response-uri']['len'] = step[1]
    unhandled_Bytes = step[0]
    message_Type['response-uri']['uri'] = b''
    for i in range(0,message_Type['response-uri']['len']):
        step = get_UTF8_char(unhandled_Bytes)
        unhandled_Bytes = step[0]
        message_Type['response-uri']['uri'] = message_Type['response-uri']['uri'] + step[1]
    step = get_U32(unhandled_Bytes)
    message_Type['message-length'] = step[1]
    unhandled_Bytes = step[0]
    step = get_Value_Type(unhandled_Bytes)
    message_Type['value-type'] = step[1]
    unhandled_Bytes = step[0]
    return((unhandled_Bytes,message_Type))


{
----target-uri    UTF-8 = U16 * (UTF8-char)          
\x00\x04   U16  
null       * (UTF8-char)
}

######################################################################################
{
----response-uri     UTF-8 = U16 * (UTF8-char)       
\x00\x02 ----U16
/1       * (UTF8-char)
}

#################################################################
def get_U32(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U32_Raw) = (unhandled_Bytes[4:],unhandled_Bytes[0:4])
    return((unhandled_Bytes,U32_Raw))

def U32_to_Int(U32_Raw):
    return(U16_raw[0] *16*16*16 + U16_raw[1]*16*16 + U16_raw[2]*16 + U16_raw[3])

#################################################################
---------------message-length  U32 get_U32(unhandled_Bytes)
{              
\x00\x00\x00\xe0
}
step = get_U32(unhandled_Bytes)
amf_packet['message-length'] = step[1]
unhandled_Bytes = step[0]

###################################################################

def get_DOUBLE(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,DOUBLE_raw) = (unhandled_Bytes[8:],unhandled_Bytes[0:8])
    return((unhandled_Bytes,DOUBLE_raw))

def DOUBLE_to_Float(DOUBLE_raw):
    return(struct.unpack('!d',DOUBLE_raw)[0])

###################################################################

def get_U29(unhandled_Bytes):
    U29_raw = b''
    i = 0 
    while(i<4):
        if(unhandled_Bytes[i]<128):
            U29_raw = U29_raw + unhandled_Bytes[i:]
            break
        else:
            U29_raw = U29_raw + unhandled_Bytes[i:i+1]
        i = i + 1
    return((unhandled_Bytes[(i+1):],U29_raw))


def U29_to_INT(U29_raw):
    len = U29_raw.__len__()
    if(len == 1):
        return(int(U29_raw,16))
    elif(len == 2):
        seven_1 = (U29_raw[0] - 128 )* 2**7
        seven_2 = U29_raw[1]
        return(seven_1 + seven_2)
    elif(len == 3):
        seven_1 = ( U29_raw[0] - 128 ) * 2**14
        seven_2 = ( U29_raw[1] - 128 ) * 2**7
        seven_3 = U29_raw[2]
        return(seven_1 + seven_2 + seven_3)
    elif(len == 4):
        seven_1 = (U29_raw[0] - 128 ) * (2**22)
        seven_2 = (U29_raw[1] - 128 ) * (2**15)
        seven_3 = (U29_raw[2] - 128 ) * (2**8)
        seven_4 = U29_raw[3]
        return(seven_1 + seven_2 + seven_3 + seven_4)
    else:
        return(None)


def INT_to_U29(int):
    bin_Str = bin(int).lstrip('0b')
    len = bin_Str.__len__()
    if(len < 8):
        new_Bin_Str = '{0:0>8}'.format(bin_Str[0:7])
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    elif(len < 15):
        seven_1 = '{0:0>8}'.format(bin_Str[0:7])
        seven_2 = '1{0:0>7}'.format(bin_Str[7:14])
        new_Bin_Str = seven_1 + seven_2
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    elif(len < 22):
        seven_1 = '{0:0>8}'.format(bin_Str[0:7])
        seven_2 = '1{0:0>7}'.format(bin_Str[7:14])
        seven_3 = '1{0:0>7}'.format(bin_Str[14:21])
        new_Bin_Str = seven_1 + seven_2 + seven_3
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    elif(len < 30):
        seven_1 = '{0:0>8}'.format(bin_Str[0:7])
        seven_2 = '1{0:0>7}'.format(bin_Str[7:14])
        seven_3 = '1{0:0>7}'.format(bin_Str[14:21])
        seven_4 = '{0:0>8}'.format(bin_Str[21:])
        new_Bin_Str = seven_1 + seven_2 + seven_3 + seven_4
        new_Bin_Str = '{0:0>2}'.format(hex(int(new_Bin_Str,2)).lstrip('0x'))
        return(new_Bin_Str.encode())
    else:
        return(None)




# xml-doc-type = xml-doc-marker (U29O-ref | (U29X-value  *(UTF8-char))) 
# U29O-ref | (U29X-value  *(UTF8-char))
# U29O-ref = U29 
; The first (low) bit is a flag  
; (representing whether an instance  
; follows) with value 0 to imply that  
; this is not an instance but a  
; reference. The remaining 1 to 28  
; significant bits are used to encode an 
; object reference index (an integer). 
# U29X-value   = U29 
def get_Xml_Doc(unhandled_Bytes):
    Xml_Doc_Dict = {}
    step = get_U29(unhandled_Bytes)
    U29S_raw = step[1]
    unhandled_Bytes = step[0]
    interg = U29_to_INT(U29_raw)
    is_Ref = interg & 1
    if(is_Ref == 0):
        Xml_Doc_Dict['ref'] = interg
    else:
        Xml_Doc_Dict['len'] = interg
        Xml_Doc_Dict['body'] = b''
        for i in range(1,interg+1):
            step = get_UTF8_char(unhandled_Bytes)
            unhandled_Bytes = step[0]
            Xml_Doc_Dict['body'] = Xml_Doc_Dict['body'] + step[1]
    return((unhandled_Bytes,Xml_Doc_Dict))


# string-type = string-marker UTF-8-vr 
UTF-8-vr = U29S-ref | (U29S-value *(UTF8-char))
U29S-ref = U29 
; The first (low) bit is a flag with  
; value 0. The remaining 1 to 28  
; significant bits are used to encode a  
; string reference table index (an integer). 
U29S-value = U29 
UTF-8-empty = 0x01 

def get_String(unhandled_Bytes):
    string_Dict = {}
    step = get_U29(unhandled_Bytes)
    U29S_raw = step[1]
    unhandled_Bytes = step[0]
    interg = U29_to_INT(U29_raw)
    is_Ref = interg & 1
    if(is_Ref == 0):
        string_Dict['ref'] = interg
    else:
        string_Dict['len'] = interg
        string_Dict['body'] = b''
        for i in range(1,interg+1):
            step = get_UTF8_char(unhandled_Bytes)
            unhandled_Bytes = step[0]
            string_Dict['body'] = string_Dict['body'] + step[1]
    return((unhandled_Bytes,string_Dict))



date-type = date-marker (U29O-ref | (U29D-value date-time))
U29D-value = U29 
date-time = DOUBLE

def get_Date(unhandled_Bytes):
    Date_Dict = {}
    step = get_U29(unhandled_Bytes)
    U29S_raw = step[1]
    unhandled_Bytes = step[0]
    interg = U29_to_INT(U29_raw)
    is_Ref = interg & 1
    if(is_Ref == 0):
        Date_Dict['ref'] = interg
    else:
        Date_Dict['reserved'] = interg
        step = get_DOUBLE(unhandled_Bytes)
        unhandled_Bytes = step[0]
        Date_Dict['date-time'] = step[1]
    return((unhandled_Bytes,Date_Dict))

def get_Date_Time(DOUBLE_raw)
    since_epoch = DOUBLE_to_Float(DOUBLE_raw)
    date='Wed, 11 Apr 2012 09:37:05 +0800'
    dd=datetime.datetime.strptime(date,'%a, %d %b %Y %H:%M:%S %z')
    current_DD = dd.fromtimestamp(since_epoch)
    return(current_DD.strftime("%Y-%m-%d %H:%M:%S:%f"))


##########################################

U29A-value = U29
assoc-value = UTF-8-vr value-type 
U29A-value  (UTF-8-empty | *(assoc-value) UTF-8-empty)  *(value-type)
array-type = array-marker U29O-ref
array-type = array-marker U29A-value  (UTF-8-empty | *(assoc-value) UTF-8-empty)  *(value-type)) 
(UTF-8-empty | *(assoc-value) UTF-8-empty)  *(value-type)


def get_Array(unhandled_Bytes):
    array_Dict = {}
    step = get_U29(unhandled_Bytes)
    U29S_raw = step[1]
    unhandled_Bytes = step[0]
    interg = U29_to_INT(U29_raw)
    is_Ref = interg & 1
    if(is_Ref == 0):
        array_Dict['ref'] = interg
    else:
        array_Dict['count-of-dense'] = interg
        array_Dict['dense'] = {}
        empty_Name_Sign = unhandled_Bytes[0]
        assoc_index = 1
        while(not(empty_Name_Sign == b'\x01')):
            step = get_Assoc_Value(unhandled_Bytes)
            unhandled_Bytes = step[0]
            array_Dict['assoc-value'] = {}
            array_Dict['assoc-value'][assoc_index] = step[1]
            assoc_index = assoc_index + 1
            empty_Name_Sign = unhandled_Bytes[0]
        array_Dict['assoc-value']['end'] = empty_Name_Sign
        for i in range(1,array_Dict['count-of-dense']+1):
            step = get_Value_Type(unhandled_Bytes)
            unhandled_Bytes = step[0]
            array_Dict['dense'][i] = step[1]
    return((unhandled_Bytes,array_Dict))



def get_Assoc_Value(unhandled_Bytes):
    



##########################################
---------------AMF3
value-type = undefined-marker | null-marker | false-marker | true-marker | integer-type | double-type |  string-type | xml-doc-type | date-type |  array-type | object-type |  xml-type | byte-array- type | vector-int-type | vector-uint-type | vector-double-type | vector-object-type | dictionary-type 
def get_Value_Type_AMF3(unhandled_Bytes):
    value_Type = {}
    (unhandled_Bytes,value_Type['marker']) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    if(value_Type['marker'] == 0):
        value_Type['marker-string'] = 'undefined'
        value_Type['body'] = None
    elif(value_Type['marker'] == 1):
        value_Type['marker-string'] = 'null'
        value_Type['body'] = None
    elif(value_Type['marker'] == 2):
        value_Type['marker-string'] = 'false'
        value_Type['body'] = None
    elif(value_Type['marker'] == 3):
        value_Type['marker-string'] = 'true'
        value_Type['body'] = None
    elif(value_Type['marker'] == 4):
        value_Type['marker-string'] = 'interg'
        step = get_U29(unhandled_Bytes)
        value_Type['body'] = step[1]
        unhandled_Bytes = step[0]
    elif(value_Type['marker'] == 5):
        value_Type['marker-string'] = 'double'
        step = get_DOUBLE(unhandled_Bytes)
        value_Type['body'] = step[1]
        unhandled_Bytes = step[0]
    elif(value_Type['marker'] == 6):
        value_Type['marker-string'] = 'string'
        step = get_String(unhandled_Bytes)
        value_Type['body'] = step[1]
        unhandled_Bytes = step[0]
    elif(value_Type['marker'] == 7):
        value_Type['marker-string'] = 'xml-doc'
        step =  get_Xml_Doc(unhandled_Bytes)
        value_Type['body'] = step[1]
        unhandled_Bytes = step[0]
    elif(value_Type['marker'] == 8):
        value_Type['marker-string'] = 'date'
        step =  get_Date(unhandled_Bytes)
        value_Type['body'] = step[1]
        unhandled_Bytes = step[0]
    elif(value_Type['marker'] == 9):
        value_Type['marker-string'] = 'array'##
        step =  get_Array(unhandled_Bytes)
        value_Type['body'] = step[1]
        unhandled_Bytes = step[0]
    elif(value_Type['marker'] == 10):
    elif(value_Type['marker'] == 11):
    elif(value_Type['marker'] == 12):
    elif(value_Type['marker'] == 13):
    elif(value_Type['marker'] == 14):
    elif(value_Type['marker'] == 15):
    elif(value_Type['marker'] == 16):
    elif(value_Type['marker'] == 17):
    else:
        return(None)
---------------AMF0 
value-type   = number-type | boolean-type | string-type | object-type | null-marker | undefined-marker | reference-type | ecma-array-type |  strict-array-type | date-type | long-string-type | xml-document-type | typed-object-type | avmplus-object-type
def get_Value_Type_AMF0(unhandled_Bytes):
    value_Type = {}
    (unhandled_Bytes,value_Type['marker']) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    if(value_Type['marker'] == 0):
        value_Type['body'] = 
    elif(value_Type['marker'] == 1):
    elif(value_Type['marker'] == 2):
    elif(value_Type['marker'] == 3):
    elif(value_Type['marker'] == 4):
    elif(value_Type['marker'] == 5):
    elif(value_Type['marker'] == 6):
    elif(value_Type['marker'] == 7):
    elif(value_Type['marker'] == 8):
    elif(value_Type['marker'] == 9):
    elif(value_Type['marker'] == 10):
    elif(value_Type['marker'] == 11):
    elif(value_Type['marker'] == 12):
    elif(value_Type['marker'] == 13):
    elif(value_Type['marker'] == 14):
    elif(value_Type['marker'] == 15):
    elif(value_Type['marker'] == 16):
    elif(value_Type['marker'] == 17):
    else:
        return(None)
###################################################################
{
\n #  -----------------------------------AMF0 value-type   strict-array-type 
}
{
\x00\x00\x00\x01 # array-count U32 1
}
{
\x11  #value-type : avmplus-object-marker   AMF3 embeded in AMF0 
}
{
\n # object-marker AMF3 object-type
}
(U29O-ref | (U29O-traits-ext class-name *(U8)) | U29O-traits-ref | (U29O- traits class-name *(UTF-8-vr))) *(value-type) *(dynamic-member)
{
\x81\x13 # ------------U29O-traits 1-0000001 0-001-0011  0000001001 = 9  member = 9
}
-------------------------------class-name UTF-8-vr  --- UTF-8-vr = U29S-ref | (U29S-value *(UTF8-char)) 
-------------------------------(U29S-value *(UTF8-char)) 
{
M #      U29S-value '0-100110-1' 100110
}
# *(UTF8-char) 
{ 
flex.messaging.messages.CommandMessage
}
------------(U29S-value *(UTF8-char))
{
\x13
operation
}
------------(U29S-value *(UTF8-char))
\x1b
correlationId
------------(U29S-value *(UTF8-char))
\x13
messageId
------------(U29S-value *(UTF8-char))
\x11
clientId
------------(U29S-value *(UTF8-char))
\x15
timeToLive
------------(U29S-value *(UTF8-char))
\x13
timestamp
------------(U29S-value *(UTF8-char))
\x0f
headers
------------(U29S-value *(UTF8-char))
\x17
destination
------------(U29S-value *(UTF8-char))
\t
body
{=====================================================1
---------------value-type
\x04 -------- interg
\x05 -----------U29 5
}
{=====================================================2
---------------value-type
\x06 -------- string
\x01 ----------- UTF-8-vr  U29S-value  0-000000-1 
}
{=====================================================3
---------------value-type
\x06-------- string
I
50A43A42-6AB3-FA5B-0601-AA658F60C1F5
}
{=====================================================4
---------------value-type
\x01---------NULL
}
{=====================================================5
---------------value-type
\x04---------interg
\x00  ---------0
}
{=====================================================6
---------------value-type
\x04---------interg
\x00
}
{=====================================================7
--------------------------------value-type
\n ---------------object-marker
(U29O-ref | (U29O-traits-ext class-name *(U8)) | U29O-traits-ref | (U29O- traits class-name *(UTF-8-vr))) *(value-type) *(dynamic-member)
    \x0b ------  0-000-1011 U29O-traits     dynamic  sealed member  section(dynamic-member 之前的value-type是000 =0 个)
    \x01 -------class-name UTF-8-vr  classname 空串的ClassName就是指这个object的Class就是普通的Object类
    -------------------------------------------dynamic-member 
    ------------name UTF-8-vr
    \t 0-000100-1  U29S-value
    DSId  ----------*(UTF8-char)
    -------------value-type
    \x06 ------------string
    \x07  0-000011-1 U29S-value
    nil ------------*(UTF8-char)
    -------------------------------------------dynamic-member 
    ------------name UTF-8-vr
    %
    DSMessagingVersion
    ------------value-type
    \x04 --------- interg
    \x01 ----------1
    ------------------------------------------dynamic-member END UTF-8-empty = 0x01
    \x01  0-000000-1 U29S-value
}

{=====================================================8
\x06 ----------string
\x01 ----------empty
} 
{ =====================================================9
\n  ---------------object-marker
    \x05 ------0-00001-01 U29O-traits-ref    sent-by-reference    ref index = 1
}
\x01 ----- ?????
