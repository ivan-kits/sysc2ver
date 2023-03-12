#!/usr/bin/python

############################################################################################
#
#           This program reads in a SystemC file then writes out verilog RTL file
#           making the appropriate substitutions. 
#
#           syntax: sysc2ver.py filename(no extension)
#
#	    Author: John Hamilton - Medtronic
#	    Copyright (c) 2004, Medtronic Inc.
#
#	    This software may be used and distributed according to the terms of
#	    the GNU General Public License (GPL), incorporated herein by reference.
#
#	    Initial revision 0.5
#
############################################################################################
import sys
import string
import re
infile=[]
ports=[]
senslst=[]
moduleports=[]
ioports=[]
iodefs='\n'
regdefs='\n'
seqptr = initptr = 0
state = 0
senscmd1=''
senscmd=[]
sensindx = 0
casecount = 0
casetree = [0,0,0,0,0,0,0,0]

# Check that there is a filename specified then open the header file and output file
if len(sys.argv) > 1:
  fpath = sys.argv[1]+'.h'
  f=open(fpath, 'r')
  fo=open(sys.argv[1]+'.v', 'w')
  fp=open('portlist.txt', 'a')

  # Read in header file and write out verilog file
  for line in f.readlines():

    # STATE 0 - Add comments to verilog file
    if state == 0: # Find comments
      if line[0:9]=='SC_MODULE':
	state = 1
	modulestr = 'module '+sys.argv[1]+' ('
	portstr = sys.argv[1]+' '+sys.argv[1]+' ('
      elif line[0:8]!='#include':
	fo.write(line)

    # STATE 1 - Read in I/O signals, create I/O defs and module statement
    elif state == 1: # Find array definitions
      ports = string.split(line)
      if len(ports) > 1:
	isreg = 0
	if ports[0] == 'sc_in<bool>':
	  iodefs = iodefs + '  input        '
	elif ports[0] == 'sc_out<bool>':
	  iodefs = iodefs + '  output       '
	  regdefs = regdefs + '  reg          '
	  isreg = 1
	elif ports[0][0:12] == 'sc_inout_rv<':
	  if ports[0][13] == '>':
	    iodefs = iodefs + '  inout  [' + str(int(ports[0][12]) -1) + ':0] '
	  else:
	    indxval = int(ports[0][12])*10 + int(ports[0][13])
	    iodefs = iodefs + '  input  [' + str(indxval - 1) + ':0]'
	elif ports[0][0:14] == 'sc_in<sc_uint<':
	  if ports[0][15] == '>':
	    iodefs = iodefs + '  input  [' + str(int(ports[0][14]) -1) + ':0] '
	  else:
	    indxval = int(ports[0][14])*10 + int(ports[0][15])
	    iodefs = iodefs + '  input  [' + str(indxval - 1) + ':0]'
	elif ports[0][0:17] == 'sc_in<sc_biguint<':
	  if ports[0][18] == '>':
	    iodefs = iodefs + '  input  [' + str(int(ports[0][17]) -1) + ':0] '
	  else:
	    indxval = int(ports[0][17])*10 + int(ports[0][18])
	    iodefs = iodefs + '  input  [' + str(indxval - 1) + ':0]'
	elif ports[0][0:15] == 'sc_out<sc_uint<':
	  if ports[0][16] == '>':
	    iodefs = iodefs + '  output [' + str(int(ports[0][15]) -1) + ':0] '
	    regdefs = regdefs + '  reg    [' + str(int(ports[0][15]) -1) + ':0] '
	    isreg = 1
	  else:
	    indxval = int(ports[0][15])*10 + int(ports[0][16])
	    iodefs = iodefs + '  output [' + str(indxval -1) + ':0]'
	    regdefs = regdefs + '  reg    [' + str(indxval -1) + ':0]'
	    isreg = 1
	elif ports[0][0:18] == 'sc_out<sc_biguint<':
	  if ports[0][19] == '>':
	    iodefs = iodefs + '  output [' + str(int(ports[0][18]) -1) + ':0] '
	    regdefs = regdefs + '  reg    [' + str(int(ports[0][18]) -1) + ':0] '
	    isreg = 1
	  else:
	    indxval = int(ports[0][18])*10 + int(ports[0][19])
	    iodefs = iodefs + '  output [' + str(indxval -1) + ':0]'
	    regdefs = regdefs + '  reg    [' + str(indxval -1) + ':0]'
	    isreg = 1
	if ports[1] == '>':
	  ioname = string.replace(ports[2],';','')
	  modulestr = modulestr + ioname + ', '
	  portstr = portstr + '.' + ioname + '(' + ioname + ')' + ', '
	else:
	  ioname = string.replace(ports[1],';','')
	  modulestr = modulestr + ioname + ', '
	  portstr = portstr + '.' + ioname + '(' + ioname + ')' + ', '
	iodefs = iodefs + '  ' + ioname + ';\n'
	if isreg == 1:
	  regdefs = regdefs + '  ' + ioname + ';\n'
      else:
	fo.write(modulestr[0:len(modulestr)-2] + ');\n')
	fp.write(portstr[0:len(portstr)-2] + ');\n')
	fo.write(iodefs)
	fo.write(regdefs)
	regdefs = '\n'
	state = 2

    # STATE 2 - Create local register definitions
    elif state == 2:
      ports = string.split(line)
      if len(ports) > 1:
	if ports[0] == 'bool':
	  iodefs = iodefs + '  reg          '
	elif ports[0][0:8] == 'sc_uint<':
	  if ports[0][9] == '>':
	    regdefs = regdefs + '  reg    [' + str(int(ports[0][8]) -1) + ':0] '
	  else:
	    indxval = int(ports[0][8])*10 + int(ports[0][9])
	    regdefs = regdefs + '  reg    [' + str(indxval -1) + ':0]'
	elif ports[0][0:11] == 'sc_biguint<':
	  if ports[0][12] == '>':
	    regdefs = regdefs + '  reg    [' + str(int(ports[0][11]) -1) + ':0] '
	  else:
	    indxval = int(ports[0][11])*10 + int(ports[0][12])
	    regdefs = regdefs + '  reg    [' + str(indxval -1) + ':0]'

	if ports[1] == '>':
	  ioname = string.replace(ports[2],';','')
	else:
	  ioname = string.replace(ports[1],';','')
	if string.find(ioname,'[') > 0:
	  ioname = ioname[0:string.find(ioname,'[')+1]+"0:"+str(int(ioname[(string.find(ioname,'[')+1):string.find(ioname,']')])-1)+"]"
        regdefs = regdefs + '  ' + ioname + ';\n'
      else:
	regdefs = re.sub('\[0:0\]','     ',regdefs)
	fo.write(regdefs)
	state = 3

    # STATE 3 - Create method and sensitivity definitions
    elif state == 3:
      senslst = string.split(line)
      if len(senslst) > 1:
	if senslst[0][0:9] == 'sensitive':
	  edgedir = ''
	  if senslst[0][9:13] == '_pos':
	    senscmd.append('always @(posedge ')
	    edgedir = 'posedge '
	  elif senslst[0][9:13] == '_neg':
	    senscmd.append('always @(negedge ')
	    edgedir = 'negedge '
	  else:
	    senscmd.append('always @(')
	  firstone = 0
	  for senselem in senslst:
	    if senselem[0:9] != 'sensitive':
	      if senselem[0:2] == '<<':
		i = len(senscmd) - 1
		if firstone > 0:
		  senscmd[i] = senscmd[i] + ' or ' + edgedir
		else:
		  firstone = 1
	      else:
		senscmd[i] = senscmd[i] + string.replace(senselem,';',')\n')
  f.close()
  fpath = sys.argv[1]+'.cpp'
  f=open(fpath, 'r')
  state = 0

  # Read in code file and write out verilog file
  fo.write('\n\n')
  edgecode = 0
  for line in f.readlines():
    subflag = string.find(line,'//#SUB')
    if (subflag >= 0):
      line = line[subflag+6:];
      fo.write(line)
    elif line[0:4] == 'void':
      newline = senscmd.pop(0)
      if (string.find(newline,'posedge') >= 0) or (string.find(newline,'negedge') >= 0):
	edgecode = 1
      else:
	edgecode = 0
      fo.write('\n' + newline)
    else:
      if string.find(line,'case') >= 0:
	line = string.replace(line,'case ','')
	i = string.find(line,':')
	line = line[0:i+1] + ' begin ' + line[i+1:]
      if string.find(line,'switch') >= 0:
	casecount = casecount + 1
	line = string.replace(line,'switch','case')
	if string.find(line,'{') >= 0:
          line = string.replace(line,'{','')
          casetree[casecount] = casetree[casecount] + 1
      if string.find(line,'{') >= 0:
	if (casecount > 0):
	  if casetree[casecount] == 0:
	    line = string.replace(line,'{','')
	  else:
	    line = re.sub('{','begin',line)
          casetree[casecount] = casetree[casecount] + 1
	else:
	  line = re.sub('{','begin',line)
      if string.find(line,'}') >= 0:
	if (casecount > 0):
	  casetree[casecount] = casetree[casecount] - 1
	  if casetree[casecount] == 0:
	    line = re.sub('}','endcase',line)
	    casecount = casecount - 1
	  else:
	    line = re.sub('}','end',line)
	else:
          line = re.sub('}','end',line)
      line = re.sub('.read\(\)','',line)
      line = re.sub('"ZZZZZZZZ"','8\'hzz',line)
      newline = re.split('([A-Z])',line,1)
      if len(newline) == 3:
	line = newline[0] + '`' + newline[1] + newline[2]
      line = re.sub('  break;','end',line)
      line = re.sub('break;','end',line)
      i = string.find(line,'0x')
      if i >= 0:
	if line[i+3:i+4] == ';' or line[i+3:i+4] == ' ':
	  line = re.sub('0x','4\'h',line)
	elif line[i+4:i+5] == ';' or line[i+4:i+5] == ' ':
	  line = re.sub('0x','8\'h',line)
	elif line[i+5:i+6] == ';' or line[i+5:i+6] == ' ':
	  line = re.sub('0x','12\'h',line)
	elif line[i+6:i+7] == ';' or line[i+6:i+7] == ' ':
	  line = re.sub('0x','16\'h',line)
	elif line[i+7:i+8] == ';' or line[i+7:i+8] == ' ':
	  line = re.sub('0x','20\'h',line)
	elif line[i+8:i+9] == ';' or line[i+8:i+9] == ' ':
	  line = re.sub('0x','24\'h',line)
	elif line[i+9:i+10] == ';' or line[i+9:i+10] == ' ':
	  line = re.sub('0x','28\'h',line)
	elif line[i+10:i+11] == ';' or line[i+10:i+11] == ' ':
	  line = re.sub('0x','32\'h',line)
	elif line[i+11:i+12] == ';' or line[i+11:i+12] == ' ':
	  line = re.sub('0x','36\'h',line)
	elif line[i+12:i+13] == ';' or line[i+12:i+13] == ' ':
	  line = re.sub('0x','40\'h',line)
	elif line[i+13:i+14] == ';' or line[i+13:i+14] == ' ':
	  line = re.sub('0x','44\'h',line)
	elif line[i+14:i+15] == ';' or line[i+14:i+15] == ' ':
	  line = re.sub('0x','48\'h',line)
	elif line[i+15:i+16] == ';' or line[i+15:i+16] == ' ':
	  line = re.sub('0x','52\'h',line)
	elif line[i+16:i+17] == ';' or line[i+16:i+17] == ' ':
	  line = re.sub('0x','56\'h',line)
	elif line[i+17:i+18] == ';' or line[i+17:i+18] == ' ':
	  line = re.sub('0x','60\'h',line)
	elif line[i+18:i+19] == ';' or line[i+18:i+19] == ' ':
	  line = re.sub('0x','64\'h',line)
      if edgecode == 1:
	line = re.sub(' = ',' <= ',line)
      if string.find(line,'(0') >= 0:
	line = re.sub('\(0','{3\'b000',line)
	line = re.sub('\)','}',line)
      if string.find(line,'.range') >= 0:
	strmatch = re.compile(r".range\((\d+)\,(\d+)\)")
	line = strmatch.sub(r'[\1:\2]', line)
      if string.find(line,'= (') >= 0:
	line = re.sub('\(','{',line)
	line = re.sub('\)','}',line)
      line = re.sub('default:','default: begin',line)
      if line[0:8]!='#include':
	fo.write(line)

  fo.write('endmodule\n')
  f.close()
  fo.close()
  fp.write('\n')
  fp.close()
  print "done with " + sys.argv[1] + "!"
  fpath = sys.argv[1]+'.cpp'

# If no file specified on command line, print out syntax
else:
  print "genverilog.py cfile"
