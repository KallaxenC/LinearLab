
#This is my DIY version of maths LATEX stuff, it pulls out functions from the input text and evaluates them using other modules i've built

from trignometric_functions import sin_Deg, cos_Deg, tan_Deg

# I decided to setup a constant for the decimal precision we want to round all our non-exact values to. This means we can adjust this without having to change the value on each function individually
DECIMAL_PRECISION = 5 

def work_with_fractions(letter_array, number_array):
    output = ""
    for i in range(len(number_array)):
        result = ""
        
        numbers = number_array[i]

        try:
            letters = letter_array[i]
        except Exception:
            continue

        negative_function = letters.startswith("-")
        function = letters[1:] if negative_function else letters

        if function == "sin()" or function == "sin":
            result = round(sin_Deg(float(numbers), 50), DECIMAL_PRECISION)

        if function == "cos()" or function == "cos":
            result = round(cos_Deg(float(numbers), 50), DECIMAL_PRECISION)

        if function == "tan()" or function == "tan":
            outcome = tan_Deg(float(numbers), 50)
            if outcome != "error":
                result =  round(output, DECIMAL_PRECISION)
            else:
                return "error" 
                
            
        if function == "sqrt()" or function == "sqrt" or function == "root()" or function == "root":
            if float(numbers) < 0:
                return "error" 
                
            else:
                result = round(float(numbers) ** 0.5, DECIMAL_PRECISION)

        if negative_function and function in ("sin()", "sin", "cos()", "cos", "tan()", "tan", "sqrt()", "sqrt", "root()", "root"):
            result = -result

        if function == "" and numbers != "":
            if output == "":
                output = float(numbers)
            else:
                try:
                    output = round(output / float(numbers), DECIMAL_PRECISION)
                except ZeroDivisionError:
                    return "error" 
                    

        elif function == "":
            continue
        elif output == "":
            output = result
        else:
            try:
                output = round(float(output) / result, DECIMAL_PRECISION)
            except ZeroDivisionError:
                return "error" 
                

    return output
            
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
        number_array = []
        letter_array = []

        for i, char in enumerate(data):
            already_added = False
            if char == "/":
                number_array.append(numbers)
                letter_array.append(letters)
                numbers = ""
                letters = ""
                already_added = True
            elif char.isdigit():
                numbers = numbers + str(char)
            elif char == ".":
                numbers = numbers + "."
            elif char == "-":
                if numbers == "" and letters == "" and i + 1 < len(data) and data[i + 1].isalpha():
                    letters = "-"
                elif "-" in numbers:
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

        if already_added == False:
            number_array.append(numbers)
            letter_array.append(letters)
        
        output = work_with_fractions(letter_array, number_array)
        return output

        '''
        try:
            float(numbers)
        except ValueError:
            return "error" 
            
        '''
        #Trig function checker


        
        