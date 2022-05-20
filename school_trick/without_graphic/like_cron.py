#!/usr/bin/env python3

from datetime import datetime

time_8_0_done =False
time_8_30_done =False
time_9_15_done =False
time_9_45_done =False
time_10_30_done =False
time_11_0_done =False
time_11_45_done =False
time_12_15_done =False


while 1:
    time = datetime.today().time()

    if not time_8_0_done:
        if time.hour == 8 and time.minute == 0:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_8_0_done = True
            print(f'i runned script at {time.hour + time.minute}')

    if not time_8_30_done:
        if time.hour == 8 and time.minute == 30:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_8_30_done = True
            print(f'i runned script at {time.hour + time.minute}')

    if not time_9_15_done:
        if time.hour == 9 and time.minute == 15:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_9_15_done = True
            print(f'i runned script at {time.hour + time.minute}')

    if not time_9_45_done:
        if time.hour == 9 and time.minute == 45:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_9_45_done = True
            print(f'i runned script at {time.hour + time.minute}')
  
    if not time_10_30_done:
        if time.hour == 10 and time.minute == 30:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_10_30_done = True
            print(f'i runned script at {time.hour + time.minute}')

    if not time_11_0_done:
        if time.hour == 11 and time.minute == 0:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_11_0_done = True
            print(f'i runned script at {time.hour + time.minute}')

    if not time_11_45_done:
        if time.hour == 11 and time.minute == 45:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_11_45_done = True
            print(f'i runned script at {time.hour + time.minute}')

    if not time_12_15_done:
        if time.hour == 12 and time.minute == 15:
            exec(
                open("/home/me/python_programs/funy_things/school_trick/without_graphic/school_trick.py").read()
            )
            time_12_15_done = True
            print(f'i runned script at {time.hour}:{time.minute}')

    

    if time.hour == 0 and time.minute == 0:
        time_8_0_done =False
        time_8_30_done =False
        time_9_15_done =False
        time_9_45_done =False
        time_10_30_done =False
        time_11_0_done =False
        time_11_45_done =False
        time_12_15_done =False        

