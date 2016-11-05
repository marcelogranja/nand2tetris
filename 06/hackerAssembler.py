# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 03:51:43 2016

@author: marcelo
"""

import os
import re

COMP_TABLE = {
'0': '0101010',
'1': '0111111',
'-1': '0111010',
'D': '0001100',
'A': '0110000',
'M': '1110000',
'!D': '0001101',
'!A': '0110001',
'!M': '1110001',
'-D': '0001111',
'-A': '0110011',
'-M': '1110011',
'D+1': '0011111',
'A+1': '0110111',
'M+1': '1110111',
'D-1': '0001110',
'A-1': '0110010',
'M-1': '1110010',
'D+A': '0000010',
'D+M': '1000010',
'D-A': '0010011',
'D-M': '1010011',
'A-D': '0000111',
'M-D': '1000111',
'D&A': '0000000',
'D&M': '1000000',
'D|A': '0010101',
'D|M': '1010101'}

DEST_TABLE = {
'null': '000',
'M': '001',
'D': '010',
'MD': '011',
'A': '100',
'AM': '101',
'AD': '110',
'AMD': '111'}

JUMP_TABLE = {
'null': '000',
'JGT': '001',
'JEQ': '010',
'JGE': '011',
'JLT': '100',
'JNE': '101',
'JLE': '110',
'JMP': '111'}

symbol_table = {
'R0':'0',
'R1':'1',
'R2':'2',
'R3':'3',
'R4':'4',
'R5':'5',
'R6':'6',
'R7':'7',
'R8':'8',
'R9':'9',
'R10':'10',
'R11':'11',
'R12':'12',
'R13':'13',
'R14':'14',
'R15':'15',
'SCREEN':'16384',
'KBD':'24576',
'SP':'0',
'LCL':'1',
'ARG':'2',
'THIS':'3',
'THAT':'4'}

def parser(code):
    '''Parsers assembly files'''
    
    clean_code = []
    for line in code:
        
        # removes special characters and whitespace
        
        line = line.replace(' ','').replace('\r','').replace('\n','')
        line = line.split('//')[0] # ignore inline comments
        
        if len(line) == 0: # ignore empty lines
            continue
        elif line[:2] == '//': # ignore comment lines
            continue
        else:

            # core parsering
            label, rest, dest, comp, jump = None, None, None, None, None
            
            if line[0] == '(':
                line_type = 'L'
                label = line[ line.find('(')+1 : line.find(')') ]
                                
            elif line[0] == '@':
                line_type = 'A'
                rest = line[1:]
            else:
                line_type = 'C'
                dest = 'null'
                jump = 'null'
                
                if '=' in line and ';' in line:
                    dest = line.split('=')[0]
                    comp, jump = line.split('=')[1].split(';')                
                elif '=' in line:
                    dest, comp = line.split('=')                                
                elif ';' in line:
                    comp, jump = line.split(';')    
            clean_code.append( (line_type, label, rest, dest, comp, jump) )

    return clean_code

def symbol_translator(parsered_asm):
    '''translates hack symbols to values'''

    # initial pass to identify labels   
    idx = 0
    for line_type, label, rest, dest, comp, jump in parsered_asm:
        if line_type == 'L':
            symbol_table[label] = str(idx)
        else:
            idx += 1
    

    # translates symbols
 
    translated_asm = []
    new_variable_address = 16
    
    for line_type, label, rest, dest, comp, jump in parsered_asm:
        
        if line_type == 'A' and not rest.isdigit():
            
            # for initiating variables
            if not rest in symbol_table.keys():
                symbol_table[rest] = str(new_variable_address)
                rest = str(new_variable_address)
                new_variable_address += 1
    
            # for initiated variables
            else:
                rest = symbol_table[rest]

        translated_asm.append( (line_type, rest, dest, comp, jump) )        

    return translated_asm

    
def code_generator(translated_asm):
    '''translates from non-symbolic hack to machine code''' 
    
    hack_code = []
    for line_type, rest, dest, comp, jump in translated_asm:

        # handles A-instructions
        if line_type == 'A':
            hack_line = '0' + format( int(rest) , '015b')
    
        # handles C-instructions    
        elif line_type == 'C':
            hack_line = '111' + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]
        
        else:
            continue

        hack_code.append( hack_line + '\r\n')
        
    return hack_code

if __name__ == '__main__':
                            
    files = ['add','max','rect','pong']
    
    wd = os.path.join(os.getcwd(), 'pong/')
    os.chdir(wd)
    
    with open('Pong.asm', 'r') as fp:
        asm = fp.readlines()    
    
    parsered_asm = parser(asm)
    translated_asm = symbol_translator(parsered_asm)
    hack_code = code_generator(translated_asm)
                
            
    with open('Pong.hack', 'wb') as fp:
        fp.writelines( hack_code )