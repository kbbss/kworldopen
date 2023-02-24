# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


from src.klsworld.person import fromLabelname as person_fromLabelname
from src.klsworld.targetshape import find as targetshape_find

person = person_fromLabelname("iu")
print("person",person)

targetshape = targetshape_find( "Linaqruf/anything-v3.0" , {"id":str(person["_id"]) ,"name":"person" }   )

print("targetshape",targetshape)