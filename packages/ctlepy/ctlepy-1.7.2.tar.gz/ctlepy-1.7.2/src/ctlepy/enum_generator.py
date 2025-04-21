# ctle Copyright (c) 2023 Ulrik Lindahl
# Licensed under the MIT license https://github.com/Cooolrik/ctle/blob/main/LICENSE

from enum import Enum
from .formatted_output import formatted_output

class enum_value:
    def __init__( self, name:str, value:str, desc:str ) -> None:
        self.name = name
        self.value = value
        self.desc = ' '.join(desc.split()) # removes all consecutive whitespace and replaces with just a single space

class enum_type:
    def __init__( self, name:str, types:str, desc:str, values:list[enum_value] ) -> None:
        self.name = name
        self.types = types
        self.desc = desc
        self.values = values
    
# name_padding - minimum number of chars in name, (will be right-padded with spaces if less)
# value_padding - minimum number of chars in value, (will be right-padded with spaces if less)
# pad_to_max - automatically increase paddings based on names and values in the enum
def generate_enum_declaration( enm:enum_type, out:formatted_output, name_padding:int = 0, value_padding:int = 0, pad_to_max:bool = True  ) -> None:
    if pad_to_max:
        for val in enm.values:
            name_padding = max( name_padding, len(val.name) )
            value_padding = max( value_padding, len(val.value) )

    if enm.desc != None and len(enm.desc) > 0:
        out.comment_ln(enm.desc)

    s = 'enum class ' + enm.name
    if enm.types != None and len(enm.types) > 0:
        s += ' : ' + enm.types
    out.ln(s)

    with out.blk( add_semicolon=True ):
        for val in enm.values:
            # get name, pad with spaces
            s = val.name
            if len(val.name) < name_padding:
                s += ' ' * (name_padding - len(val.name)) 
            # add value, pad with spaces
            if val.value != None:
                s += ' = '
                if len(val.value) < value_padding:
                    s += ' ' * (value_padding - len(val.value)) 
                s += val.value
            # end of value, add comment
            s += ','
            if val.desc != None and len(val.desc) > 0:
                s += ' // ' + val.desc
            out.ln(s)
    
def generate_enum_function_declarations( enm:enum_type, out:formatted_output ) -> None:
    out.comment_ln('Converts a string into an enum: ' + enm.name + ' value.' )
    out.comment_ln('Returns status::ok on successful conversion.' )
    out.ln(f'ctle::status convert_string_to_enum( {enm.name} &dest , const std::string &src );')
    out.ln(f'ctle::status convert_string_to_enum( {enm.name} &dest , const char *src );')
    out.ln()

    out.comment_ln('Write the enum: ' + enm.name + ' value into a string. Checks that the enum value is valid, and returns status::ok on success.' )
    out.comment_ln('The version which retuns a string, returns an empty string if the enum is not a valid value.' )
    out.ln(f'ctle::status convert_enum_to_string( std::string &dest , {enm.name} src );')
    out.ln(f'std::string convert_enum_to_string( {enm.name} src );')
    out.ln()

    out.comment_ln('Get the description of the enum: ' + enm.name + ' value into as a string. Returns status::ok if a description is found.' )
    out.comment_ln('The version which retuns a string, returns an empty string if a description is not found.' )
    out.ln(f'ctle::status get_enum_value_description( std::string &dest , {enm.name} src );')
    out.ln(f'std::string get_enum_value_description( {enm.name} src );')
    out.ln()

    out.comment_ln('Checks if the value is a valid enum: ' + enm.name + ' and returns true if the value checks out ok.' )
    out.ln(f'bool is_valid_enum( {enm.name} value );')
    out.ln()    

