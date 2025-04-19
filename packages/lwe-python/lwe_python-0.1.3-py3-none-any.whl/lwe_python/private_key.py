import os
import json

class PrivateKey():
  def __init__(self, secret, modulus=None):
    self.secret = secret
    self.modulus = None
    if modulus is not None:
      self.modulus = modulus

  @classmethod
  def loadJSON(cls, json_data):
    data = json.loads(json_data)
    key = cls(data['mod'])
    return key
  
  @classmethod
  def load_keyfile(cls, keyfile_path):
    fp = open(keyfile_path)
    data = fp.read()
    fp.close()
    return cls.loadJSON(data)

  def save_to_keyfile(self, keyfile_path):
    fp = open(os.path.join(keyfile_path, "sec.lwe.key"), "w")
    data = json.dumps({
      "sec": self.secret,
      "mod": self.modulus
    })
    fp.write(data)
    fp.close()