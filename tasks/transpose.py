matrix = [
    [1,2,3,4,5,6],
    [4,5,6,5,6,7],
    [7,8,9,6,7,8],
    [10,11,12,13,9,10],
    [4,5,6,5,6,7],
    [7,8,9,6,7,8],
    ]

def transpose(matrix):
    for i in range(len(matrix)//2+1):
        for j in range(len(matrix[0])):
            if i<j:
                temp = matrix[i][j]
                matrix[i][j] = matrix[j][i]
                matrix[j][i] = temp

transpose(matrix)
print(matrix)


"""
module:
request
logger

tasks:
forecast - future
past - forecast
"""