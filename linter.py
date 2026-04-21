import hashlib

def search_in_file(filename, keyword):
    f = open(filename, "r")
    lines = f.read().split("\n")
    f.close()
    
    unused = 42 #неиспользуемая
    
    for i in range(len(lines)):
        if keyword in lines[i]:
            #слабый хеш MD5
            h = hashlib.md5(lines[i].encode())
            print(f"Line {i+1}: {lines[i]}")

def main():
    file = "test.txt"
    kw = input("Keyword: ")
    search_in_file(file, kw)

if __name__ == "__main__":
    main()