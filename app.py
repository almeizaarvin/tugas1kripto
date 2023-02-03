from flask import Flask, render_template, request, redirect, url_for
import ast 


app = Flask(__name__, static_folder="static")


@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        method = request.form['method']
        key = request.form['key']
        action = request.form['action']
        if file:
            if method == "ExtendedVigenereCipher":
                return(readTextFileinByte(file, method))
            elif method == "VigenereCipher":
                rawtext=readTextFile(file, method)
                if action=="Encrypt":
                    return(vigenereCipherEncrypt(rawtext, key))
                elif action=="Decrypt":
                    return(vigenereCipherDecrypt(rawtext, key))
            elif method == "AutokeyVigenereCipher":
                rawtext=readTextFile(file, method)
                if action=="Encrypt":
                    return(autokeyVigenereCipherEncrypt(rawtext, key))
                elif action=="Decrypt":
                    return(autokeyVigenereCipherDecrypt(rawtext, key))
            elif method == "AffineCipher":
                rawtext=readTextFile(file, method)
                if action=="Encrypt":
                    return(affineCipherEncrypt(rawtext, key))
                elif action=="Decrypt":
                    return(affineCipherDecrypt(rawtext, key))
            elif method == "HillCipher":
                rawtext=readTextFile(file, method)
                matrixKey=readMatrix(key)
                if action=="Encrypt":
                    return(hillCipherEncrypt(rawtext, matrixKey))
                elif action=="Decrypt":
                    return(hillCipherDecrypt(rawtext, matrixKey))
            else:
                render_template('index.html', text=readTextFile(file, method), method=method)
    
    else:
        return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True)

#FILE PROCESSING HELPER

def removeNonCharacter(text):
    return ''.join(filter(str.isalnum, text))

def readTextFile(file, method):
    file_contents = file.read().decode('utf-8')
    return file_contents

def readTextFileinByte(file, method):
    file_contents = file.read()
    return file_contents

#MATRIX PROCESSING HELPER (PENGGANTI LIBRARY)

def inverseModulo(a, p):
    for i in range(p):
        r = (i * a) % p
        if r == 1:
            break
    return i

def readMatrix(key):
    return ast.literal_eval(key)

