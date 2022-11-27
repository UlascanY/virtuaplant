#!/usr/bin/env python
import logging #line:6
from twisted .internet import reactor #line:10
from pymodbus .server .asynchronous import StartTcpServer #line:13
from pymodbus .device import ModbusDeviceIdentification #line:14
from pymodbus .datastore import ModbusSequentialDataBlock #line:15
from pymodbus .datastore import ModbusSlaveContext ,ModbusServerContext #line:16
from pymodbus .transaction import ModbusRtuFramer ,ModbusAsciiFramer #line:17
import sys ,random #line:20
import pygame #line:21
from pygame .locals import *#line:22
from pygame .color import *#line:23
import pymunk #line:24
import socket #line:27
import argparse #line:30
import os #line:32
import sys #line:33
import time #line:34
class MyParser (argparse .ArgumentParser ):#line:38
    def error (O00OO0OO0OO0O0OOO ,O000OO000O0OO00O0 ):#line:39
        sys .stderr .write ('error: %s\n'%O000OO000O0OO00O0 )#line:40
        O00OO0OO0OO0O0OOO .print_help ()#line:41
        sys .exit (2 )#line:42
parser =MyParser (description ='This Python script starts the SCADA/ICS World Server',epilog ='',add_help =True )#line:47
parser .add_argument ("-t",action ="store",dest ="server_addr",help ="Modbus server IP address to listen on")#line:50
if len (sys .argv )==1 :#line:53
	parser .print_help ()#line:54
	sys .exit (1 )#line:55
args =parser .parse_args ()#line:58
logging .basicConfig ()#line:60
log =logging .getLogger ()#line:61
log .setLevel (logging .INFO )#line:62
SCREEN_WIDTH =580 #line:65
SCREEN_HEIGHT =460 #line:66
FPS =50.0 #line:67
MODBUS_SERVER_PORT =5022 #line:70
oil_spilled_amount =0 #line:73
oil_processed_amount =0 #line:74
PLC_FEED_PUMP =0x01 #line:77
PLC_TANK_LEVEL =0x02 #line:78
PLC_OUTLET_VALVE =0x03 #line:79
PLC_SEP_VALVE =0x04 #line:80
PLC_OIL_SPILL =0x06 #line:81
PLC_OIL_PROCESSED =0x07 #line:82
PLC_WASTE_VALVE =0x08 #line:83
PLC_OIL_UPPER =0x09 #line:84
tank_level_collision =0x4 #line:87
ball_collision =0x5 #line:88
outlet_valve_collision =0x6 #line:89
sep_valve_collision =0x7 #line:90
waste_valve_collision =0x8 #line:91
oil_spill_collision =0x9 #line:92
oil_processed_collision =0x3 #line:93
def get_ip ():#line:95
    from netifaces import interfaces ,ifaddresses ,AF_INET #line:96
    for O000000000O0OOOOO in interfaces ():#line:97
        O0OO000OO00OOO00O =[OO0OO0O0O00OO00O0 ['addr']for OO0OO0O0O00OO00O0 in ifaddresses (O000000000O0OOOOO ).setdefault (AF_INET ,[{'addr':'No IP addr'}])]#line:98
        if O000000000O0OOOOO =="enp0s3":#line:99
            return ''.join (O0OO000OO00OOO00O )#line:100
def PLCSetTag (O00O0O00OO000OO0O ,O0O0O0O0OOO0O0OOO ):#line:103
    context [0x0 ].setValues (3 ,O00O0O00OO000OO0O ,[O0O0O0O0OOO0O0OOO ])#line:104
def PLCGetTag (OO0O0OO0OO0OOOO00 ):#line:107
    return context [0x0 ].getValues (3 ,OO0O0OO0OO0OOOO00 ,count =1 )[0 ]#line:108
def to_pygame (OO0O00OO000OO0OOO ):#line:110
    ""#line:111
    return int (OO0O00OO000OO0OOO .x ),int (-OO0O00OO000OO0OOO .y +600 )#line:112
