import numpy as np
import pandas as pd

runExpectancy = pd.read_csv('Plate Discipline/runExpectancy.csv')
pTake = pd.read_csv('Plate Discipline/pTake.csv')
pSwing = pd.read_csv('Plate Discipline/pSwing.csv')
strikes_0 = pd.read_csv('Plate Discipline/zero_strike.csv')
strikes_1 = pd.read_csv('Plate Discipline/one_strike.csv')
strikes_2 = pd.read_csv('Plate Discipline/two_strike.csv')
decisionProb = pd.read_csv('Plate Discipline/decisionProbability.csv')

strikes_dict = {
    0: strikes_0,
    1: strikes_1,
    2: strikes_2
}

Type = 'Breaking'
Location = 'Waste'
Outs = 1
Runners = '-- 2 --'
Balls = 2
Strikes = 2
Count = f"{Balls}-{Strikes}"

def get_run_expectancy(runExpectancy, Outs, Runners, Balls, Strikes):
    Count = f"{Balls}-{Strikes}"
    runExpectancy['Outs'] = runExpectancy['Outs'].astype(int)
    matrix = runExpectancy[
        (runExpectancy['Outs'] == Outs) &
        (runExpectancy['Runners'] == Runners)
    ]

    if not matrix.empty:
        ERV = matrix[Count].iloc[0]
        return float(ERV)
    else:
        print("Invalid input.")

def get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes):
    if Strikes in strikes_dict:
        strikes_n = strikes_dict[Strikes]
        strikes_n['Outs'] = strikes_n['Outs'].astype(int)
        strikes_n.rename(columns={'0': 0, '1': 1, '2': 2, '3': 3}, inplace=True)

        # Filter the DataFrame based on Outs and Runners
        matrix = strikes_n[
            (strikes_n['Outs'] == Outs) &
            (strikes_n['Runners'] == Runners)
        ]

        # Check if a valid row exists
        if not matrix.empty:
                ERV = matrix[Balls].iloc[0]
                return (float(ERV))

def get_pTake(pTake, Type, Location, Output):
    matrix = pTake[
        (pTake['Pitch Type'] == Type) &
        (pTake['Location'] == Location)
    ]

    if not matrix.empty:
        ERV = matrix[Output].iloc[0]
        return float(ERV)
    else:
        print("Invalid input.")

def get_pSwing(pSwing, Type, Location, Output):
    matrix = pSwing[
        (pSwing['Pitch Type'] == Type) &
        (pSwing['Location'] == Location)
    ]

    if not matrix.empty:
        ERV = matrix[Output].iloc[0]
        return float(ERV)
    else:
        print("Invalid input.")

def get_decisionProb(decisionProb, Type, Location, Output):
    matrix = decisionProb[
        (decisionProb['Pitch Type'] == Type) &
        (decisionProb['Location'] == Location)
    ]

    if not matrix.empty:
        ERV = matrix[Output].iloc[0]
        return float(ERV)
    else:
        print("Invalid input.")

def calculate_ball(Type, Location, Outs, Runners, Balls, Strikes):
    Balls += 1
    addRuns = 0
    if (Balls == 4):
        if (Runners == '-- -- --'):
            Runners = '1 -- --'
        elif (Runners == '1 -- --'):
            Runners = '1 2 --'
        elif (Runners == '-- 2 --'):
            Runners = '1 2 --'
        elif (Runners == '-- -- 3'):
            Runners = '1 -- 3'
        elif (Runners == '1 2 --'):
            Runners = '1 2 3'
        elif (Runners == '1 -- 3'):
            Runners = '1 2 3'
        elif (Runners == '-- 2 3'):
            Runners = '1 2 3'
        elif (Runners == '1 2 3'):
            addRuns += 1
        Balls = 0
        Strikes = 0
    p = get_pTake(pTake, Type, Location, 'Ball')
    RE = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
    # print(f"Ball: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
    # print(f"P(Ball) = {p} ; RE(Ball) = {RE}")
    ERV = p * RE
    return ERV

