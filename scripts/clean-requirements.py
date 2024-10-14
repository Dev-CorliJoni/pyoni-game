def filter_requirements(filename, excludes):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if not any(exclude in line for exclude in excludes):
                print(f"{line.strip()} added to requirements.txt.")
                file.write(line)
            else:
                print(f"{line.strip()} removed from requirements.txt.")



print()
print(f"------------- Start cleaning requirements.txt file -------------")
excludes = ['pipreqs', 'setuptools']
filter_requirements('requirements.txt', excludes)
print()
