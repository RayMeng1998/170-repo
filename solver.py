import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from collections import Counter

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]  #Create a Graph
    list_of_homes_indices = []
    starting_car_location_index = list_of_locations.index(starting_car_location) # Change the starting_car_location to index
    dropoff_dict = {}
    tour = [starting_car_location_index]
    for home in list_of_homes:# Create a list of home indices
        list_of_homes_indices.append(list_of_locations.index(home))
    #Eliminating Dead-End Scenario
    for home in list_of_homes_indices:
        n = nx.all_neighbors(G,home)
        if list(n) == 1:
            list_of_homes_indices.remove(home)
            dropoff_list = [home]
            neighbor = n[0]
            ns = nx.all_neighbors(G, neighbor)
            count = len(ns)
            while count == 2:
                if neighbor in list_of_homes_indices:
                    list_of_homes_indices.remove(neighbor)
                    dropoff_list.append(neighbor)
                ns.remove(neighbor)
                neighbor = ns[0]
                ns = nx.all_neighbors(G, neighbor)
                count = len(ns)
            if neighbor not in dropoff_dict.keys():
                dropoff_dict[neighbor] = dropoff_list
            else:
                dropoff_dict[neighbor] += dropoff_list
        else:
            if home not in dropoff_dict.keys():
                dropoff_dict[home] = [home]
            else:
                dropoff_dict[home].append(home)
    start_point = starting_car_location_index
    sth = None
    while list_of_homes_indices:
        min, result = float('inf'), None
        for home in list_of_homes_indices:
            l = nx.dijkstra_path_length(G, start_point, home)
            if l < min:
                min, result = l, home
        tour += list(nx.dijkstra_path(G, start_point, result)[1:])
        start_point = result
        if len(list_of_homes_indices) == 1:
            sth = list_of_homes_indices[0]
        list_of_homes_indices.remove(result)
    tour += list(nx.dijkstra_path(G, sth, starting_car_location_index)[1:])
    return tour, dropoff_dict



"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