def calculate_strike(Type, Location, Outs, Runners, Balls, Strikes):
    Strikes += 1
    if (Strikes == 3):
        Outs += 1
        if (Outs < 3):
            Balls = 0
            Strikes = 0
        if (Outs == 3):
            return 0
    p = get_pTake(pTake, Type, Location, 'Strike')
    RE = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes)
    # print(f"Strike: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
    # print(f"P(Strike) = {p} ; RE(Strike) = {RE}")
    ERV = p * RE
    return ERV

def calculate_miss(Type, Location, Outs, Runners, Balls, Strikes):
    Strikes += 1
    if (Strikes == 3):
        Outs += 1
        if (Outs < 3):
            Balls = 0
            Strikes = 0
        if (Outs == 3):
            return 0
    p = get_pSwing(pSwing, Type, Location, 'Miss')
    RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes)
    # print(f"Miss: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
    # print(f"P(Miss) = {p} ; RV(Miss) = {RV}")
    ERV = p * RV
    return ERV

def calculate_foul(Type, Location, Outs, Runners, Balls, Strikes):
    if (Strikes != 2):
        Strikes += 1
    p = get_pSwing(pSwing, Type, Location, 'Foul')
    RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes)
    # print(f"Foul: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
    # print(f"P(Foul) = {p} ; RV(Foul) = {RV}")
    ERV = p * RV
    return ERV

