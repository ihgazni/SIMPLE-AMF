import sys
import os
import struct
import re

# amf0_U8 :
# An unsigned byte, 8-bits of data, an octet 
def amf0_Get_U8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U8_raw) = (unhandled_Bytes[1:],unhandled_Bytes[0:1])
    return((unhandled_Bytes,U8_raw))

def amf0_U8_to_INT(U8_raw):
    return(U8_raw[0])

def amf0_INT_to_U8(INT):
    high = '{0:0>2}'.format(hex(INT).lstrip('0x'))[0:2]
    high = int(high,16)
    return(chr(high).encode('latin-1'))


# amf0_U16 : 
# An unsigned 16-bit integer in big endian (network) byte order 
def amf0_Get_U16(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U16_raw) = (unhandled_Bytes[2:],unhandled_Bytes[0:2])
    return((unhandled_Bytes,U16_raw))

def amf0_U16_to_INT(U16_raw):
    return(struct.unpack('!H',S16_raw)[0])

def amf0_INT_to_U16(INT):
    return(struct.pack('!H',255))

# amf0_U32
# An unsigned 32-bit integer in big endian (network) byte order 

def amf0_Get_U32(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,U32_raw) = (unhandled_Bytes[4:],unhandled_Bytes[0:4])
    return((unhandled_Bytes,U32_raw))

def amf0_U32_to_INT(U32_raw):
    return(struct.unpack('!I',U32_raw)[0])

def amf0_INT_to_U32(INT):
    return(struct.pack('!I',INT))


# amf0_S16 :
# An signed 16-bit integer in big endian (network) byte order 

def amf0_Get_S16(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,S16_raw) = (unhandled_Bytes[2:],unhandled_Bytes[0:2])
    return((unhandled_Bytes,S16_raw))

def amf0_S16_to_INT(S16_raw):
    return(struct.unpack('!h',S16_raw)[0])

def amf0_INT_to_S16(INT):
    return(struct.pack('!h',255))

# amf0_DOUBLE :
# 8 byte IEEE-754 double precision floating point value in network byte order (sign bit in low memory). 

def amf0_Get_DOUBLE(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,DOUBLE_raw) = (unhandled_Bytes[8:],unhandled_Bytes[0:8])
    return((unhandled_Bytes,DOUBLE_raw))

def amf0_DOUBLE_to_Float(DOUBLE_raw):
    return(struct.unpack('!d',DOUBLE_raw)[0])
    
def amf0_Get_Date_Time(DOUBLE_raw)
    since_epoch = amf0_DOUBLE_to_Float(DOUBLE_raw)
    date='Wed, 11 Apr 2012 09:37:05 +0800'
    dd=datetime.datetime.strptime(date,'%a, %d %b %Y %H:%M:%S %z')
    current_DD = dd.fromtimestamp(since_epoch)
    return(current_DD.strftime("%Y-%m-%d %H:%M:%S:%f"))

# amf0_KB A kilobyte or 1024 bytes
amf0_KB = 1024
# amf0_GB A Gigabyte or 1,073,741,824 bytes, 1024 * 1024 * 1024
amf0_GB = 1073741824

# In ABNF syntax, [RFC3629] describes UTF-8 as follows:   
# UTF8-char = UTF8-1 | UTF8-2 | UTF8-3 | UTF8-4 
# UTF8-1 = %x00-7F 
# UTF8-2 = %xC2-DF UTF8-tail 
# UTF8-3 = %xE0 %xA0-BF UTF8-tail | %xE1-EC 2(UTF8-tail) | \
         # %xED %x80-9F UTF8-tail | %xEE-EF 2(UTF8-tail) 
# UTF8-4 = %xF0 %x90-BF 2(UTF8-tail) | %xF1-F3 3(UTF8-tail) | \
         # %xF4 %x80-8F 2(UTF8-tail) 
# UTF8-tail = %x80-BF 
def amf0_Get_UTF8_char(unhandled_Bytes):
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

def amf0_Get_UTF8_string_Len_Raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf0_Get_U16(unhandled_Bytes)
    return((unhandled_Bytes,count_Raw))

def amf0_UTF8_string_Len(UTF8_string_Len_Raw):
    count = amf0_U16_to_INT(UTF8_string_Len_Raw)
    return(count)

