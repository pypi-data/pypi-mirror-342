import timeit
#------------------------------------------------------------------------------
def report(s=""): pass # print(s)
#-----------------------------------------------------------------------------------
# ICON Programming Language: (1st pass, attribute grammar generated)
#
#                       every write(5 > ((1 to 2) * (3 to 4)));
#-----------------------------------------------------------------------------------
def x5_start():         global x5_V;           x5_V = 5;            x5_succeed()
def x5_resume():                                                    x5_fail()
#-----------------------------------------------------------------------------------
def x1_start():         global x1_V;           x1_V = 1;            x1_succeed()
def x1_resume():                                                    x1_fail()
#-----------------------------------------------------------------------------------
def x2_start():         global x2_V;           x2_V = 2;            x2_succeed()
def x2_resume():                                                    x2_fail()
#-----------------------------------------------------------------------------------
def to1_start():                                                    x1_start()
def x1_fail():                                                      to1_fail()
def x2_fail():                                                      x1_resume()
def to1_code():
                        global to1_I, x2_V, to1_V
                        if to1_I > x2_V:                            x2_resume()
                        else: to1_V = to1_I;                        to1_succeed()
def to1_resume():       global to1_I;           to1_I = to1_I + 1;  to1_code()
def x1_succeed():                                                   x2_start()
def x2_succeed():       global to1_I, x1_V;     to1_I = x1_V;       to1_code()
#-----------------------------------------------------------------------------------
def x3_start():         global x3_V;            x3_V = 3;           x3_succeed()
def x3_resume():                                                    x3_fail()
#-----------------------------------------------------------------------------------
def x4_start():         global x4_V;            x4_V = 4;           x4_succeed()
def x4_resume():                                                    x4_fail()
#-----------------------------------------------------------------------------------
def to2_start():                                                    x3_start()
def x3_fail():                                                      to2_fail()
def x4_fail():                                                      x3_resume()
def to2_code():
                        global to2_I, x4_V, to2_V
                        if to2_I > x4_V:                            x4_resume()
                        else: to2_V = to2_I;                        to2_succeed()
def to2_resume():       global to2_I;           to2_I = to2_I + 1;  to2_code()
def x3_succeed():                                                   x4_start()
def x4_succeed():       global to2_I, x3_V;     to2_I = x3_V;       to2_code()
#-----------------------------------------------------------------------------------
def mult_start():                                                   to1_start()
def to1_fail():                                                     mult_fail()
def to2_fail():                                                     to1_resume()
def mult_resume():                                                  to2_resume()
def to1_succeed():                                                  to2_start()
def to2_succeed():
                        global mult_V, to1_V, to2_V
                        mult_V = to1_V * to2_V;                     mult_succeed()
#-----------------------------------------------------------------------------------
def greater_start():                                                x5_start()
def x5_fail():                                                      greater_fail()
def mult_fail():                                                    x5_resume()
def greater_resume():                                               mult_resume()
def x5_succeed():                                                   mult_start()
def mult_succeed():
                        global x5_V, mult_V, greater_V
                        if x5_V <= mult_V:                          mult_resume()
                        else: greater_V = mult_V;                   greater_succeed()
#-----------------------------------------------------------------------------------
def write1_start():                                                 greater_start()
def write1_resume():                                                greater_resume()
def greater_fail():                                                 write1_fail()
def greater_succeed():
                        global write_V, greater_V
                        write_V = greater_V
                        report(write_V);                            write1_succeed()
#-----------------------------------------------------------------------------------
# ICON Programming Language: (2nd pass, optimization)
#
#                       every write(5 > ((1 to 2) * (3 to 4)));
#-----------------------------------------------------------------------------------
def write2_start():     global to3_I;           to3_I = 1;          to3_code()
def to3_resume():       global to3_I;           to3_I = to3_I + 1;  to3_code()
def to3_code():
                        global to3_I, to4_I
                        if to3_I > 2:                               write2_fail()
                        else: to4_I = 3;                            to4_code()
def write2_resume():    global to4_I;           to4_I = to4_I + 1;  to4_code()
def to4_code():
                        global to4_I, mult_V, to3_I, greater_V
                        if to4_I > 4:                               to3_resume()
                        else:
                            mult_V = to3_I * to4_I
                            if 5 <= mult_V:                         write2_resume()
                            else:
                                greater_V = mult_V
                                report(greater_V);                  write2_succeed()
#-----------------------------------------------------------------------------------
def icon1():                                                        write1_start()
def write1_fail():      report("Failure.")                          # Yeah! UNWIND already.
def write1_succeed():   report("Success!");                         write1_resume()
def icon2():                                                        write2_start()
def write2_fail():      report("Failure.")                          # Yeah! UNWIND already.
def write2_succeed():   report("Success!");                         write2_resume()
#-----------------------------------------------------------------------------------
def main():
    if True:
        time1 = timeit.timeit(lambda: icon1(), number = 1_000_000, globals = globals());
        print(time1)
        time2 = timeit.timeit(lambda: icon2(), number = 1_000_000, globals = globals());
        print(time2)
    else:
        report()
        icon1()
        report()
        icon2()
#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
#-----------------------------------------------------------------------------------
