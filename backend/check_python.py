import sys

print("Python executable:")
print(sys.executable)

print()

print("Python version:")
print(sys.version)

print()

try:
    import groq

    print("Groq import: OK")
    print("Groq location:")
    print(groq.__file__)

except Exception as error:

    print("Groq import FAILED")
    print(error)
    