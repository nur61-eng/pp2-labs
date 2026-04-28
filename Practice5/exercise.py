import re
text = "a ab abb abbb ac"
result = re.findall(r'ab*', text)
print(result)
#2
import re
text = "ab abb abbb abbbb"
result = re.findall(r'ab{2,3}', text)
print(result)
#3
import re
text = "hello_world test_string Python_Test"
result = re.findall(r'[a-z]+_[a-z]+', text)
print(result)
#4
import re
text = "Hello world My name is Tamirlan"
result = re.findall(r'[A-Z][a-z]+', text)
print(result)
#5
import re
text = "acb aab axb a9b"
result = re.findall(r'a.b', text)
print(result)
#6
import re
text = "Hello, world. Python is cool"
result = re.sub(r'[ ,.]', ':', text)
print(result)
#7
import re
text = "hello_world_python"
result = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)
print(result)
#8
import re
text = "HelloWorldPython"
result = re.findall(r'[A-Z][^A-Z]*', text)
print(result)
#9
import re
text = "HelloWorldPython"
result = re.sub(r'([A-Z])', r' \1', text).strip()
print(result)
#10
import re
text = "HelloWorldPython"
result = re.sub(r'([A-Z])', r'_\1', text).lower().lstrip('_')
print(result)