    # for row in range(4):
    #     for col in range(4):
    #         if col != 0 and row != 0 and row != 3 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row-1][col] += "|di|"
    #             cave[row+1][col] += "|ui|"
    #             cave[row][col-1] += "|ri|"
    #             cave[row][col+1] += "|li|"
    #         elif col == 0 and row != 0 and row != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row-1][col] += "|di|"
    #             cave[row+1][col] += "|ui|"
    #             cave[row][col+1] += "|li|"
    #         elif col != 0 and row == 0 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row+1][col] += "|ui|"
    #             cave[row][col-1] += "|ri|"
    #             cave[row][col+1] += "|li|"
    #         elif col != 0 and row == 3 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row-1][col] += "|di|"
    #             cave[row][col-1] += "|ri|"
    #             cave[row][col+1] += "|li|"
    #         elif row != 0 and row != 3 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row-1][col] += "|di|"
    #             cave[row+1][col] += "|ui|"
    #             cave[row][col-1] += "|ri|"
    #         elif row == 3 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row-1][col] += "|di|"
    #             cave[row][col-1] += "|ri|"
    #         elif row == 0 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row+1][col] += "|ui|"
    #             cave[row][col-1] += "|ri|"
    #         elif col == 0 and row == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
    #             cave[row-1][col] += "|di|"
    #             cave[row][col+1] += "|li|"
    #
    #         if row == 0:
    #             cave[row][col] += "|ui|"
    #         if row == 3:
    #             cave[row][col] += "|di|"
    #         if col == 0:
    #             cave[row][col] += "|li|"
    #         if col == 3:
    #             cave[row][col] += "|ri|"

# a = [1,2,3]
# try:
#     a.remove(4)
# except ValueError:
#     print("error")

a = {1: 2}
print(a)
a.update({1: 3})
print(a)