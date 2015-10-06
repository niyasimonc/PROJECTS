def palindrome(word):
    i=0
    j=-1
    while(i<9):
        if word[i]==word[j]:
            i=i+1
            j=j-1
        else:
          return False
    return True

print palindrome('malayalam')

