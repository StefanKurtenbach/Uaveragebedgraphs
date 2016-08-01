#needs sorted files
#adds bedgraph files

import os
import csv

def add (input1, input2, newfile):
    buffer_size = 100000
    chromosomes_done = []
    done = "no"
    while done == "no":
        output_ctl = []
        output_treatment = []
        output = []

        # make list of single chromosome
        with open(input1) as ctrl:
            current_chromosome = ""
            done = "yes"
            for line in ctrl:
                line_split = line.split("\t")  # check if there is a more efficient way to import
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] not in chromosomes_done:
                    chromosomes_done.append(line_split[0])
                    current_chromosome = line_split[0]
                    print(newfile + ": " + current_chromosome)
                    done = "no"
                    break
            if done == "yes":
                break

        with open(input1) as ctrl:
            ctrl_chr_data = []
            for line in ctrl:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] == current_chromosome:
                    ctrl_chr_data.append(line_split)
                if len(ctrl_chr_data) == buffer_size: break
        with open(input2) as treat:
            treat_chr_data = []
            for line in treat:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] == current_chromosome:
                    treat_chr_data.append(line_split)
                if len(treat_chr_data) == buffer_size: break

        i = -1
        output_temp = []
        while len(ctrl_chr_data) != 0 or len(treat_chr_data) != 0:
            i = i + 1  # base nr
            ctrlvalue = 0
            if len(ctrl_chr_data) == 1:
                collectnext = "no"
                with open(input1) as ctrl:
                    for line in ctrl:
                        if len(ctrl_chr_data) == buffer_size: break
                        line_split = line.split("\t")
                        if collectnext == "yes" and current_chromosome != line_split[0]: break
                        line_split[3] = line_split[3].replace("\n", "")
                        if collectnext == "yes":
                            if line_split[0] == current_chromosome:
                                ctrl_chr_data.append(line_split)
                        elif ctrl_chr_data[0][0] == line_split[0]:
                            if ctrl_chr_data[0][1] == line_split[1]:
                                if ctrl_chr_data[0][2] == line_split[2]:
                                    if ctrl_chr_data[0][3] == line_split[3]:
                                        collectnext = "yes"

            if len(ctrl_chr_data) > 0:
                if int(ctrl_chr_data[0][2]) == i:
                    ctrl_chr_data.pop(0)
            if len(ctrl_chr_data) > 0:
                if i >= int(ctrl_chr_data[0][1]):
                    if i <= int(ctrl_chr_data[0][2]):
                        ctrlvalue = float(ctrl_chr_data[0][3])

            treatvalue = 0
            if len(treat_chr_data) == 1:
                collectnext = "no"
                with open(input2) as treat:
                    for line in treat:
                        if len(treat_chr_data) == buffer_size: break
                        line_split = line.split("\t")
                        if collectnext == "yes" and current_chromosome != line_split[0]: break
                        line_split[3] = line_split[3].replace("\n", "")
                        if collectnext == "yes":
                            if line_split[0] == current_chromosome:
                                treat_chr_data.append(line_split)
                        elif treat_chr_data[0][0] == line_split[0]:
                            if treat_chr_data[0][1] == line_split[1]:
                                if treat_chr_data[0][2] == line_split[2]:
                                    if treat_chr_data[0][3] == line_split[3]:
                                        collectnext = "yes"

            if len(treat_chr_data) > 0:
                if int(treat_chr_data[0][2]) == i:
                    treat_chr_data.pop(0)
            if len(treat_chr_data) > 0:
                if i >= int(treat_chr_data[0][1]):
                    if i <= int(treat_chr_data[0][2]):
                        treatvalue = float(treat_chr_data[0][3])

            # add to output list
            if ctrlvalue != 0 or treatvalue != 0:
                if len(output_temp) == 0:
                    output_temp = [str(current_chromosome), i, i+1, ctrlvalue + treatvalue]
                elif output_temp[2] == i:
                        if output_temp[3] == ctrlvalue + treatvalue:
                            output_temp[2] = i+1
                        else: #if not the same value
                            output_temp[2] = output_temp[2]
                            output.append(output_temp)
                            output_temp = [str(current_chromosome), i, i + 1, ctrlvalue + treatvalue]
                else:
                    output_temp[2] = output_temp[2]
                    output.append(output_temp)
                    output_temp = [str(current_chromosome), i, i + 1, ctrlvalue + treatvalue]

        if len(output_temp) > 0:
            output_temp[2] = output_temp[2]
            output.append(output_temp)

        with open(newfile, "a") as f:
            for row in output:
                f.write(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\n")




#Code to sum bedgraph files goes here_______________________________________


add("2.bedgraph", "3.bedgraph", "23.bedgraph") #example

# ... add more
