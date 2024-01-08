import subprocess
import chardet # detect the encoding of text 

outputText = subprocess.run(
    'ipconfig',
    shell=True,
    check=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
).stdout #.decode('gbk')
import chardet # detect the encoding of text 

encodingInfo = chardet.detect(outputText)
encoding = encodingInfo['encoding']
output = outputText.decode(encoding, 'ignore')
print(output)