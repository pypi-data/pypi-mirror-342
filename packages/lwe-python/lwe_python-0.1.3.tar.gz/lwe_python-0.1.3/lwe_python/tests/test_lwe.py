from .. import PublicKey, PrivateKey, encrypt_bit, decrypt_bit, encrypt_string, decrypt_data
import pytest
import json


@pytest.fixture
def public_key_file(mocker):
  builtin_open = "builtins.open"
  keydata = mocker.mock_open(read_data=json.dumps(
    {
      "Aval": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
      "Bval": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 ],
      "eq": 13,
      "mod": 13
    }
  ))
  mocker.patch(builtin_open, keydata)



@pytest.fixture
def save_keyfile(mocker):
  builtin_open = "builtins.open"
  return mocker.patch(builtin_open, mocker.mock_open())


def test_public_key_generates_A_values():
  key = PublicKey(mod_number=13, error_vector=[1,2, 1], number_of_equations=3)
  key.generate_key_values(100)
  print(key.A())
  assert len(key.A()) == 3
  assert key.A()[0] < key.modulus
  assert key.A()[1] < key.modulus
  assert key.A()[2] < key.modulus


def test_A_vector_accept_correct_number_of_values():
  key = PublicKey(mod_number=13, error_vector=[1,2, 1], number_of_equations=3)
  with pytest.raises(Exception):
    key.set_A_vector([4,5,6,7,8])
  
  key.set_A_vector([3, 5, 9])
  assert len(key.A()) == 3


def test_A_vector_only_accepts_correct_values():
  key = PublicKey(mod_number=13, error_vector=[1,2, 1], number_of_equations=3)
  with pytest.raises(Exception):
    key.set_A_vector([99, 4, 8])

def test_public_key_generates_B_vector():
  key = PublicKey(mod_number=13, error_vector=[1,2,1], number_of_equations=3)
  key.generate_key_values(100)
  assert len(key.B()) == key.number_of_equations

def test_public_key_generates_correct_values_for_B_vector():
  #  const opts: KeyOptions = {
  #   modNumber: 97,
  #   errorVector: [1, 1, 4, 1, 4],
  #   numberOfEquations: 5
  # }
  # const pubkey = new PublicKey(opts)
  # pubkey.setAVec([6, 38, 90, 83, 51])
  # pubkey.generateKeyValues(5)
  # const secretKey = new PrivateKey(opts)
  # secretKey.setSecret(5)
  # const vectorB = pubkey.getB()
  # expect(vectorB).toEqual([31, 94, 66, 28, 65])
  key = PublicKey(mod_number=97, error_vector=[1, 1, 4, 1, 4], number_of_equations=5)
  key.set_A_vector([6, 38, 90, 83, 51])
  key.generate_key_values(5)
  Bvectors = key.B()
  assert Bvectors == [31, 94, 66, 28, 65]

def test_returns_valid_JSON_for_PublicKey():
  key = PublicKey(mod_number=3557, error_vector=[1,4,2,-2], number_of_equations=4)
  key.generate_key_values(200)
  result = key.to_json()
  result_json = json.loads(result)
  assert "Aval" in result_json.keys()
  assert "Bval" in result_json.keys()
  assert "eq" in result_json.keys()
  assert "mod" in result_json.keys()

def test_loads_valid_JSON_key_file():
  keydata = {
    "Aval": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    "Bval": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 ],
    "eq": 13,
    "mod": 13
  }
  keydata_json = json.dumps(keydata)
  key = PublicKey.loadJSON(keydata_json)
  assert key.number_of_equations == 13
  assert key.A() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
  assert key.B() == [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 ]


def test_public_key_loads_keyfile(public_key_file):
  key = PublicKey.load_keyfile("./pub.lwe.key")
  assert key.number_of_equations == 13
  assert key.A() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
  assert key.B() == [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 ]
  assert key.modulus == 13

def test_public_key_saves_keyfile(save_keyfile):
  key = PublicKey(mod_number=13, error_vector=[], number_of_equations=13)
  key.set_A_vector([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
  key.set_B_vector([21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 ])
  key.save_to_keyfile("./")
  content = json.dumps({
    "Aval": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    "Bval": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 ],
    "eq": 13,
    "mod": 13
  })
  save_keyfile().write.assert_called_once_with(content)



def test_save_private_key_info(save_keyfile):
  priv_key = PrivateKey(100)
  priv_key.save_to_keyfile("./")
  content = json.dumps({
    "sec": 100,
    "mod": None
  })
  save_keyfile().write.assert_called_once_with(content)


def test_encrypt_decrypt_bit_works():
  secret_value = 5
  mod_number = 97
  error_vector = [1, 1, 4, 1, 4, 3, 2, 4, 1, 2, 3, 4, 3, 3, 2, 1, 1, 3, 4, 1]
  number_of_equations = 20
  message = 1

  pub_key = PublicKey(mod_number=mod_number, error_vector=error_vector, number_of_equations=number_of_equations)
  pub_key.generate_key_values(secret_value)
  priv_key = PrivateKey(secret_value, mod_number)
  ev = encrypt_bit(pub_key, message)
  result = decrypt_bit(priv_key, ev)
  assert result == message

def test_encrypt_string_function_works():
  secret_value = 5
  mod_number = 97
  error_vector = [1, 1, 4, 1, 4, 3, 2, 4, 1, 2, 3, 4, 3, 3, 2, 1, 1, 3, 4, 1]
  number_of_equations = 20

  pub_key = PublicKey(mod_number=mod_number, error_vector=error_vector, number_of_equations=number_of_equations)
  pub_key.generate_key_values(secret_value)
  priv_key = PrivateKey(secret_value, mod_number)
  data = encrypt_string("hi", pub_key)
  final = decrypt_data(data, priv_key)
  assert final == "hi"

  data = encrypt_string(json.dumps({"hello": "world"}), pub_key)
  final = decrypt_data(data, priv_key)
  final = json.loads(final)
  assert final["hello"] == "world"




