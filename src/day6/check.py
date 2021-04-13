def input_check(result_list, trigger=None):
    while (True):
        try:
            if (trigger is None):
                input_number = int(input("#: "))
                if (len(result_list) < int(input_number) or int(input_number) == 0):
                    print("That wasn't a number")
                else:
                    print(result_list[input_number - 1][0].title())
                    break
            else:
                input_number = int(input())
                break
        except Exception:
            print("That wasn't a number")

    return input_number


def number_to_code(result_list, number):
    return result_list[number - 1][2]

