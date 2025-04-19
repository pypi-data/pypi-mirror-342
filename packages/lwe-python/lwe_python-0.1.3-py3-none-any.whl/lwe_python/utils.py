import math
import random
from bitarray import bitarray

def __get_random_number(max, amt_to_return):
  ret = []
  for x in range(0, amt_to_return):
    ret.append(math.floor(random.random() * max))
  return ret


def encrypt_string(string_to_encrypt, public_key):
  byte_array = string_to_encrypt.encode('utf-8')
  bit_array = bitarray()
  bit_array.frombytes(byte_array)
  print(bit_array)
  encrypted_data_array = []
  for x in range(0, len(bit_array)):
    encrypted_data_array.append(encrypt_bit(public_key, bit_array[x]))
  
  return encrypted_data_array


def decrypt_data(encrypted_data, private_key):
  result = []
  for x in range(0, len(encrypted_data)):
    print(f"encrypted data is {type(encrypted_data[x]) == dict}")
    if (type(encrypted_data[x])  == list):
      for y in encrypted_data[x]:
        result.append(decrypt_bit(private_key, y))
    else:
      result.append(decrypt_bit(private_key, encrypted_data[x]))
  result = bitarray(result)
  result = result.tobytes()
  return result.decode('utf-8')

def encrypt_bit(public_key, bit):
  sample_rate = math.floor(public_key.number_of_equations / 2)
  sampled_indexes = __get_random_number(public_key.number_of_equations, sample_rate)
  sum_of_A_samples = 0
  sum_of_B_samples = 0
  for x in range(0, len(sampled_indexes)):
    sum_of_A_samples = sum_of_A_samples + public_key.A()[ sampled_indexes[x] ]
  
  for y in range(0, len(sampled_indexes)):
    sum_of_B_samples =  sum_of_B_samples + public_key.B()[ sampled_indexes[y] ]
  
  u = sum_of_A_samples % public_key.modulus
  v = (sum_of_B_samples +  math.floor(public_key.modulus / 2) * bit) % public_key.modulus
  return { "u": u, "v": v }


def decrypt_bit(private_key, encrypted_data):
  print(f"encrypted data is {encrypted_data}")
  bit_check = math.floor(private_key.modulus / 2)
  value_from_vector = encrypted_data["v"] - private_key.secret * encrypted_data["u"]
  dec = value_from_vector % private_key.modulus

  if dec > bit_check:
    return 1
  return 0