def multiplyMatrix(m1, m2):
    m3 = [[0 for j in range(len(m2[0]))] for i in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                m3[i][j] += m1[i][k] * m2[k][j]
    return m3

def alphabetIndex(char):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet.index(char)

def indexOfAlphabet(idx):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range (0, len(alphabet)):
        if alphabet[idx] == alphabet[i]:
            return alphabet[idx]
        
def createInverseMatrix(A):
    n = len(A)
    AM = [[0] * 2 * n for i in range(2 * n)]
    for i in range(n):
        for j in range(n):
            AM[i][j] = A[i][j]
    for i in range(n):
        for j in range(n, 2 * n):
            AM[i][j] = 0
        AM[i][i + n] = 1
    for i in range(n):
        for j in range(i + 1, n):
            if AM[i][i] == 0:
                continue
            m = AM[j][i] / AM[i][i]
            for k in range(2 * n):
                AM[j][k] -= m * AM[i][k]
    for i in range(n - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            if AM[i][i] == 0:
                continue
            m = AM[j][i] / AM[i][i]
            for k in range(2 * n):
                AM[j][k] -= m * AM[i][k]
    for i in range(n):
        t = AM[i][i]
        for j in range(2 * n):
            AM[i][j] /= t
    result = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = AM[i][j + n]
    return result

def determinantMatrix(A):
    n = len(A)
    AM = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            AM[i][j] = A[i][j]
    for i in range(n):
        for j in range(i + 1, n):
            if AM[i][i] == 0:
                continue
            m = AM[j][i] / AM[i][i]
            for k in range(n):
                AM[j][k] -= m * AM[i][k]
    result = 1.0
    for i in range(n):
        result *= AM[i][i]
    return result

def adjointMatrix(m):
    n = len(m)
    adj_m = []
    for i in range(n):
        adj_m.append([])
        for j in range(n):
            adj_m[i].append((-1)**(i+j) * determinantMatrix(minor(m, i, j)))
    return transpose(adj_m)

def minor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def transpose(m):
    return [list(x) for x in zip(*m)]

def createMatrixGrouping(text, step):
    if (len(text) % step != 0):
        for i in range (0, len(text) % step):
            text += 'X'
    matrixGrouping = [[[text[i-1]], [text[i]]] for i in range (1, len(text), 2)]
    return matrixGrouping

def vigenereCipherEncrypt(plaintext, key):
    plaintext = removeNonCharacter(plaintext)
    keyIndex = [ord(i) for i in key]
    plaintextIndex = [ord(i) for i in plaintext]
    ciphertext = ''
    for i in range(len(plaintextIndex)):
        x = ((plaintextIndex[i] + keyIndex[i % len(key)]) % 26) + ord('A')
        ciphertext += chr(x)
            
    return render_template('index.html', text=plaintext, method="vigenereCipher", action="Encrypt", result=ciphertext)

def vigenereCipherDecrypt(ciphertext, key):
    keyIndex = [ord(i) for i in key]
    ciphertextIndex = [ord(i) for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertextIndex)):
        x = ((ciphertextIndex[i] - keyIndex[i % len(key)]) % 26 ) + ord('A')
        plaintext += chr(x)

    return render_template('index.html', text=ciphertext, method="vigenereCipher", action="Decrypt", result=plaintext)

def autokeyVigenereCipherEncrypt(plaintext, key):
    keyword = key + plaintext
    ciphertext = ""

    for i in range(len(plaintext)):
        j = int(i % len(keyword))
        ciphertext += indexOfAlphabet((alphabetIndex(plaintext[i]) + alphabetIndex(keyword[j])) % 26)
        print(ciphertext)
        
    return render_template('index.html', text=plaintext, method="AutokeyVigenereCipher", action="Encrypt", result=ciphertext)

def autokeyVigenereCipherDecrypt(ciphertext, key):
    plaintext = ''
    keyIndex = 0

    for i in range (0, len(ciphertext)):
        x = chr((26 + ord(ciphertext[i]) - ord(key[keyIndex])) % 26 + 65)
        plaintext +=x
        key += x
        keyIndex += 1

    return render_template('index.html', text=ciphertext, method="AutokeyVigenereCipher", action="Decrypt", result=plaintext)

def affineCipherEncrypt(plaintext, inputkey):
    a=int(inputkey[0])
    b=int(inputkey[3])
    ciphertext=''
    
    for i in range(len(plaintext)):
        x = (a * (ord(plaintext[i]) - ord('A')) + b) % 26
        ciphertext += chr(x+ ord('A'))
    return render_template('index.html', text=plaintext, method="affineCipher", action="Encrypt", result=ciphertext)
    
def affineCipherDecrypt(ciphertext, inputkey):
    a=int(inputkey[0])
    b=int(inputkey[3])
    plaintext=''
    
    aInv = inverseModulo(a, 26)
            
    for char in ciphertext:
        index = (aInv * (alphabetIndex(char) - b)) % 26
        plaintext += indexOfAlphabet(index)
    return render_template('index.html', text=ciphertext, method="affineCipher", action="Decrypt", result=plaintext)

def hillCipherEncrypt(plaintext, key):
    step = len(key)
    plaintextMatrix = createMatrixGrouping(plaintext, step)
  
    for i in range (0, len(plaintextMatrix)):
        for j in range (0, len(plaintextMatrix[i])):
            for k in range (0, len(plaintextMatrix[i][j])):
                plaintextMatrix[i][j][k] = alphabetIndex(plaintextMatrix[i][j][k]) 
        
    dotResult = []
    for i in range (0, len(plaintextMatrix)):
        dotResult.append(multiplyMatrix(key, plaintextMatrix[i]))
        
    for i in range (0, len(dotResult)):
        for j in range (0, len(dotResult[i])):
            for k in range (0, len(dotResult[i][j])):
                dotResult[i][j][k] = indexOfAlphabet((dotResult[i][j][k] % 26))
                
    result = ''
    for i in range (0, len(dotResult)):
        for j in range (0, len(dotResult[i])):
            for k in range (0, len(dotResult[i][j])):
                result += dotResult[i][j][k]
                
    return render_template('index.html', text=plaintext, method="hillCipher", action="", result=result)

def hillCipherDecrypt(ciphertext, key):
    determinant = int(determinantMatrix(key))
    determinant = determinant % 26
    invNum = inverseModulo(determinant, 26)
    
    adjointMatrixKey = adjointMatrix(key)
    for i in range (0, len(adjointMatrixKey)):
        for j in range (0, len(adjointMatrixKey)):
            adjointMatrixKey[i][j] *= invNum
            adjointMatrixKey[i][j] = int(adjointMatrixKey[i][j] % 26)
            
    print(key)
    print(determinant)
    print(adjointMatrix(key))
    print(invNum)
    
    return hillCipherEncrypt(ciphertext, adjointMatrixKey)
