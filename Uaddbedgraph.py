#needs sorted files
#adds bedgraph files

import os
import csv

def add (input1, input2, newfile):
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
                    print(current_chromosome)
                    done = "no"
                    break
            if done == "yes":
                break

            ctrl_chr_data = []
            for line in ctrl:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] == current_chromosome:
                    ctrl_chr_data.append(line_split)
        with open(input2) as treat:
            treat_chr_data = []
            for line in treat:
                line_split = line.split("\t")
                line_split[3] = line_split[3].replace("\n", "")
                if line_split[0] == current_chromosome:
                    treat_chr_data.append(line_split)

        i = 0
        output_temp = []
        while len(ctrl_chr_data) != 0 and len(treat_chr_data) != 0:
            i = i + 1  # base nr, check if list at end
            # get values for base nr
            ctrlvalue = 0
            if len(ctrl_chr_data) > 0:
                if int(ctrl_chr_data[0][2]) < i:
                    ctrl_chr_data.pop(0)
                if len(ctrl_chr_data) > 0:
                    if i >= int(ctrl_chr_data[0][1]):
                        if i <= int(ctrl_chr_data[0][2]):
                            ctrlvalue = float(ctrl_chr_data[0][3])

            treatvalue = 0
            if len(treat_chr_data) > 0:
                if int(treat_chr_data[0][2]) < i:
                    treat_chr_data.pop(0)
                if len(treat_chr_data) > 0:
                    if i >= int(treat_chr_data[0][1]):
                        if i <= int(treat_chr_data[0][2]):
                            treatvalue = float(treat_chr_data[0][3])

            # add to output list
            if ctrlvalue != 0 or treatvalue != 0:
                        if len(output_temp) == 0:
                            temp = []
                            temp.append(str(current_chromosome))
                            temp.append(i)
                            temp.append(i + 1)
                            temp.append(ctrlvalue + treatvalue)
                            output_temp.append(temp)

                        else:
                            if output_temp[-1][2] == i:
                                if output_temp[-1][3] == ctrlvalue + treatvalue:
                                    output_temp[-1][2] = i + 1
                            else:
                                output.append(output_temp[0])
                                output_temp = []
                                temp = []
                                temp.append(str(current_chromosome))
                                temp.append(i)
                                temp.append(i + 1)
                                temp.append(ctrlvalue + treatvalue)
                                output_temp.append(temp)

        if len(output_temp) > 0:
            output.append(output_temp[0])

        with open(newfile, "a") as f:
            for row in output:
                f.write(str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\n")




#_______________________________________


add("3.bedgraph", "4.bedgraph", "34.txt")
add("5.bedgraph", "6.bedgraph", "56.txt")
add("7.bedgraph", "8.bedgraph", "78.txt")
add("9.bedgraph", "10.bedgraph", "910.txt")

add("34.txt", "56.txt", "3456.txt")
add("78.txt", "910.txt", "78910.txt")

add("3456.txt", "78910.txt", "345678910.txt")
add("345678910.txt", "2.bedgraph", "final.txt")