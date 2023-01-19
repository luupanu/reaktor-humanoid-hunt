from collections import defaultdict

def read_data():
  with open('challenge_2', 'r') as file:
    return file.read()

def most_frequent(s):
  d = defaultdict(int)
  for c in s:
    d[c] += 1
  return max(d.items(), key=lambda kv: kv[1])[0]

def find_all_chars_next_to(s, c):
  next_to = []
  for i, x in enumerate(s):
    if x == c:
      next_to.append(s[i+1])
  return ''.join(next_to)

def decode_data():
  password = []
  s = read_data()
  c = most_frequent(s)
  while True:
    password.append(c)
    next_to = find_all_chars_next_to(s, c)
    c = most_frequent(next_to)
    if c == ';':
      return ''.join(password)

if __name__ == '__main__':
  print(decode_data())