def calculate_out(Type, Location, Outs, Runners, Balls, Strikes):
    addRuns = 0
    Outs += 1
    if (Outs == 3):
        return 0
    Balls = 0
    Strikes = 0
    if (Runners == '-- -- --'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        # print(f"Out In-Play: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV(Out) = {RV}")
        ERV = p * RV
        return ERV
    elif (Runners == '1 -- --'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '1 -- --'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.99
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- -- --'
        Outs += 1
        if Outs == 3:
            RV_2 = 0
        else:
            RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.01
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '-- 2 --'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '-- -- 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.4  #estimated
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- 2 --'
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.6  #estimated
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '-- -- 3'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '-- -- 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.75  #estimated
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- -- --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.25  #estimated
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '1 2 --'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '1 2 --' 
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.44 #estimate
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- 3'
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.44 #estimate
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- -- 3'
        Outs += 1
        if Outs == 3:
            RV_3 = 0
        else:
            RV_3 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_3 = 0.02 #estimate
        # print(f"Out In-Play 3: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2} ; RV_3(Out) = {RV_3}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2) + (RV_3*p_3))
        return ERV
    elif (Runners == '1 -- 3'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '1 -- 3' 
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.69 #estimate
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.30 #estimate
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- -- --'
        Outs += 1
        if Outs == 3:
            RV_3 = 0
        else:
            RV_3 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_3 = 0.01 #estimate
        # print(f"Out In-Play 3: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2} ; RV_3(Out) = {RV_3}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2) + (RV_3*p_3))
        return ERV
    elif (Runners == '-- 2 3'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '-- 2 3' 
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.48 #estimate
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- 2 --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.48 #estimate
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- -- 3'
        RV_3 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_3 = 0.04 #estimate
        # print(f"Out In-Play 3: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2} ; RV_3(Out) = {RV_3}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2) + (RV_3*p_3))
        return ERV
    elif (Runners == '1 2 3'):
        p = get_pSwing(pSwing, Type, Location, 'Out In-Play')
        Runners = '1 2 3' 
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.69 #estimate
        # print(f"Out In-Play 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 2 --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.30 #estimate
        # print(f"Out In-Play 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- -- 3'
        Outs += 1
        if Outs == 3:
            RV_3 = 0
        else:
            RV_3 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_3 = 0.01 #estimate
        # print(f"Out In-Play 3: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Out) = {p} ; RV_1(Out) = {RV_1} ; RV_2(Out) = {RV_2} ; RV_3(Out) = {RV_3}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2) + (RV_3*p_3))
        return ERV

def calculate_single(Type, Location, Outs, Runners, Balls, Strikes):
    Balls = 0
    Strikes = 0
    addRuns = 0
    if (Runners == '-- -- --'):
        Runners = '1 -- --'
        p = get_pSwing(pSwing, Type, Location, 'Single')
        RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        # print(f"Single: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV(Single) = {RV}")
        ERV = p * RV
        return ERV
    elif (Runners == '1 -- --'):
        p = get_pSwing(pSwing, Type, Location, 'Single')
        Runners = '1 2 --'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.7
        # print(f"Single 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- 3'
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.3
        # print(f"Single 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV_1(Single) = {RV_1} ; RV_2(Single) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '-- 2 --'):
        p = get_pSwing(pSwing, Type, Location, 'Single')
        Runners = '1 -- 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.4
        # print(f"Single 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.6
        # print(f"Single 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV_1(Single) = {RV_1} ; RV_2(Single) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '-- -- 3'):
        Runners = '1 -- --'
        addRuns += 1
        p = get_pSwing(pSwing, Type, Location, 'Single')
        RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        # print(f"Single: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV(Single) = {RV}")
        ERV = p * RV
        return ERV
    elif (Runners == '1 2 --'):
        p = get_pSwing(pSwing, Type, Location, 'Single')
        Runners = '1 2 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.4
        # print(f"Single 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 2 --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.3
        # print(f"Single 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- 3'
        RV_3 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_3 = 0.3
        # print(f"Single 3: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV_1(Single) = {RV_1} ; RV_2(Single) = {RV_2} ; RV_3(Single) = {RV_3}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2) + (RV_3*p_3))
        return ERV
    elif (Runners == '1 -- 3'):
        addRuns += 1
        p = get_pSwing(pSwing, Type, Location, 'Single')
        Runners = '1 2 --'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.7
        # print(f"Single 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- 3'
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.3
        # print(f"Single 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV_1(Single) = {RV_1} ; RV_2(Single) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '-- 2 3'):
        addRuns += 1
        p = get_pSwing(pSwing, Type, Location, 'Single')
        Runners = '1 -- 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.4
        # print(f"Single 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.6
        # print(f"Single 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV_1(Single) = {RV_1} ; RV_2(Single) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '1 2 3'):
        addRuns += 1
        p = get_pSwing(pSwing, Type, Location, 'Single')
        Runners = '1 2 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.4
        # print(f"Single 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 2 --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.3
        # print(f"Single 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '1 -- 3'
        RV_3 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_3 = 0.3
        # print(f"Single 3: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Single) = {p} ; RV_1(Single) = {RV_1} ; RV_2(Single) = {RV_2} ; RV_3(Single) = {RV_3}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2) + (RV_3*p_3))
        return ERV
    
def calculate_double(Type, Location, Outs, Runners, Balls, Strikes):
    Balls = 0
    Strikes = 0
    addRuns = 0
    if (Runners == '-- -- --') or (Runners == '-- 2 --') or (Runners == '-- -- 3') or (Runners == '-- 2 3'):
        Runners = '-- 2 --'
        if (Runners == '-- 2 --') or (Runners == '-- -- 3'):
            addRuns += 1
        elif (Runners == '-- 2 3'):
            addRuns += 2
        p = get_pSwing(pSwing, Type, Location, 'Double')
        RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        # print(f"Double: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Double) = {p} ; RV(Double) = {RV}")
        ERV = p * RV
        return ERV
    elif (Runners == '1 -- --'):
        p = get_pSwing(pSwing, Type, Location, 'Double')
        Runners = '-- 2 3'
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.6
        # print(f"Double 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- 2 --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.4
        # print(f"Double 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Double) = {p} ; RV_1(Double) = {RV_1} ; RV_2(Double) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '1 2 --') or (Runners == '1 -- 3'):
        p = get_pSwing(pSwing, Type, Location, 'Double')
        Runners = '-- 2 3'
        addRuns += 1
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.6
        # print(f"Double 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- 2 --'
        addRuns += 1
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.4
        # print(f"Double 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Double) = {p} ; RV_1(Double) = {RV_1} ; RV_2(Double) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV
    elif (Runners == '1 2 3'):
        p = get_pSwing(pSwing, Type, Location, 'Double')
        Runners = '-- 2 3'
        addRuns += 2
        RV_1 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_1 = 0.6
        # print(f"Double 1: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        Runners = '-- 2 --'
        addRuns += 3
        RV_2 = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
        p_2 = 0.4
        # print(f"Double 2: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
        # print(f"P(Double) = {p} ; RV_1(Double) = {RV_1} ; RV_2(Double) = {RV_2}")
        ERV = p * ((RV_1*p_1) + (RV_2*p_2))
        return ERV

def calculate_triple(Type, Location, Outs, Runners, Balls, Strikes):
    addRuns = 0
    if (Runners == '1 -- --') or (Runners == '-- 2 --') or (Runners == '-- -- 3'):
        addRuns += 1
    elif (Runners == '1 2 --') or (Runners == '1 -- 3') or (Runners == '-- 2 3'):
        addRuns += 2
    elif (Runners == '1 2 3'):
        addRuns += 3
    Balls = 0
    Strikes = 0
    Runners = '-- -- 3'
    p = get_pSwing(pSwing, Type, Location, 'Triple')
    RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
    # print(f"Triple: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
    # print(f"P(Triple) = {p} ; RV(Triple) = {RV}")
    ERV = p * RV
    return ERV

def calculate_homerun(Type, Location, Outs, Runners, Balls, Strikes):
    addRuns = 1
    if (Runners == '1 -- --') or (Runners == '-- 2 --') or (Runners == '-- -- 3'):
        addRuns += 1
    elif (Runners == '1 2 --') or (Runners == '1 -- 3') or (Runners == '-- 2 3'):
        addRuns += 2
    elif (Runners == '1 2 3'):
        addRuns += 3
    Balls = 0
    Strikes = 0
    Runners = '-- -- --'
    p = get_pSwing(pSwing, Type, Location, 'Homerun')
    RV = get_RE_strikes(strikes_dict, Outs, Runners, Balls, Strikes) + addRuns
    # print(f"Homerun: {Balls}-{Strikes} {Outs} outs, '{Runners}'")
    # print(f"P(Homerun) = {p} ; RV(Homerun) = {RV}")
    ERV = p * RV
    return ERV

def calculate_take_ERV(Type, Location, Outs, Runners, Balls, Strikes):
    return (calculate_ball(Type, Location, Outs, Runners, Balls, Strikes) + calculate_strike(Type, Location, Outs, Runners, Balls, Strikes))

def calculate_swing_ERV(Type, Location, Outs, Runners, Balls, Strikes):
    return (calculate_miss(Type, Location, Outs, Runners, Balls, Strikes) + calculate_foul(Type, Location, Outs, Runners, Balls, Strikes) + calculate_out(Type, Location, Outs, Runners, Balls, Strikes) + calculate_single(Type, Location, Outs, Runners, Balls, Strikes) + calculate_double(Type, Location, Outs, Runners, Balls, Strikes) + calculate_triple(Type, Location, Outs, Runners, Balls, Strikes) + calculate_homerun(Type, Location, Outs, Runners, Balls, Strikes))

def calculate_ERV_given_pitch(Type, Location, Outs, Runners, Balls, Strikes):
    take_portion = calculate_take_ERV(Type, Location, Outs, Runners, Balls, Strikes) * get_decisionProb(decisionProb, Type, Location, 'Take')
    swing_portion = calculate_swing_ERV(Type, Location, Outs, Runners, Balls, Strikes) * get_decisionProb(decisionProb, Type, Location, 'Swing')
    ERV = take_portion + swing_portion
    return ERV

print(f"Situation:\n{Count} {Outs} out(s), '{Runners}'\nPitch: {Location} {Type}\n")
print(f"Expected Run Value BEFORE the pitch: {get_run_expectancy(runExpectancy, Outs, Runners, Balls, Strikes)}\n")

print(f"Expected Run Value AFTER pitch, but BEFORE decision: {calculate_ERV_given_pitch(Type, Location, Outs, Runners, Balls, Strikes)}\n")

take_result = calculate_take_ERV(Type, Location, Outs, Runners, Balls, Strikes)
swing_result = calculate_swing_ERV(Type, Location, Outs, Runners, Balls, Strikes)

print(f"ERV(Take): {take_result}")
print(f"ERV(Swing): {swing_result}")