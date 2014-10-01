
import sys
import os
import struct
import re
import datetime

#################################--common parts--################################################

# amf3_U8 :
# An unsigned byte, 8-bits of data, an octet 
def amf3_Get_U8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))

def amf3_U8_to_INT(U8_raw):
    return(U8_raw[0])

def amf3_INT_to_U8(INT):
    high = '{0:0>2}'.format(hex(INT).lstrip('0x'))[0:2]
    high = int(high,16)
    return(chr(high).encode('latin-1'))


# amf3_U16 : 
# An unsigned 16-bit integer in big endian (network) byte order 
def amf3_Get_U16(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U16_raw) = (unhandled_Bytes[2:],unhandled_Bytes[0:2])
    return((unhandled_Bytes,U16_raw))

def amf3_U16_to_INT(U16_raw):
    return(struct.unpack('!H',S16_raw)[0])

def amf3_INT_to_U16(INT):
    return(struct.pack('!H',255))

# amf3_U32
# An unsigned 32-bit integer in big endian (network) byte order 

def amf3_Get_U32(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U32_raw) = (unhandled_Bytes[4:],unhandled_Bytes[0:4])
    return((unhandled_Bytes,U32_raw))

def amf3_U32_to_INT(U32_raw):
    return(struct.unpack('!I',U32_raw)[0])

def amf3_INT_to_U32(INT):
    return(struct.pack('!I',INT))

# amf3_DOUBLE :
# 8 byte IEEE-754 double precision floating point value in network byte order (sign bit in low memory). 

def amf3_Get_DOUBLE(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,DOUBLE_raw) = (unhandled_Bytes[8:],unhandled_Bytes[0:8])
    return((unhandled_Bytes,DOUBLE_raw))

def amf3_DOUBLE_to_Float(DOUBLE_raw):
    return(struct.unpack('!d',DOUBLE_raw)[0])
    
def amf3_Get_Date_Time(DOUBLE_raw)
    since_epoch = amf3_DOUBLE_to_Float(DOUBLE_raw)
    date='Wed, 11 Apr 2012 09:37:05 +0800'
    dd=datetime.datetime.strptime(date,'%a, %d %b %Y %H:%M:%S %z')
    current_DD = dd.fromtimestamp(since_epoch)
    return(current_DD.strftime("%Y-%m-%d %H:%M:%S:%f"))

# MB = A megabyte or 1048576 bytes.
amf3_MB = 1048576

#
# In ABNF syntax, [RFC3629] describes UTF-8 as follows:   
# UTF8-char = UTF8-1 | UTF8-2 | UTF8-3 | UTF8-4 
# UTF8-1 = %x00-7F 
# UTF8-2 = %xC2-DF UTF8-tail 
# UTF8-3 = %xE0 %xA0-BF UTF8-tail | %xE1-EC 2(UTF8-tail) | \
         # %xED %x80-9F UTF8-tail | %xEE-EF 2(UTF8-tail) 
# UTF8-4 = %xF0 %x90-BF 2(UTF8-tail) | %xF1-F3 3(UTF8-tail) | \
         # %xF4 %x80-8F 2(UTF8-tail) 
# UTF8-tail = %x80-BF 
def amf3_Get_UTF8_char(unhandled_Bytes):
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

# UTF-8 = U16 *(UTF8-char)  
# A 16-bit byte-length header implies a theoretical maximum of 65,535 bytes \
# to encode a string in UTF-8 (essentially 64KB).     

def amf3_Get_UTF8_string_Len_Raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf3_Get_U16(unhandled_Bytes)
    return((unhandled_Bytes,count_Raw))

def amf3_UTF8_string_Len(UTF8_string_Len_Raw):
    count = amf3_U16_to_INT(UTF8_string_Len_Raw)
    return(count)

def amf3_Get_UTF8_string_Raw(unhandled_Bytes,UTF8_string_Len_Raw):
    count = amf3_U16_to_INT(UTF8_string_Len_Raw)
    handled_Bytes = b''
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf3_Get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))

def amf3_UTF8_String(UTF8_string_Raw):
    return(UTF8_string_Raw.decode('utf-8'))

def amf3_Get_UTF8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf3_Get_U16(unhandled_Bytes)
    handled_Bytes = handled_Bytes + count_raw
    count = amf3_U16_to_INT(count_Raw)
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf3_Get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))



