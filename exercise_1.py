def read_data():
  with open('challenge_1', 'r') as file:
    return file.read().split('\n')

def byte_to_int(b):
  try:
    return int(b, 2)
  except ValueError:
    print('Not a valid number')

def decode_line(line, chunk_size):
  valid = False
  i = 0
  while True:  # assume we don't have bad data and get stuck in an infinite loop
    value = byte_to_int(line[i:i+chunk_size])
    if value < len(line) / chunk_size:
      i = value * chunk_size
      valid = True
    else:
      if valid:
        return byte_to_int(line[i:i+chunk_size])
      i += chunk_size

def decode_ascii(a):
  return ''.join(chr(i) for i in a)

def decode_data():
  password = []
  for line in read_data():
    password.append(decode_line(line, 8))
  return decode_ascii(password)

if __name__ == '__main__':
  print(decode_data())