def add_ball (OOO0OOOOOOOO00000 ):#line:115
    OO00O0O00O0OO0O0O =0.01 #line:116
    O00O00OOO0O0O0000 =2 #line:117
    O0OO0OO0O0O0000O0 =pymunk .moment_for_circle (OO00O0O00O0OO0O0O ,0 ,O00O00OOO0O0O0000 ,(0 ,0 ))#line:118
    OOOOOOO00000OO0O0 =pymunk .Body (OO00O0O00O0OO0O0O ,O0OO0OO0O0O0000O0 )#line:119
    OOOOOOO00000OO0O0 ._bodycontents .v_limit =120 #line:120
    OOOOOOO00000OO0O0 ._bodycontents .h_limit =1 #line:121
    O00OOOO0O0OOOO0O0 =random .randint (69 ,70 )#line:122
    OOOOOOO00000OO0O0 .position =O00OOOO0O0OOOO0O0 ,565 #line:123
    O00O00OOO0OO00000 =pymunk .Circle (OOOOOOO00000OO0O0 ,O00O00OOO0O0O0000 ,(0 ,0 ))#line:124
    O00O00OOO0OO00000 .friction =0.0 #line:125
    O00O00OOO0OO00000 .collision_type =ball_collision #line:126
    OOO0OOOOOOOO00000 .add (OOOOOOO00000OO0O0 ,O00O00OOO0OO00000 )#line:127
    return O00O00OOO0OO00000 #line:128
def draw_ball (O0OO00O0O00O00000 ,O0O000O000O0O000O ,color =THECOLORS ['brown']):#line:131
    OO00O0000O000OO0O =int (O0O000O000O0O000O .body .position .x ),600 -int (O0O000O000O0O000O .body .position .y )#line:132
    pygame .draw .circle (O0OO00O0O00O00000 ,color ,OO00O0000O000OO0O ,int (O0O000O000O0O000O .radius ),2 )#line:133
def sep_valve (OO0000OO0OO0OO0OO ):#line:136
    OO0OOOO00O0O000O0 =pymunk .Body ()#line:137
    OO0OOOO00O0O000O0 .position =(327 ,218 )#line:138
    O00O00000OO0O00O0 =2 #line:139
    O000O00OOOO0OO0OO =(-15 ,0 )#line:140
    OO00O0O00O0O0OOOO =(15 ,0 )#line:141
    O000O0OOOOOO0OOO0 =pymunk .Segment (OO0OOOO00O0O000O0 ,O000O00OOOO0OO0OO ,OO00O0O00O0O0OOOO ,O00O00000OO0O00O0 )#line:142
    O000O0OOOOOO0OOO0 .collision_type =sep_valve_collision #line:143
    OO0000OO0OO0OO0OO .add (O000O0OOOOOO0OOO0 )#line:144
    return O000O0OOOOOO0OOO0 #line:145
def waste_valve (O0000OOO0OOO00O0O ):#line:148
    OOO000OOO0OOOOOO0 =pymunk .Body ()#line:149
    OOO000OOO0OOOOOO0 .position =(225 ,218 )#line:150
    OO0OO0OO00OO000OO =2 #line:151
    O0O0OO00000O00OO0 =(-8 ,0 )#line:152
    OO000O00OOO0O0OO0 =(9 ,0 )#line:153
    O0O0OOOOO0O00000O =pymunk .Segment (OOO000OOO0OOOOOO0 ,O0O0OO00000O00OO0 ,OO000O00OOO0O0OO0 ,OO0OO0OO00OO000OO )#line:154
    O0O0OOOOO0O00000O .collision_type =waste_valve_collision #line:155
    O0000OOO0OOO00O0O .add (O0O0OOOOO0O00000O )#line:156
    return O0O0OOOOO0O00000O #line:157
def tank_level_sensor (O00O0O00O00O0OOOO ):#line:160
    OOO0O0O0O0OOO0OOO =pymunk .Body ()#line:161
    OOO0O0O0O0OOO0OOO .position =(115 ,535 )#line:162
    OOO0O0OOOOOO0000O =3 #line:163
    O0O00O000O0OOO00O =(0 ,0 )#line:164
    OO00OO0O00O0000O0 =(0 ,0 )#line:165
    OO0OOOOOO00OOO000 =pymunk .Circle (OOO0O0O0O0OOO0OOO ,OOO0O0OOOOOO0000O ,(0 ,0 ))#line:166
    OO0OOOOOO00OOO000 .collision_type =tank_level_collision #line:167
    O00O0O00O00O0OOOO .add (OO0OOOOOO00OOO000 )#line:168
    return OO0OOOOOO00OOO000 #line:169
def outlet_valve (O000000OOOOO00000 ):#line:172
    OOOOO0OO0O00O0O00 =pymunk .Body ()#line:173
    OOOOO0OO0O00O0O00 .position =(70 ,410 )#line:174
    O0O000OO00000OO00 =(-14 ,0 )#line:176
    O0OOOOO00O0OOO00O =(14 ,0 )#line:177
    O0O00O0O0O0OOO0O0 =2 #line:178
    OO00OO00OOO000OOO =pymunk .Segment (OOOOO0OO0O00O0O00 ,O0O000OO00000OO00 ,O0OOOOO00O0OOO00O ,O0O00O0O0O0OOO0O0 )#line:179
    OO00OO00OOO000OOO .collision_type =outlet_valve_collision #line:180
    O000000OOOOO00000 .add (OO00OO00OOO000OOO )#line:181
    return OO00OO00OOO000OOO #line:182