#################################--common parts--################################################


#################################--amf3_only--################################################
# In ABNF syntax, the variable length unsigned 29-bit integer type is described as follows:
# U29 = U29-1 | U29-2 | U29-3 | U29-4
# U29-1 = %x00-7F
# U29-2 = %x80-FF %x00-7F
# U29-3 = %x80-FF %x80-FF %x00-7F
# U29-4 = %x80-FF %x80-FF %x80-FF %x00-FF

def amf3_Get_U29(unhandled_Bytes):
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


def amf3_U29_to_INT(U29_raw):
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


def amf3_INT_to_U29(int):
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


# U29S-ref = U29 ; 
# The first (low) bit is a flag with 
# value 0. The remaining 1 to 28 
# significant bits are used to encode a 
# string reference table index (an 
# integer).

def amf3_Is_U29S_ref(U29):
    int_Little_Endian = U29[-1]
    if(int_Little_Endian % 2 == 0):
        return(amf3_U29_to_INT(U29) // 2)
    else:
        return(None)


# U29S-value = U29 ; The first (low) bit is a flag with 
# value 1. The remaining 1 to 28 
# significant bits are used to encode the 
# byte-length of the UTF-8 encoded 
# representation of the string

def amf3_Is_U29S_value(U29):
    int_Little_Endian = U29[-1]
    if(int_Little_Endian % 2 == 1):
        return((amf3_U29_to_INT(U29)-1) // 2)
    else:
        return(None)

# UTF-8-empty = 0x01  
# The UTF-8-vr empty string which is 
# never sent by reference.

amf3_UTF_8_empty = b'\x01'

# UTF-8-vr = U29S-ref | (U29S-value *(UTF8-char))

def amf3_Get_UTF8_vr(unhandled_Bytes):
    vr = {}
    step = amf3_Get_U29(unhandled_Bytes)
    unhandled_Bytes = step[0]
    U29_raw = step[1]
    s_Ref = amf3_Is_U29S_ref(U29_raw)
    s_Value_Len = amf3_Is_U29S_value(U29_raw)
    vr['ref'] = s_Ref
    vr['value'] = {}
    vr['value']['len'] = s_Value_Len
    string = b''
    for i in range(0,s_Value_Len):
        step = amf3_Get_UTF8_char(unhandled_Bytes)
        unhandled_Bytes = step[0]
        string = string + step[1]
    vr['value']['string'] = string
    return((unhandled_Bytes,vr))

##-----------------------------------------------------------------##
# AMF 3 Data Types 
##-----------------------------------------------------------------##

amf3_Data_Types = {
    'name-to-marker':{
        'undefined-marker':b'\x00',
        'null-marker':b'\x01',
        'false-marker':b'\x02',
        'true-marker':b'\x03',  
        'integer-marker':b'\x04',  
        'double-marker':b'\x05',
        'string-marker':b'\x06',
        'xml-doc-marker':b'\x07',
        'date-marker':b'\x08',
        'array-marker':b'\x09',
        'object-marker': b'\x0A',
        'xml-marker':b'\x0B',
        'byte-array-marker':b'\x0C',
        'vector-int-marker' : b'\x0D',
        'vector-uint-marker' : b'\x0E',
        'vector-double-marker' : b'\x0F',
        'vector-object-marker' : b'\x10',
        'dictionary-marker' : b'\x11'
    },
    'marker-to-name': {
        b'\x00':  'undefined-marker',
        b'\x01':  'null-marker',
        b'\x02':  'false-marker',
        b'\x03':  'true-marker',
        b'\x04':  'integer-marker',
        b'\x05':  'double-marker',
        b'\x06':  'string-marker',
        b'\x07':  'xml-doc-marker',
        b'\x08':  'date-marker',
        b'\x09':  'array-marker',
        b'\x0A':  'object-marker',
        b'\x0B':  'xml-marker',
        b'\x0C':  'byte-array-marker',
        b'\x0D':  'vector-int-marker',
        b'\x0E':  'vector-uint-marker',
        b'\x0F':  'vector-double-marker',
        b'\x10':  'vector-object-marker',
        b'\x11':  'dictionary-marker'
    }
}


#################################--amf3_only--################################################