# if use_lowercase_strings is True, all strings will be generated as lowercase. 
# if use_lowercase_strings is False, the strings will be generated identical as the enum values
def generate_enum_function_implementations( enm:enum_type, out:formatted_output, use_lowercase_strings:bool = False ) -> None:
    
    # generate the look-up tables 
    out.ln(f'static const std::unordered_map<{enm.name}, const char *> enum_{enm.name}_to_string_mapping = ')
    with out.blk( add_semicolon=True ):
        for val in enm.values:
            if use_lowercase_strings:
                out.blk_ln(f'{enm.name}::{val.name} , "{val.name.lower()}"', add_comma=True )
            else:
                out.blk_ln(f'{enm.name}::{val.name} , "{val.name}"', add_comma=True )
    out.ln()

    out.ln(f'static const std::unordered_map<{enm.name}, const char *> enum_{enm.name}_to_description_mapping = ')
    with out.blk( add_semicolon=True ):
        for val in enm.values:
            if val.desc != None:
                out.blk_ln(f'{enm.name}::{val.name} , "{val.desc}"', add_comma=True )
    out.ln()    

    out.ln(f'static const std::unordered_map<std::string, {enm.name}> enum_string_to_{enm.name}_mapping = ')
    with out.blk( add_semicolon=True ):
        for val in enm.values:
            if use_lowercase_strings:
                out.blk_ln(f'"{val.name.lower()}" , {enm.name}::{val.name}', add_comma=True )
            else:
                out.blk_ln(f'"{val.name}" , {enm.name}::{val.name}', add_comma=True )
    out.ln()   

    out.ln(f'ctle::status convert_string_to_enum( {enm.name} &dest , const std::string &src )')
    with out.blk():
        out.comment_ln('look up value, check if found')
        out.ln(f'auto it = enum_string_to_{enm.name}_mapping.find(src);')
        out.ln(f'if( it == enum_string_to_{enm.name}_mapping.end() )')
        with out.blk():
            out.ln('return ctle::status::not_found;')
        out.ln()
        out.comment_ln('all ok, return value in dest')
        out.ln('dest = it->second;')
        out.ln('return ctle::status::ok;')
    out.ln()

    out.ln(f'ctle::status convert_string_to_enum( {enm.name} &dest , const char *src )')
    with out.blk():
        out.comment_ln('check validity of input param')
        out.ln('if( !src )')
        with out.blk():
            out.ln('return ctle::status::invalid_param;')
        out.ln()
        out.comment_ln('look up value using std::string version of the function')
        out.ln('return convert_string_to_enum( dest, std::string(src) );')
    out.ln()

    out.ln(f'ctle::status convert_enum_to_string( std::string &dest , {enm.name} src )')
    with out.blk():
        out.comment_ln('look up enum value, check if found')
        out.ln(f'auto it = enum_{enm.name}_to_string_mapping.find(src);')
        out.ln(f'if( it == enum_{enm.name}_to_string_mapping.end() )')
        with out.blk():
            out.ln('return ctle::status::not_found;')
        out.ln()
        out.comment_ln('all ok, return name in dest')
        out.ln('dest = std::string(it->second);')
        out.ln('return ctle::status::ok;')    
    out.ln()

    out.ln(f'std::string convert_enum_to_string( {enm.name} src )')
    with out.blk():
        out.comment_ln('look up enum value, check if found')
        out.ln(f'auto it = enum_{enm.name}_to_string_mapping.find(src);')
        out.ln(f'if( it == enum_{enm.name}_to_string_mapping.end() )')
        with out.blk():
            out.ln('return ""; // not found')
        out.ln()
        out.comment_ln('all ok, return name string')
        out.ln('return std::string(it->second);')    
        out.ln()

    out.ln(f'ctle::status get_enum_value_description( std::string &dest , {enm.name} src )')
    with out.blk():
        out.comment_ln('look up enum value, check if found')
        out.ln(f'auto it = enum_{enm.name}_to_description_mapping.find(src);')
        out.ln(f'if( it == enum_{enm.name}_to_description_mapping.end() )')
        with out.blk():
            out.ln('return ctle::status::not_found;')
        out.ln()
        out.comment_ln('all ok, return description in dest')
        out.ln('dest = std::string(it->second);')
        out.ln('return ctle::status::ok;')    
    out.ln()

    out.ln(f'std::string get_enum_value_description( {enm.name} src )')
    with out.blk():
        out.comment_ln('look up enum value, check if found')
        out.ln(f'auto it = enum_{enm.name}_to_description_mapping.find(src);')
        out.ln(f'if( it == enum_{enm.name}_to_description_mapping.end() )')
        with out.blk():
            out.ln('return ""; // no description found')
        out.ln()
        out.comment_ln('all ok, return description string')
        out.ln('return std::string(it->second);')    
    out.ln()

    out.ln(f'bool is_valid_enum( {enm.name} value )')
    with out.blk():
        out.comment_ln('look up enum value, check if found')
        out.ln(f'auto it = enum_{enm.name}_to_string_mapping.find(value);')
        out.ln(f'if( it == enum_{enm.name}_to_string_mapping.end() )')
        with out.blk():
            out.ln('return false; // not found, not valid')
        out.ln()
        out.comment_ln('enum found')
        out.ln('return true;')    
    out.ln()

