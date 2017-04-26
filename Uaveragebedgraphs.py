#needs sorted files

import os
from array import *

def add (input, newfile):
    nr_files = len(input)
    done = "no"
    chromosomes_done = []
    while done == "no":
        output_ctl = []
        output_treatment = []
        output = []
        # get current chromosome
        with open(input[0]) as ctrl:
            current_chromosome = ""
            done = "yes"
            for line in ctrl:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] not in chromosomes_done:
                    chromosomes_done.append(line_split[0])
                    current_chromosome = line_split[0]
                    print("Current Chromosome: " + current_chromosome)
                    done = "no"
                    break
            if done == "yes":
                break
        start = 1000000000 #prelim values
        stop = 0
        # get start and stop for current chromosome
        for file in input:
            with open(file) as f:
                breakyn = "no"
                prime = "no"
                for line in f:
                    if breakyn == "yes": break
                    line_split = line.split("\t")
                    if line_split[0] == current_chromosome:
                        if prime == "no":
                            if int(line_split[1]) < start:
                                start = int(line_split[1])
                            prime = "yes"
                        elif prime == "yes":
                            stop_temp = int(line_split[2])
                    elif prime == "yes":
                        if line_split[0] != current_chromosome:
                            breakyn = "yes"
                if stop < stop_temp:
                        stop = stop_temp
        # make empty output lists (multiple to avoid memory errors)
        length = stop - start
        output_temp1 = []
        output_temp2 = []
        output_temp3 = []
        output_start = []
        output_stop = []
        output_value = []

        if length < 100000000:
            output_temp1 = array('f',[0]*length)
        elif length < 200000000:
                output_temp1 = array('f', [0] * 100000000)
                output_temp2 = array('f', [0] * (length - 100000000))
        elif length < 300000000:
            output_temp1 = array('f', [0] * 100000000)
            output_temp2 = array('f', [0] * 100000000)
            output_temp3 = array('f', [0] * (length - 200000000))

        #sum up
        for file in input:
            with open(file) as file2:
                breakyn = "no"
                for line in file2:
                    line_split = line.split("\t")
                    if line_split[0] == current_chromosome:
                        breakyn = "yes"
                        line_split[3] = line_split[3].replace("\n", "")
                        for o in range(int(line_split[2]) - int(line_split[1])):
                            coord = o + int(line_split[1]) - start
                            if coord < 100000000:
                                output_temp1[coord] = output_temp1[coord] + float(line_split[3])
                            elif coord < 200000000:
                                    output_temp2[coord - 100000000] = output_temp2[coord - 100000000] + float(line_split[3])
                            elif coord < 300000000:
                                output_temp3[coord - 200000000] = output_temp3[coord - 200000000] + float(line_split[3])
                    elif breakyn == "yes": break
        output_start = array('I',[0]*15000000)
        output_stop = array('I',[0]*15000000)
        output_value = array('f',[0]*15000000)
        next = "no"
        for l in range(length):
            if l < 100000000:
                if output_temp1[l] != 0:
                    if output_value[0] == 0:
                        output_start[0] = start
                        output_stop[0] = start + 1
                        output_value[0] = output_temp1[0]
                        position = 0 # filled positions in array
                    elif output_temp1[l] == output_value[position]:
                            output_stop[position] += 1
                    else:
                        position += 1
                        output_start[position] = start + l
                        output_stop[position] = start + l + 1
                        output_value[position] = output_temp1[l]
            elif l < 200000000:
                if output_temp2[l-100000000] != 0:
                    if output_temp2[l-100000000] == output_value[position]:
                        output_stop[position] += 1
                    else:
                        position += 1
                        output_start[position] = start + l
                        output_stop[position] = start + l + 1
                        output_value[position] = output_temp2[l-100000000]
            elif l < 300000000:
                if output_temp3[l-200000000] != 0:
                    if output_temp3[l-200000000] == output_value[position]:
                        output_stop[position] += 1
                    else:
                        position += 1
                        try:
                            output_start[position] = start + l
                            output_stop[position] = start + l + 1
                            output_value[position] = output_temp3[l-200000000]
                        except:
                            print("l: " + str(l))
                            print("position: " + str(position))

        with open(newfile, "a") as f:
            for x, row in enumerate(output_start):
                if output_value[x] > 0:
                    f.write(str(current_chromosome) + "\t" + str(row) + "\t" + str(output_stop[x]) + "\t" + str(output_value[x]/nr_files) + "\n")


############################################################################
input = ["2.bedgraph", "3.bedgraph","4.bedgraph", "5.bedgraph","6.bedgraph", "7.bedgraph","8.bedgraph", "9.bedgraph","13.bedgraph", "14.bedgraph", "1.bedgraph", "15.bedgraph"]
add(input, "testoutput.bedgraph")
