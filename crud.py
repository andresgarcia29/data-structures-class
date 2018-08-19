"""
  CRUD
  This class we can inherit to get this methods
"""

from contracts.validations import return_validation, validate_contract, validate_id
from helpers.messages import messages
from helpers.order import sort_like_contracts, sort_update_like_contracts

class CRUD (object):

    jump = '\n'
    delimiter = '|'

    @staticmethod
    def converto_to_text(sort_array):
        #Convert array to format text
        text = ""
        for x in sort_array:
            text += str(x) + CRUD.delimiter
        text = text[0: len(text) - 1] + CRUD.jump
        return text

    @staticmethod
    def search_position_array_id(lines, id):
      #Search the position of id
        for i, x in enumerate(lines):
            if x.split('|')[0] == str(id):
                return i

    def __init__(self, *args, **kwargs):
        self.file_path = kwargs['_file']
        del kwargs['_file']

    def getAll(self):
      with open(self.file_path, 'a+') as file:
        file = open(self.file_path, 'r')
        lines = []
        for line in file:
          lines.append(line)
        return lines

    @validate_id
    def get_one_by_id(self, id):
      with open(self.file_path, 'a+') as file:
        file = open(self.file_path, 'r')
        for line in file:
          if int(line.split('|')[0]) == int(id):
            file.close()
            return line

    @validate_contract
    def create(self, **obj):
      with open(self.file_path, 'a+') as file:
        #Get all the lines to the file to convert to ID
        self.id = len(open(self.file_path).readlines())
        #Assign ID
        obj['id'] = self.id
        #Order components like fields
        sort_array = sort_like_contracts(**obj)
        #Prepair text to insert
        text = ""
        for x in sort_array:
          text += str(x) + CRUD.delimiter
        text = text[0: len(text) - 1] + CRUD.jump
        #Insert text in a file
        file.write(text)

    @validate_id
    @validate_contract
    def update(self, **obj):
      with open(self.file_path, 'r+') as file:
        #Find element to update
        register = self.get_one_by_id(obj['id'])
        #Delete the primary object
        del obj['id']
        #Sort and update the exactly fields
        kwargs = {}
        kwargs['obj'] = obj
        kwargs['register'] = register
        register = sort_update_like_contracts(**kwargs)
        #Prepair string to change in array
        register = self.converto_to_text(register)
        #Delete a line and insert the line
        lines = file.readlines()
        current_line = self.search_position_array_id(lines, register.split('|')[0])
        lines[int(current_line)] = register
      #Change all the text
      with open(self.file_path, 'w+') as file:
          for x in lines:
            file.write(x)

    @validate_id
    def delete(self, id):
      with open(self.file_path, 'r+') as file:
        #Read all lines
        lines = file.readlines()
        #Get position of id and delete
        position = self.search_position_array_id(lines, id)
        del lines[position]
      #Change all the text
      with open(self.file_path, 'w+') as file:
          for x in lines:
              file.write(x)