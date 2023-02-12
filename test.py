# some_list_data_struct = ["fuck","blue", "blue","you", "cock", "kevin", "ronald", "cock", "blue"]


# # Traditional path that is language agnostic
# print("Traditional path that is language agnostic")
# my_dict = {}
# for key in some_list_data_struct:
#     if key in my_dict:
#         my_dict[key]+=1
#     else:
#         my_dict[key]=1

# print(my_dict)
# print("\n")


# # Mega easy mode python way
# from collections import Counter

# print("Mega easy mode python way")
# mycounter  =  dict(Counter(some_list_data_struct))
# print(mycounter)
# print("\n")


# # My random ass fucky solution
# print("My random ass fucky solution")
# myfuckycounter = dict([(i,some_list_data_struct.count(i)) for i in some_list_data_struct])
# print(myfuckycounter)