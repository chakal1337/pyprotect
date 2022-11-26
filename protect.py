import hashlib
import base64
import sys
import string
import random
import dis

stub = """def get_eval_2(): return eval("\\x65\\x76\\x61\\x6c")
def esc_cz_2(): return get_eval_2()("\\x65\\x78\\x65\\x63")
esc_cz_2()("\\x69\\x6d\\x70\\x6f\\x72\\x74\\x20\\x73\\x79\\x73")
esc_cz_2()("\\x69\\x6d\\x70\\x6f\\x72\\x74\\x20\\x68\\x61\\x73\\x68\\x6c\\x69\\x62")
esc_cz_2()("\\x69\\x6d\\x70\\x6f\\x72\\x74\\x20\\x62\\x61\\x73\\x65\\x36\\x34")
def get_self(): return magic_str
def get_eval(): return eval(base64.b64decode("ZXZhbA==").decode())
def esc_cz(): return get_eval()(base64.b64decode("ZXhlYw==").decode())
def disable_print(): return get_eval()(base64.b64decode("ZGVmIHByaW50KGFyZ3MpOiByZXR1cm4=").decode())
def self_integr():
 if hashlib.md5(get_self().encode()).hexdigest() != self_hash: sys.exit(-1)
magic_str = "{SCRIPT}"
self_hash = "{SELF_HASH}"
xz_val = "{SCRIPT}"
xz_val = base64.b64decode(xz_val.encode()).decode()
self_integr()
cline_val = ""
for a_line in xz_val.splitlines():
 if a_line == "": continue
 a_line = a_line.split("\\t")
 hsh_val = a_line[0]
 hsh_chr = chr(int(a_line[1]) ^ int(a_line[2]))
 if hashlib.md5(hsh_chr.encode()).hexdigest() == hsh_val:
  cline_val += hsh_chr
 if hsh_chr == ";":
  esc_cz()(cline_val)
  cline_val = ""
esc_cz()(cline_val)
"""

stub_underscore = """def get_eval_2(): return eval("\\x65\\x76\\x61\\x6c")
def esc_cz_2(): return get_eval_2()("\\x65\\x78\\x65\\x63")
esc_cz_2()("\\x69\\x6d\\x70\\x6f\\x72\\x74\\x20\\x62\\x61\\x73\\x65\\x36\\x34")
my_script = "{SCRIPT}"
def get_eval(): return eval(base64.b64decode("ZXZhbA==").decode())
def esc_cz(): return get_eval()(base64.b64decode("ZXhlYw==").decode())
def disable_print(): return get_eval()(base64.b64decode("ZGVmIHByaW50KGFyZ3MpOiByZXR1cm4=").decode())
def underscore_to_char(string_old):
 string_new = ""
 string_old = string_old.split(" ")
 for string_old_l in string_old:
  if len(string_old_l): string_new += chr(len(string_old_l))
 return string_new
esc_cz()(underscore_to_char(my_script))
"""

symbols_randomize = [
 "xz_val",
 "cline_val",
 "a_line",
 "hsh_val",
 "hsh_chr",
 "esc_cz",
 "magic_str",
 "self_hash",
 "get_self",
 "self_integr",
 "main_func",
 "disable_print",
 "get_eval",
 "underscore_to_char",
 "my_script",
 "string_new",
 "string_old"
]

def underscore_to_char(string_old):
 string_new = ""
 string_old = string_old.split(" ")
 for string_old_l in string_old:
  string_new += chr(len(string_old_l))
 return string_new
 
def char_to_underscore(string_old):
 string_new = ""
 for i in range(len(string_old)):
  string_new += ("_" * ord(string_old[i])) + " "
 return string_new

def getrandstr():
 return "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(6, 8)))

def mangle_script(script_out):
 script_out = "import base64;exec(base64.b64decode(\"{}\").decode());".format(base64.b64encode(script_out.encode()).decode())
 return script_out

def randomize_vars(script_out):
 for symbol_curr in symbols_randomize:
  script_out = script_out.replace(symbol_curr, getrandstr())
 return mangle_script(script_out)
 
def protect(script_in, iter, maxiter):
 print("Protecting round {} of {}".format(iter, maxiter))
 print(script_in)
 script_out = ""
 for i in range(len(script_in)):
  hash_char = hashlib.md5(script_in[i].encode()).hexdigest()
  keychosen = random.randint(3, 35)
  script_out += "{}\t{}\t{}\n".format(hash_char, int(ord(script_in[i]) ^ keychosen), keychosen)
 script_encoded = base64.b64encode(script_out.encode()).decode()
 script_hash = hashlib.md5(script_encoded.encode()).hexdigest()
 script_out = stub.replace("{SCRIPT}", script_encoded)
 script_out = script_out.replace("{SELF_HASH}", script_hash)
 script_out = randomize_vars(script_out)
 if iter < maxiter:
  return protect(script_out, iter+1, maxiter)
 else:
  return script_out

def make_hex_escape(string):
 stringnew = ""
 for i in range(len(string)):
  stringnew += "\\x{:02x}".format(ord(string[i]))
 return stringnew 
 
def compress_script(script_out_final):
 final = ""
 for i in range(len(script_out_final)):
  final += "{}".format(ord(script_out_final[i]))
  if i != len(script_out_final): final += ","
 exec_a="for ___ in _.split(\",\"):\n if ___ != \"\": __ += chr(int(___));\n"
 final = "_=\"{}\";__=\"\";exec(\"{}\");exec(__);".format(final, make_hex_escape(exec_a))
 return final
   
if len(sys.argv) < 3:
 print("<script in> <script out>")
 sys.exit(0)
with open(sys.argv[1], "rb") as file:
 script_in = file.read().decode()
script_out = protect(script_in, 1, 1)
with open(sys.argv[2], "wb") as file:
 script_out_final = stub_underscore
 script_out_final = script_out_final.replace("{SCRIPT}", char_to_underscore(script_out))
 for symbol_curr in symbols_randomize:
  script_out_final = script_out_final.replace(symbol_curr, getrandstr())
 script_out_final = mangle_script(script_out_final)
 script_out_final = compress_script(script_out_final)
 write_to_file = script_out_final.encode()
 file.write(write_to_file)