def oil_spill_sensor (OOO000000OOO00O0O ):#line:185
    O00OO00O00OOOO0OO =pymunk .Body ()#line:186
    O00OO00O00OOOO0OO .position =(0 ,100 )#line:187
    OO0O0OOOOO00O0O00 =7 #line:188
    OO0OO000O000OO0O0 =(0 ,75 )#line:189
    O00O00O0OO0000OO0 =(137 ,75 )#line:190
    O00OO00OO0OOO0O0O =pymunk .Segment (O00OO00O00OOOO0OO ,OO0OO000O000OO0O0 ,O00O00O0OO0000OO0 ,OO0O0OOOOO00O0O00 )#line:191
    O00OO00OO0OOO0O0O .collision_type =oil_spill_collision #line:192
    OOO000000OOO00O0O .add (O00OO00OO0OOO0O0O )#line:193
    return O00OO00OO0OOO0O0O #line:194
def oil_processed_sensor (O0O0OOO0OO000O0O0 ):#line:197
    O0O0OO0O00OOO0O00 =pymunk .Body ()#line:198
    O0O0OO0O00OOO0O00 .position =(327 ,218 )#line:199
    O00O0O000OO000OO0 =7 #line:200
    O0OOOO0OO000OOO0O =(-12 ,-5 )#line:201
    OO0OO00OOOOOOO0O0 =(12 ,-5 )#line:202
    O00O0000O0OOO000O =pymunk .Segment (O0O0OO0O00OOO0O00 ,O0OOOO0OO000OOO0O ,OO0OO00OOOOOOO0O0 ,O00O0O000OO000OO0 )#line:203
    O00O0000O0OOO000O .collision_type =oil_processed_collision #line:204
    O0O0OOO0OO000O0O0 .add (O00O0000O0OOO000O )#line:205
    return O00O0000O0OOO000O #line:206
def add_pump (O0O0O0OO0O0O000OO ):#line:209
    O0OO00O000O0000O0 =pymunk .Body ()#line:210
    O0OO00O000O0000O0 .position =(70 ,585 )#line:211
    OO0OO00O000OO00O0 =pymunk .Poly .create_box (O0OO00O000O0000O0 ,(15 ,20 ),(0 ,0 ),0 )#line:212
    O0O0O0OO0O0O000OO .add (OO0OO00O000OO00O0 )#line:213
    return OO0OO00O000OO00O0 #line:214
