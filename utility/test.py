full_dicto = {"root": {"aa" : {"aaa": {},
                          "aab" : {}
                          }
                  }
        , "b": 2}

current_path = {"root": {"aa" : {"aaa": {"aaaa": "test1",
                                  "aaab": "test2"},
                                }
                        }
}

print(full_dicto)
print(current_path)
full_dicto.update(current_path)
print(full_dicto)