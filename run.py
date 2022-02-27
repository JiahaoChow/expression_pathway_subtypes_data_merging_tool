'''
This is a project to process pathway data, expression data and subtypes data.
The shared data in these three files will be selected and saved as csv files named with subtypes.
If you have two files of subtypes or two files of expression, please use the lines annotated.
'''

import pandas as pd

# pathway
pathway_path = 'data/all.txt'
# subtype
subtype_path = 'data/TCGA_OV_gene_expression_subtype.txt'
# subtype_path_2 = 'data/Molecular_subtype_classification.txt'

# expression
expression_path = 'data/AgilentG4502A_07_3.txt'
# expression_path_2 = 'data/G450_BRCA.csv'

# read pathway data and drop duplicates
P = pd.read_table(pathway_path, header=None)
print("reading pathway data, the size of the file is", P.shape)
P = P[0].drop_duplicates()
print('droping the duplicates, the size of the file after processing is', P.shape)

# read subtypes file
S = pd.read_table(subtype_path)
print("reading subtypes data, the size of the file is", S.shape)
# list all types of subtypes in 'types'
types = S['gene_expression_subtype'].value_counts().index
# split the gene into several types
type_list = []
for item in types:
    list = S[S["gene_expression_subtype"]==item].values
    type_list.append(list)
    print("subtype of \"{}\" has items of {}".format(item, list.size))

# read subtypes file
# S2 = pd.read_table(subtype_path_2)
# print("reading subtypes_2 data, the size of the file is", S2.shape)
# # list all types of subtypes in 'types'
# types2 = S2.iloc[:,1].value_counts().index
# # split the gene into several types
# type2_list = []
# for item in types2:
#     list = S2[S2.iloc[:, 1]==item].values
#     type2_list.append(list)
#     print("subtype of \"{}\" has items of {}".format(item, list.size))

# assert (0)
# read express data
E = pd.read_table(expression_path, index_col=0, header=0)
# E2 = pd.read_csv(expression_path_2, index_col=0, header=0).T
print("reading expression data, the size of the file is", E.shape)
# print("reading expression data, the size of the file is", E2.shape)
# get the first col in E (index)
E_index = E.index
# E2_index = E2.index
# select the target rows
selected_row = []
for item in P:
    if item in E_index:
    # if item in E_index and item in E2_index:
        selected_row.append(item)
print("after filtering the duplicates in pathway and expression, the data size is", len(selected_row))
# assert (0)

# get the data of E after selected
E_selected = E.loc[selected_row, :]
# E2_selected = E2.loc[selected_row, :]
# split the data into several types and save as csv file
for i in range(len(types)):
    cols = []
    col_list = type_list[i][:, 0]
    for j in col_list:
        if j in E.head():
            cols.append(j)
    print("after filtering, subtype \"{}\" has items of {}".format(types[i], len(cols)))
    save_name = './results/data_'+types[i]+'.csv'
    F = E_selected.loc[:, cols].T
    F.to_csv(save_name)
    print("saving as {}, and the size of the data is {}".format(save_name, F.shape))

# for i in range(len(types2)):
#     cols = []
#     col_list = type2_list[i][:, 0]
#     for j in col_list:
#         if j in E2.head():
#             cols.append(j)
#     print("after filtering, subtype \"{}\" has items of {}".format(types2[i], len(cols)))
#     save_name = './results/data_'+types2[i]+'.csv'
#     F = E2_selected.loc[:, cols].T
#     F.to_csv(save_name)
#     print("saving as {}, and the size of the data is {}".format(save_name, F.shape))