def add_oil_unit (OO000O00O0O0OOO0O ):#line:218
    OOOO00O0OO0O00OO0 =pymunk .Body ()#line:219
    OOOO00O0OO0O00OO0 .position =(300 ,300 )#line:220
    OO0O0OOO0OO00O0OO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-278 ,250 ),(-278 ,145 ),1 )#line:223
    O00OOO00O0000000O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-278 ,145 ),(-246 ,107 ),1 )#line:224
    O000O0OO0OO00OOO0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-180 ,250 ),(-180 ,145 ),1 )#line:225
    OO0O0O00O0O0O0000 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-180 ,145 ),(-215 ,107 ),1 )#line:226
    O0OO000O0000O0OO0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-246 ,107 ),(-246 ,53 ),1 )#line:229
    OO00OOOOO0OO00OOO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-246 ,53 ),(-19 ,53 ),1 )#line:230
    O00OOO0000OO00O0O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-19 ,53 ),(-19 ,33 ),1 )#line:231
    OO000OO00OOOO000O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-215 ,107 ),(-215 ,80 ),1 )#line:232
    O0OO00O0OO0O000O0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-215 ,80 ),(7 ,80 ),1 )#line:233
    OOO000O0O000O000O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(7 ,80 ),(7 ,33 ),1 )#line:234
    OOOOOOO000O00O0OO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-19 ,31 ),(-95 ,31 ),1 )#line:237
    O0O000O00O000OO00 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-95 ,31 ),(-95 ,-23 ),1 )#line:238
    OO0O0000O0000OOOO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-95 ,-23 ),(-83 ,-23 ),1 )#line:239
    OOOO0000OO0OO00OO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-83 ,-23 ),(-80 ,-80 ),1 )#line:240
    OOOO0000O0OOO000O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-68 ,-80 ),(-65 ,-23 ),1 )#line:241
    O0000OOO00O0OOO0O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-65 ,-23 ),(-45 ,-23 ),1 )#line:242
    O0000O0OO0O0O000O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-45 ,-23 ),(-45 ,-67 ),1 )#line:243
    O00000O000OOO0O0O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-45 ,-67 ),(13 ,-67 ),1 )#line:244
    OO0000O00O00O0OO0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(13 ,-67 ),(13 ,-82 ),1 )#line:245
    OOOOO0OOO0OO0000O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(43 ,-82 ),(43 ,-67 ),1 )#line:246
    O0OO0O00OOO0OO00O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(43 ,-67 ),(65 ,-62 ),1 )#line:247
    OO0O0OOOOOO0O0000 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(65 ,-62 ),(77 ,31 ),1 )#line:248
    O0000O00OOO00OO00 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(77 ,31 ),(7 ,31 ),1 )#line:249
    OO0O0O0000OO0O00O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-3 ,-67 ),(-3 ,10 ),3 )#line:250
    OO000O0O0O00OO0OO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-3 ,10 ),(-65 ,-23 ),1 )#line:251
    OO0O00OO0O00OO00O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(43 ,-85 ),(43 ,-113 ),1 )#line:254
    OOOOOOO00OOOOO0O0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(43 ,-113 ),(580 ,-113 ),1 )#line:255
    O0000O0OO00O00OO0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(13 ,-85 ),(13 ,-140 ),1 )#line:256
    O000000O0000O0O0O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(13 ,-140 ),(580 ,-140 ),1 )#line:257
    O0OO00O0OO0O00OOO =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-87 ,-85 ),(-87 ,-112 ),1 )#line:260
    OOOO0OOOO0O00OO0O =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-60 ,-85 ),(-60 ,-140 ),1 )#line:261
    O000OO0000O0O0000 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-87 ,-112 ),(-163 ,-112 ),1 )#line:262
    O0OO0OOOO00OO0O00 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-60 ,-140 ),(-134 ,-140 ),1 )#line:263
    OO0OO000O0OO000O0 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-163 ,-112 ),(-163 ,-185 ),1 )#line:264
    O0000O000O0O00000 =pymunk .Segment (OOOO00O0OO0O00OO0 ,(-134 ,-140 ),(-134 ,-185 ),1 )#line:265
    OO000O00O0O0OOO0O .add (OO0O0OOO0OO00O0OO ,O00OOO00O0000000O ,O000O0OO0OO00OOO0 ,OO0O0O00O0O0O0000 ,O0OO000O0000O0OO0 ,OO00OOOOO0OO00OOO ,O00OOO0000OO00O0O ,OO000OO00OOOO000O ,O0OO00O0OO0O000O0 ,OOO000O0O000O000O ,OOOOOOO000O00O0OO ,O0O000O00O000OO00 ,OO0O0000O0000OOOO ,OOOO0000OO0OO00OO ,OOOO0000O0OOO000O ,O0000OOO00O0OOO0O ,O0000O0OO0O0O000O ,O00000O000OOO0O0O ,OO0000O00O00O0OO0 ,OOOOO0OOO0OO0000O ,O0OO0O00OOO0OO00O ,OO0O0OOOOOO0O0000 ,O0000O00OOO00OO00 ,OO0O0O0000OO0O00O ,OO0O00OO0O00OO00O ,OOOOOOO00OOOOO0O0 ,O0000O0OO00O00OO0 ,O000000O0000O0O0O ,O0OO00O0OO0O00OOO ,OOOO0OOOO0O00OO0O ,O000OO0000O0O0000 ,O0OO0OOOO00OO0O00 ,OO0OO000O0OO000O0 ,O0000O000O0O00000 ,OO000O0O0O00OO0OO )#line:269
    return (OO0O0OOO0OO00O0OO ,O00OOO00O0000000O ,O000O0OO0OO00OOO0 ,OO0O0O00O0O0O0000 ,O0OO000O0000O0OO0 ,OO00OOOOO0OO00OOO ,O00OOO0000OO00O0O ,OO000OO00OOOO000O ,O0OO00O0OO0O000O0 ,OOO000O0O000O000O ,OOOOOOO000O00O0OO ,O0O000O00O000OO00 ,OO0O0000O0000OOOO ,OOOO0000OO0OO00OO ,OOOO0000O0OOO000O ,O0000OOO00O0OOO0O ,O0000O0OO0O0O000O ,O00000O000OOO0O0O ,OO0000O00O00O0OO0 ,OOOOO0OOO0OO0000O ,O0OO0O00OOO0OO00O ,OO0O0OOOOOO0O0000 ,O0000O00OOO00OO00 ,OO0O0O0000OO0O00O ,OO0O00OO0O00OO00O ,OOOOOOO00OOOOO0O0 ,O0000O0OO00O00OO0 ,O000000O0000O0O0O ,O0OO00O0OO0O00OOO ,OOOO0OOOO0O00OO0O ,O000OO0000O0O0000 ,O0OO0OOOO00OO0O00 ,OO0OO000O0OO000O0 ,O0000O000O0O00000 ,OO000O0O0O00OO0OO )#line:273
