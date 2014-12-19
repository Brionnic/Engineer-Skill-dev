__author__ = 'Snoopy'
import os

def read_default_skill_list():
    #   Make a list that will store lists of skill column headers, this will be returned to the calling function
    skill_list = []

    dir_path = os.getcwd()
    file_path = "\\skills_module\\static\\NCE_Skill.txt"
    working_path = dir_path + file_path
    path = 'C:\\Users\\Snoopy\\Dropbox\\Cisco Projects\\Advanced Services\\AS_Skills v0.2\\skills_module\\static\\skill_set.txt'
    with open(working_path, 'r') as skill_file:
        for default_skill in skill_file:
            # strip the whitespace
            new_line = default_skill.split('___')

            # use list comprehension to make a new list of titles for each column
            skill_column_list = [item for x,item in enumerate(new_line) if x < 5 ]

            # print skill_column_list

            # add this small list (of the row) to the master list
            skill_list.append(skill_column_list)

    # return the master list
    return skill_list

if __name__ == '__main__':
    new_list = read_default_skill_list()

    print new_list