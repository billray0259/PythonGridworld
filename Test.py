variable = "\"hello\""

if variable[0] == "\"" and variable[-1] == "\"":
    variable = variable[1:-1]

print(variable)