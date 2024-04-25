import csv

# Your list
your_list = [1, 2, 3, 4, 5]

# Writing the list to a CSV file with each element in a separate cell horizontally
with open('your_list.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(your_list)