def amf0_Get_UTF8_string_Raw(unhandled_Bytes,UTF8_string_Len_Raw):
    count = amf0_U16_to_INT(UTF8_string_Len_Raw)
    handled_Bytes = b''
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf0_Get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))

def amf0_UTF8_String(UTF8_string_Raw):
    return(UTF8_string_Raw.decode('utf-8'))

def amf0_Get_UTF8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf0_Get_U16(unhandled_Bytes)
    handled_Bytes = handled_Bytes + count_raw
    count = amf0_U16_to_INT(count_Raw)
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf0_Get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))


# For longer strings, a 32-bit byte-length may be required. This document will \
# refer to this type as:  
# UTF-8-long = U32 *(UTF8-char)      
# A 32-bit byte-length header implies a theoretical maximum of 4,294,967,295 bytes \
# to encode a string in UTF-8 (essentially 4GB). 

def amf0_Get_LUTF8_string_Len_Raw(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf0_Get_U32(unhandled_Bytes)
    return((unhandled_Bytes,count_Raw))

def amf0_LUTF8_string_Len(UTF8_string_Len_Raw):
    count = amf0_U32_to_INT(UTF8_string_Len_Raw)
    return(count)

def amf0_Get_LUTF8_string_Raw(unhandled_Bytes,UTF8_string_Len_Raw):
    count = amf0_U32_to_INT(UTF8_string_Len_Raw)
    handled_Bytes = b''
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf0_Get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))

def amf0_LUTF8_String(UTF8_string_Raw):
    return(UTF8_string_Raw.decode('utf-8'))

def amf0_Get_LUTF8(unhandled_Bytes):
    handled_Bytes = b''
    (unhandled_Bytes,count_Raw) = amf0_Get_U32(unhandled_Bytes)
    handled_Bytes = handled_Bytes + count_raw
    count = amf0_U32_to_INT(count_Raw)
    for i in range(1,count+1):
        (unhandled_Bytes,UTF8_Char_Raw) = amf0_Get_UTF8_char(unhandled_Bytes)
        handled_Bytes = handled_Bytes + UTF8_Char_Raw
    return((unhandled_Bytes,handled_Bytes))


# UTF-8-empty = U16 ; 
# byte-length reported as zero with  ; 
# no UTF8-char content, i.e. 0x0000 
amf0_UTF-8-empty = b'\x00\x00'

##-----------------------------------------------------------------##

##-----------------------------------------------------------------##
# AMF 0 Data Types 
##-----------------------------------------------------------------##

amf0_Data_Types = {
    'name-to-marker':{
        'number-marker':b'\x00',
        'boolean-marker':b'\x01',
        'string-marker':b'\x02',
        'object-marker':b'\x03',  
        'movieclip-marker':b'\x04',  
        'null-marker':b'\x05',
        'undefined-marker':b'\x06',
        'reference-marker':b'\x07',
        'ecma-array-marker':b'\x08',
        'object-end-marker':b'\x09',
        'strict-array-marker': b'\x0A',
        'date-marker':b'\x0B',
        'long-string-marker':b'\x0C',
        'unsupported-marker' : b'\x0D',
        'recordset-marker' : b'\x0E',
        'xml-document-marker' : b'\x0F',
        'typed-object-marker' : b'\x10',
        'avmplus-object-marker' : b'\x11'
    },
    'marker-to-name': {
        b'\x00':  'number-marker',
        b'\x01':  'boolean-marker',
        b'\x02':  'string-marker',
        b'\x03':  'object-marker',
        b'\x04':  'movieclip-marker',
        b'\x05':  'null-marker',
        b'\x06':  'undefined-marker',
        b'\x07':  'reference-marker',
        b'\x08':  'ecma-array-marker',
        b'\x09':  'object-end-marker',
        b'\x0A':  'strict-array-marker',
        b'\x0B':  'date-marker',
        b'\x0C':  'long-string-marker',
        b'\x0D':  'unsupported-marker',
        b'\x0E':  'recordset-marker',
        b'\x0F':  'xml-document-marker',
        b'\x10':  'typed-object-marker',
        b'\x11':  'avmplus-object-marker'
    }
}

# -------------------------------------------------------------------------- #

