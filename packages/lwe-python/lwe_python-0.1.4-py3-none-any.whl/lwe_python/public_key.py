import random
import json
import os


class PublicKey:
  def __init__(self, mod_number=None, error_vector=None, number_of_equations=None):
    if mod_number is None or error_vector is None or number_of_equations is None:
      raise Exception("Required arguments are missing")
    self.modulus = mod_number
    self.error_vector = error_vector
    self.number_of_equations = number_of_equations
    self.__A = []
    self.__B = []
  
  @classmethod
  def loadJSON(cls, json_data):
    data = json.loads(json_data)
    key = cls(mod_number=data['mod'], error_vector=[], number_of_equations=data['eq'])
    key.set_A_vector(data['Aval'])
    key.set_B_vector(data['Bval'])
    return key
  
  @classmethod
  def load_keyfile(cls, keyfile_path):
    fp = open(keyfile_path)
    data = fp.read()
    fp.close()
    return cls.loadJSON(data)


  def A(self):
    return self.__A

  def B(self):
    return self.__B

  def __randomize(self):
    return random.randint(1, self.modulus - 1)
  
  def __generate_A_values(self):
    for x in range(0, self.number_of_equations):
      self.__A.append(self.__randomize())

  def generate_key_values(self, secret):
    if len(self.__A) == 0:
      self.__generate_A_values()
    for i in range(0, self.number_of_equations):
      self.__B.append((self.__A[i] * secret + self.error_vector[i]) % self.modulus)
  
  def set_A_vector(self, vector):
    if len(vector) > self.number_of_equations:
      raise Exception("Too many vector entries")
    for val in vector:
      if val > self.modulus:
        raise Exception("Entries  need to be less than the modulus")
    self.__A = vector
  
  def set_B_vector(self, vector):
    if len(self.__B) > self.number_of_equations:
      raise Exception("Too many vector entries")
    if len(self.__B) != 0:
      raise Exception("B values already generated")
    self.__B = vector

  def to_json(self):
    result_dict = {}
    result_dict['Aval'] = self.__A
    result_dict['Bval'] = self.__B
    result_dict['eq'] = self.number_of_equations
    result_dict['mod'] = self.modulus
    return json.dumps(result_dict)
  

  def save_to_keyfile(self, keyfile_path):
    fp = open(os.path.join(keyfile_path, "pub.lwe.key"), "w")
    results = self.to_json()
    fp.write(results)
    fp.close()
