
#This is my DIY version of maths LATEX stuff, it pulls out functions from the input text and evaluates them using other modules i've built

from trignometric_functions import sin_Deg, cos_Deg, tan_Deg


def interpretInput(data):
    try:
        all_num = int(data)
        return all_num
    except ValueError:
        try:
            all_num = float(data)
            return all_num
        except ValueError:
            all_num = False

    if all_num == False:
        numbers = ""
        letters = ""

        for i, char in enumerate(data):
            if char.isdigit():
                numbers = numbers + str(char)
            elif char == ".":
                numbers = numbers + "."
            elif char == "-":
                if "-" in numbers:
                    try:
                        numbers = str(float(numbers)*(-1))
                    except:
                        if numbers == "-":
                            numbers = ""
                        else:
                            return "error"
                else:
                    numbers = "-" + numbers
            else:
                letters = letters + char

        print(numbers)
        print(letters)
        try:
            float(numbers)
        except ValueError:
            return "error"
        if letters == "sin()":
            return round(sin_Deg(float(numbers), 50),5)
        if letters == "cos()":
            return round(cos_Deg(float(numbers), 50),5)
        if letters == "tan()":
            output = tan_Deg(float(numbers), 50)
            if output != "error":
                return round(output, 5)
            else:
                return "error"
        
        