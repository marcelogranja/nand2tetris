# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 03:51:43 2016

@author: marcelo
"""

import os

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


def parser(code):
    '''parsers assembly files. Still missing A and C instructions handing'''
    
    output = []
    for line in code:
        line = line.replace(' ','').replace('\r','').replace('\n','')
        
        if len(line) == 0: # ignore empty lines
            continue
        elif line[:2] == '//': # ignore comment lines
            continue
        else:
            line = line.split('//')[0] # ignore inline comments
            output.append(line)

    return output            

def symbol_table(code):
    '''translates symbols to values'''
    pass
#predefined symbols
#only on a-instructions    

#loops
#prereading searching for ()
#create looptable where each () take the value of the next line as indicated by enumerate    


#variables symbols
#starts at memory addr 16
#when seen for the first time, jump reach a table


    
def code_generator(asm_code):
    '''translates from hacker to machine code'''    
    
    hack_code = []
    for line in asm_code:
#        print line,
        
        # handles A-instructions
        if line[0] == '@':
            hack_line = '0' + format( int(line[1:]) , '015b')
    
        # handles C-instructions    
        else:
            dest = 'null'
            jump = 'null'
            
            if '=' in line and ';' in line:
                dest = line.split('=')[0]
                comp, jump = line.split('=')[1].split(';')                
            elif '=' in line:
                dest, comp = line.split('=')                                
            elif ';' in line:
                comp, jump = line.split(';')
                
            hack_line = '111' + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]

        hack_code.append( hack_line + '\r\n')
#        print hacker_line
    return hack_code

                            
files = ['add','max','rect','pong']

wd = os.path.join(os.getcwd(), 'rect/')
os.chdir(wd)

with open('RectL.asm', 'r') as fp:
    asm = fp.readlines()    

clean_asm = parser(asm)
hack_code = code_generator(clean_asm)
            
        
with open('Rect.hack', 'wb') as fp:
    fp.writelines( hack_code )

#main