def draw_polygon (OO00OOOOO00OOO000 ,OO00OO0000OOOO00O ):#line:276
    OO0OO0O00OOOO00O0 =OO00OO0000OOOO00O .get_vertices ()#line:277
    O00OO0O000O0O0OO0 =[]#line:278
    for OO00O0O00O00O000O in OO0OO0O00OOOO00O0 :#line:279
        O00OO0O000O0O0OO0 .append (to_pygame (OO00O0O00O00O000O ))#line:280
    pygame .draw .polygon (OO00OOOOO00OOO000 ,THECOLORS ['black'],O00OO0O000O0O0OO0 )#line:281
def draw_line (O0O0OO000O0OO0O00 ,OOO0OO0OO000OOO0O ,color =None ):#line:284
    OOOO0OOOOO0OO00OO =OOO0OO0OO000OOO0O .body #line:285
    O0OOO0OOO00OOOO0O =OOOO0OOOOO0OO00OO .position +OOO0OO0OO000OOO0O .a .rotated (OOOO0OOOOO0OO00OO .angle )#line:286
    OOOOO0OO0OO000O0O =OOOO0OOOOO0OO00OO .position +OOO0OO0OO000OOO0O .b .rotated (OOOO0OOOOO0OO00OO .angle )#line:287
    O00OO00OOO00OO0O0 =to_pygame (O0OOO0OOO00OOOO0O )#line:288
    OOOO0OO0OOOO0OOO0 =to_pygame (OOOOO0OO0OO000O0O )#line:289
    if color is None :#line:290
        pygame .draw .lines (O0O0OO000O0OO0O00 ,THECOLORS ["black"],False ,[O00OO00OOO00OO0O0 ,OOOO0OO0OOOO0OOO0 ])#line:291
    else :#line:292
        pygame .draw .lines (O0O0OO000O0OO0O00 ,color ,False ,[O00OO00OOO00OO0O0 ,OOOO0OO0OOOO0OOO0 ])#line:293
def draw_lines (OOOOOO0O0O00OO0OO ,O0O00O0OO00O00OOO ):#line:296
    for OOO0O000OOOO0000O in O0O00O0OO00O00OOO :#line:297
        OO0OOOO0O000OO000 =OOO0O000OOOO0000O .body #line:298
        OOOO0OO000OOOOO00 =OO0OOOO0O000OO000 .position +OOO0O000OOOO0000O .a .rotated (OO0OOOO0O000OO000 .angle )#line:299
        O0OOO0OO00O000O0O =OO0OOOO0O000OO000 .position +OOO0O000OOOO0000O .b .rotated (OO0OOOO0O000OO000 .angle )#line:300
        OOOOOOOOO0OOOO0OO =to_pygame (OOOO0OO000OOOOO00 )#line:301
        OO00O00000OO0OO0O =to_pygame (O0OOO0OO00O000O0O )#line:302
        pygame .draw .lines (OOOOOO0O0O00OO0OO ,THECOLORS ["gray"],False ,[OOOOOOOOO0OOOO0OO ,OO00O00000OO0OO0O ])#line:303
def no_collision (O00O000OOO0000O00 ,O00OO0OO0OO0O0O00 ,*O00OO00O00OO0O0OO ,**OOO000O0O0OO0000O ):#line:307
    return True #line:308
def level_reached (OOO0OO00OO0O00O00 ,O000000O0OO00000O ,*O000O000O0OOOO00O ,**O0000O00OOO00O0OO ):#line:311
    log .debug ("Level reached")#line:312
    PLCSetTag (PLC_TANK_LEVEL ,1 )#line:313
    PLCSetTag (PLC_FEED_PUMP ,0 )#line:314
    return False #line:315
def oil_spilled (O00O0OO0O00OOOO00 ,O0O00OOO000O0OO0O ,*O0OOOO0OOOO00O000 ,**OO00000OO000OOOO0 ):#line:317
    global oil_spilled_amount #line:318
    log .debug ("Oil Spilled")#line:319
    oil_spilled_amount =oil_spilled_amount +1 #line:320
    PLCSetTag (PLC_OIL_SPILL ,oil_spilled_amount )#line:321
    PLCSetTag (PLC_FEED_PUMP ,0 )#line:322
    return False #line:323
