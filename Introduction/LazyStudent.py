"""

********** Documentation of the nature of the program **********
The program will get the name of a destination file with the extension txt as the first argument,
and in addition as the second argument the name of the destination file.
In the source file, invoicing operations will be given in a structure such as: 3 + 4,
ie a profit operand and then an operator and then again a profit and then another operand.
The role of the program is to calculate the mathematical expression and write the result in a
structure such as 3 + 4 = 7 directly into the testified file.
In case of connection errors or logic errors, the program will write in the target file the required comment.
********* end Documentation of the nature of the program *********

Author by Shimon Mizrahi 203375563
"""

import sys
import os
# consts
ZERO = 0
ONE = 1
TOW = 2
# global vars
full_path = ""
source = ""
destination = ""
list_of_source = []
list_of_destination = []


def operator(expression, first_operand, second_operand):
    """
    :param expression : str
    :param first_operand: int
    :param second_operand: int
    :return: str(Calculation of arithmetic expression)
    """
    result = 0
    if "+" in expression:
        result = first_operand + second_operand
    elif "-" in expression:
        result = first_operand - second_operand
    elif "*" in expression:
        result = first_operand * second_operand
    elif "/" in expression:
        result = first_operand / second_operand
    return str(result)


def check_if_not_containing_letters(first_operand, second_operand):
    """
    :param first_operand: str
    :param second_operand: str
    :return: True if not containing letters
    """
    result = False
    if first_operand.isdigit() and second_operand.isdigit():
        result = True
    return result


def one_operator_only(expression):
    """
    :param expression: str
    :return: True if containing one operator only
    """
    result = False
    if expression.count("+") + expression.count("-") + expression.count("*") + expression.count("/") == 1:
        result = True
    return result


def check_if_division_by_zero(expression, second_operand):
    """
    :param expression: str
    :param second_operand: int
    :return: True if division by zero
    """
    result = False
    if "/" in expression and int(second_operand) == 0:
        result = True
    return result


def calculate(expression):
    """
    :param expression: str
    :return: str, the function calculate the expression and return it
    """
    answer = ""
    if not expression.count(" ") == 2:
        answer = "The expression must be from a configuration such as the following 1 + 1 example\n"
        return answer
    argument_index = expression.index(" ")
    first_operand = expression[0:argument_index]
    second_operand = expression[argument_index+3:]
    if not one_operator_only(expression):
        answer = "Error, to many operands\n"
    elif not check_if_not_containing_letters(first_operand, second_operand):
        answer = "Error, not allowed letters\n"
    elif check_if_division_by_zero(expression, second_operand):
        answer = "Error, Division by zero\n"
    else:
        answer = expression + " = " + operator(expression, int(first_operand), int(second_operand)) + "\n"
    return answer


def file_operations(flag):
    """
    :return non, The function reads / writes to a file (depending on the parameter you receive)
    """
    if flag == 'r':
        with open(source, flag) as in_file:
            for line in in_file:
                list_of_source.append(line)
    else:
        with open(destination, flag) as out_file:
            for line in list_of_destination:
                out_file.write(line)


def check_num_of_arguments(sum_of_argument):
    """
    :param sum_of_argument: int
    :return: True if sum of argument == 2
    """
    global full_path, source, destination
    result = "True"
    if sum_of_argument > 2:
        full_path = sys.argv[ZERO]
        source = sys.argv[ONE]
        destination = sys.argv[TOW]
    elif sum_of_argument == 1:
        result = "script must to contain source ond destination files!"
    elif sum_of_argument == 2:
        result = "script must to contain destination file!"
    else:
        result = "ERROR There is no path to the executable!"
    return result


def check_if_files_exist(files_list):
    """
    :param files_list: str
    :return:  True if the files are exits and there name are correct
    """
    result = ""
    if source not in files_list:
        result = "Error, The file name " + source + " not correct!"
    if destination not in files_list:
        result = "Error, The file name " + destination + " not correct!"
    if source in files_list and destination in files_list:
        result = "True"
    return result


def assert_our_program():
    """
    assert function
    :return: non
    """
    assert calculate("3 + 4") == "3 + 4 = 7\n"
    assert calculate("7 w- 2") == "Error, not allowed letters\n"
    assert calculate("5 ** 3") == "Error, to many operands\n"
    assert calculate("12 / 6") == "12 / 6 = 2.0\n"
    assert calculate("1 / 0") == "Error, Division by zero\n"
    assert calculate("5  / 5") == "The expression must be from a configuration such as the following 1 + 1 example\n"
    assert calculate("4+ 0") == "The expression must be from a configuration such as the following 1 + 1 example\n"
    assert calculate("1 *2") == "The expression must be from a configuration such as the following 1 + 1 example\n"
    assert calculate("3 * 2 ") == "The expression must be from a configuration such as the following 1 + 1 example\n"


def main():
    """
    main function
    :return: non
    """
    sum_of_argument = len(sys.argv)
    script_integrity = check_num_of_arguments(sum_of_argument)
    if script_integrity == "True":
        dir_path = full_path.rfind('/')
        files_exist = check_if_files_exist(os.listdir(full_path[0:dir_path]))
        if files_exist == "True":
            file_operations('r')
            for item in list_of_source:
                if "\n" in item:
                    end_line_index = item.index("\n")
                    expression = item[0:end_line_index]
                    list_of_destination.append(calculate(expression))
                else:
                    expression = "Each arithmetic expression must be in a separate line!"
                    list_of_destination.append(expression)
            file_operations('w')
        else:
            print(files_exist)
    else:
        print(script_integrity)
    assert_our_program()


if __name__ == '__main__':
    main()
