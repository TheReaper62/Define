import matplotlib.pyplot as plt

# row = []
col = ["Area","Function"]
vals = [
    ["Date and Time","TODAY"],
    ["Text","LEFT, LEN, MID, RIGHT"],
    ["Logical","AND, IF, NOT, OR"],
    ["Lookup","HLOOKUP, VLOOKUP"],
    ["Mathematical","CEILING.MATH, FLOOR.MATH, MOD, POWER, QUOTIENT, RAND, RANDBETWEEN, ROUND, SQRT, SUM, SUMIF"],
    ["Statistical","AVERAGE, COUNT, COUNTA, COUNTBLANK, COUNTIF, LARGE, MAX, MEDIAN, MIN, MODE.SNGL, SMALL"]
]
colour = "Salmon"
filename = "7155_1_1_2.png"
title = "List of 33 examinable functions"
width = 0.3

if True:
    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = ax.table(
        cellText = vals,
        # rowLabels = row,
        colLabels = col,
        # rowColours = [colour] * len(row),
        colColours = [colour] * len(col),
        colWidths=[0.3,1.5],
        cellLoc ='center',
        loc ='center')
    ax.set_title(title,
                 fontweight ="bold")

    plt.rc('font', size=20)
    plt.savefig(filename,bbox_inches='tight')