def oil_processed (O00O0OO00O00OOO00 ,O0O0O00000OOO00OO ,*O0OOO000O000OO000 ,**OOO00O0000OOO0OO0 ):#line:325
    global oil_processed_amount #line:326
    log .debug ("Oil Processed")#line:327
    oil_processed_amount =oil_processed_amount +1 #line:328
    if oil_processed_amount >=65000 :#line:329
        PLCSetTag (PLC_OIL_PROCESSED ,65000 )#line:330
        PLCSetTag (PLC_OIL_UPPER ,oil_processed_amount -65000 )#line:331
    else :#line:332
        PLCSetTag (PLC_OIL_PROCESSED ,oil_processed_amount )#line:333
    return False #line:334
def sep_open (O0OOO000OOO000O0O ,OOO0OOO000OOOOO00 ,*O0O0OO0OO00000000 ,**OO000000O0O0O0OO0 ):#line:337
    log .debug ("Begin separation")#line:338
    return False #line:339
def sep_closed (OOOO0OOOOOO0OO0OO ,OO000OOOOO0O00OO0 ,*O0O0O0000OOOO0OOO ,**O0OOOOO00000O00OO ):#line:342
    log .debug ("Stop separation")#line:343
    return True #line:344
def outlet_valve_open (OO0OOO000O0OOO0OO ,OO000O000OOOOOO0O ,*OO000OO000O0OO000 ,**O000O00OOOO00O00O ):#line:346
    log .debug ("Outlet valve open")#line:347
    return False #line:348
def outlet_valve_closed (O0OOOOOOOO0000000 ,OO00O00000O00OO0O ,*OO00O0OOOOO00OOO0 ,**OOOO0OOOO0OO0000O ):#line:350
    log .debug ("Outlet valve close")#line:351
    return True #line:352
def waste_valve_open (O0OO0O00000OO000O ,OOO0O0O00O0O0OO0O ,*O0O0OO0O0OO00OO0O ,**O0O000OOOOOOOOOO0 ):#line:354
    log .debug ("Waste valve open")#line:355
    return False #line:356
def waste_valve_closed (OO00O000O00O0OO00 ,O0OO0O0OO000O0O00 ,*OO0OO0O0000000000 ,**OOOO0OO0OOOO00OOO ):#line:358
    log .debug ("Waste valve close")#line:359
    return True #line:360
def run_world ():#line:362
    pygame .init ()#line:363
    OOOO00OOO00O0OOO0 =pygame .display .set_mode ((SCREEN_WIDTH ,SCREEN_HEIGHT ))#line:364
    pygame .display .set_caption ("Crude Oil Pretreatment Unit")#line:365
    O00000000OO00OOO0 =pygame .time .Clock ()#line:366
    O0OO0O00O00O0OOOO =True #line:367
    OOOO000OO00O0OOOO =pymunk .Space ()#line:371
    OOOO000OO00O0OOOO .gravity =(0.0 ,-900.0 )#line:372
    OOOO000OO00O0OOOO .add_collision_handler (tank_level_collision ,ball_collision ,begin =level_reached )#line:375
    OOOO000OO00O0OOOO .add_collision_handler (oil_spill_collision ,ball_collision ,begin =oil_spilled )#line:377
    OOOO000OO00O0OOOO .add_collision_handler (oil_processed_collision ,ball_collision ,begin =oil_processed )#line:379
    OOOO000OO00O0OOOO .add_collision_handler (outlet_valve_collision ,ball_collision ,begin =no_collision )#line:381
    OOOO000OO00O0OOOO .add_collision_handler (sep_valve_collision ,ball_collision ,begin =no_collision )#line:383
    OOOO000OO00O0OOOO .add_collision_handler (waste_valve_collision ,ball_collision ,begin =no_collision )#line:385
    OO00OOOOOOO0O000O =add_pump (OOOO000OO00O0OOOO )#line:388
    O0000000O000OO0OO =add_oil_unit (OOOO000OO00O0OOOO )#line:389
    OO0OO00O0OOO0O0OO =tank_level_sensor (OOOO000OO00O0OOOO )#line:390
    O0OOO0O000OOO000O =sep_valve (OOOO000OO00O0OOOO )#line:391
    O0O0OOO0000O00000 =oil_spill_sensor (OOOO000OO00O0OOOO )#line:392
    OOOO0OO0O0O0O0000 =oil_processed_sensor (OOOO000OO00O0OOOO )#line:393
    OO0O0O00000O0O0O0 =outlet_valve (OOOO000OO00O0OOOO )#line:394
    O0O000O00OOOOOO00 =waste_valve (OOOO000OO00O0OOOO )#line:395
    OOOO0000O0OO0OOOO =[]#line:398
    OO00000O000000O0O =1 #line:399
    OO0O0O0O0OOO00O0O =pygame .font .SysFont (None ,40 )#line:402
    O0O0O0OO0OO00OOOO =pygame .font .SysFont (None ,26 )#line:403
    O0O0OOO000O00O0OO =pygame .font .SysFont (None ,18 )#line:404
    while O0OO0O00O00O0OOOO :#line:406
        O00000000OO00OOO0 .tick (FPS )#line:408
        for OOO00O000OO0OOOO0 in pygame .event .get ():#line:410
            if OOO00O000OO0OOOO0 .type ==QUIT :#line:411
                O0OO0O00O00O0OOOO =False #line:412
            elif OOO00O000OO0OOOO0 .type ==KEYDOWN and OOO00O000OO0OOOO0 .key ==K_ESCAPE :#line:413
                O0OO0O00O00O0OOOO =False #line:414
        OOO00000OOO00OO0O =pygame .image .load ("background.png")#line:417
        OOOO00OOO00O0OOO0 .fill (THECOLORS ["grey"])#line:419
        if PLCGetTag (PLC_FEED_PUMP )==1 :#line:422
            if (PLCGetTag (PLC_TANK_LEVEL )==1 ):#line:425
                PLCSetTag (PLC_FEED_PUMP ,0 )#line:426
        if PLCGetTag (PLC_OUTLET_VALVE )==1 :#line:429
            OOOO000OO00O0OOOO .add_collision_handler (outlet_valve_collision ,ball_collision ,begin =outlet_valve_open )#line:430
        elif PLCGetTag (PLC_OUTLET_VALVE )==0 :#line:431
            OOOO000OO00O0OOOO .add_collision_handler (outlet_valve_collision ,ball_collision ,begin =outlet_valve_closed )#line:432
        if PLCGetTag (PLC_SEP_VALVE )==1 :#line:435
            OOOO000OO00O0OOOO .add_collision_handler (sep_valve_collision ,ball_collision ,begin =sep_open )#line:436
        else :#line:437
            OOOO000OO00O0OOOO .add_collision_handler (sep_valve_collision ,ball_collision ,begin =sep_closed )#line:438
        if PLCGetTag (PLC_WASTE_VALVE )==1 :#line:441
            OOOO000OO00O0OOOO .add_collision_handler (waste_valve_collision ,ball_collision ,begin =waste_valve_open )#line:442
        else :#line:443
            OOOO000OO00O0OOOO .add_collision_handler (waste_valve_collision ,ball_collision ,begin =waste_valve_closed )#line:444
        OO00000O000000O0O -=1 #line:447
        if OO00000O000000O0O <=0 and PLCGetTag (PLC_FEED_PUMP )==1 :#line:449
            OO00000O000000O0O =1 #line:450
            OOO0O00O0O0OOOO00 =add_ball (OOOO000OO00O0OOOO )#line:451
            OOOO0000O0OO0OOOO .append (OOO0O00O0O0OOOO00 )#line:452
        O0O0O00000O0O000O =[]#line:454
        for OO00O0OO0OO0000O0 in OOOO0000O0OO0OOOO :#line:455
            if OO00O0OO0OO0000O0 .body .position .y <0 or OO00O0OO0OO0000O0 .body .position .x >SCREEN_WIDTH +150 :#line:456
                O0O0O00000O0O000O .append (OO00O0OO0OO0000O0 )#line:457
            draw_ball (OOO00000OOO00OO0O ,OO00O0OO0OO0000O0 )#line:459
        for OO00O0OO0OO0000O0 in O0O0O00000O0O000O :#line:461
            OOOO000OO00O0OOOO .remove (OO00O0OO0OO0000O0 ,OO00O0OO0OO0000O0 .body )#line:462
            OOOO0000O0OO0OOOO .remove (OO00O0OO0OO0000O0 )#line:463
        draw_polygon (OOO00000OOO00OO0O ,OO00OOOOOOO0O000O )#line:465
        draw_lines (OOO00000OOO00OO0O ,O0000000O000OO0OO )#line:466
        draw_ball (OOO00000OOO00OO0O ,OO0OO00O0OOO0O0OO ,THECOLORS ['black'])#line:467
        draw_line (OOO00000OOO00OO0O ,O0OOO0O000OOO000O )#line:468
        draw_line (OOO00000OOO00OO0O ,OO0O0O00000O0O0O0 )#line:469
        draw_line (OOO00000OOO00OO0O ,O0O000O00OOOOOO00 )#line:470
        draw_line (OOO00000OOO00OO0O ,O0O0OOO0000O00000 ,THECOLORS ['red'])#line:471
        draw_line (OOO00000OOO00OO0O ,OOOO0OO0O0O0O0000 ,THECOLORS ['red'])#line:472
        O0OO0O00OO0O0OO0O =O0O0O0OO0OO00OOOO .render (str ("Crude Oil Pretreatment Unit"),1 ,THECOLORS ['blue'])#line:475
        OOOO00O0OO0OOO0OO =OO0O0O0O0OOO00O0O .render (str ("VirtuaPlant"),1 ,THECOLORS ['gray20'])#line:476
        O0O0OOOO0O0000OOO =O0O0OOO000O00O0OO .render (str ("(press ESC to quit)"),1 ,THECOLORS ['gray'])#line:477
        OO00000O0OOO00OOO =O0O0O0OO0OO00OOOO .render (str ("Feed Pump"),1 ,THECOLORS ['blue'])#line:478
        O00O00OO00OOO0O00 =O0O0O0OO0OO00OOOO .render (str ("Oil Storage Unit"),1 ,THECOLORS ['blue'])#line:479
        OO0000000OO0O0000 =O0O0O0OO0OO00OOOO .render (str ("Separator Vessel"),1 ,THECOLORS ['blue'])#line:480
        OOOOO00000OOOOO0O =O0O0O0OO0OO00OOOO .render (str ("Waste Water Treatment Unit"),1 ,THECOLORS ['blue'])#line:481
        OO0O00OO0OO0O00OO =O0O0OOO000O00O0OO .render (str ("Tank Level Sensor"),1 ,THECOLORS ['blue'])#line:482
        OOO0O000O0OOOO00O =O0O0OOO000O00O0OO .render (str ("Separator Vessel Valve"),1 ,THECOLORS ['blue'])#line:483
        OO0O0OO0O0O00OO00 =O0O0OOO000O00O0OO .render (str ("Waste Water Valve"),1 ,THECOLORS ['blue'])#line:484
        O0OOOO00O0000O0OO =O0O0OOO000O00O0OO .render (str ("Outlet Valve"),1 ,THECOLORS ['blue'])#line:485
        OOO00000OOO00OO0O .blit (O0OO0O00OO0O0OO0O ,(300 ,40 ))#line:487
        OOO00000OOO00OO0O .blit (OOOO00O0OO0OOO0OO ,(347 ,10 ))#line:488
        OOO00000OOO00OO0O .blit (O0O0OOOO0O0000OOO ,(SCREEN_WIDTH -115 ,0 ))#line:489
        OOO00000OOO00OO0O .blit (OO00000O0OOO00OOO ,(80 ,0 ))#line:490
        OOO00000OOO00OO0O .blit (O00O00OO00OOO0O00 ,(125 ,100 ))#line:491
        OOO00000OOO00OO0O .blit (OO0000000OO0O0000 ,(385 ,275 ))#line:492
        OOOO00OOO00O0OOO0 .blit (OOOOO00000OOOOO0O ,(265 ,490 ))#line:493
        OOO00000OOO00OO0O .blit (OO0O00OO0OO0O00OO ,(125 ,50 ))#line:494
        OOO00000OOO00OO0O .blit (O0OOOO00O0000O0OO ,(90 ,195 ))#line:495
        OOO00000OOO00OO0O .blit (OOO0O000O0OOOO00O ,(350 ,375 ))#line:496
        OOO00000OOO00OO0O .blit (OO0O0OO0O0O00OO00 ,(90 ,375 ))#line:497
        OOOO00OOO00O0OOO0 .blit (OOO00000OOO00OO0O ,(0 ,0 ))#line:498
        OOOO000OO00O0OOOO .step (1 /FPS )#line:500
        pygame .display .flip ()#line:501
    if reactor .running :#line:503
        reactor .callFromThread (reactor .stop )#line:504
store =ModbusSlaveContext (di =ModbusSequentialDataBlock (0 ,[0 ]*100 ),co =ModbusSequentialDataBlock (0 ,[0 ]*100 ),hr =ModbusSequentialDataBlock (0 ,[0 ]*100 ),ir =ModbusSequentialDataBlock (0 ,[0 ]*100 ))#line:510
context =ModbusServerContext (slaves =store ,single =True )#line:512
identity =ModbusDeviceIdentification ()#line:515
identity .VendorName ='Simmons Oil Refining Platform'#line:516
identity .ProductCode ='SORP'#line:517
identity .VendorUrl ='http://simmons.com/markets/oil-gas/pages/refining-industry.html'#line:518
identity .ProductName ='SORP 3850'#line:519
identity .ModelName ='Simmons ORP 3850'#line:520
identity .MajorMinorRevision ='2.09.01'#line:521
def startModbusServer ():#line:523
    StartTcpServer (context ,identity =identity ,address =(get_ip (),MODBUS_SERVER_PORT ))#line:526
def main ():#line:528
    reactor .callInThread (run_world )#line:529
    startModbusServer ()#line:530
if __name__ =='__main__':#line:532
    sys .exit (main ())#line:533
