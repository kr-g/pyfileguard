
# File Guard and Large File Guard

support for preserving the old content of a file.
support for large files provide access via `seek()` to a specific file position.

# use in own code

use `with context` and `rollback()` to rewind the changes done.

# when to use in own code

there are some typical use cases, such as:
- in test scenarios when you need to rollback for the next test case
- when wrting changed config files from your code (falls back to old state)
- when randomly accessing larger files in binary mode


# code for small files

for small files `FileGuard` makes a copy using a `TemporaryFile`.
in error case or when calling `rollback()` the file is copied back.


    import shutil
    from fileguard import FileGuard, LargeFileGuard, dumpbim


    def sample():
        
        # copy test file
        shutil.copy2("monty.bak.txt","monty.txt")

        try:
            with FileGuard("monty.txt",mode="+w",
                           always_restore=False,
                           blksize = 512,
                           debug=True,
                           ) as f:
                print("before write",f)
                f.write("content gone")
                f.flush()
                print("after write",f)
                
                raise Exception("something went wrong")
            
        except Exception as ex:
            print("err", ex)

        with open( "monty.txt", "rb" ) as f:
            c = f.read()
            print("---file content---")
            print(c)


# code for large files

for large files `LargeFileGuard` provides methods like `seek()` and `tell()`
to set the file pointer position. when writing to `LargeFileGuard` it preserves
the content of the underlying file by writing to a journal or "before-image"
file (also known as copy-on-write).
in error case or by calling `rollback()` the changes are rewinded.


    sample2():
        
        # copy test file
        shutil.copy2("monty.bak.txt","monty.txt")

        try:
            with LargeFileGuard("monty.txt","r+",
                                    always_restore=False, # always rewind
                                    keep_bim=True, # keep bim file, deleted otherwise
                                    blksize=512,
                                    debug=True,
                                ) as f:
                print("before write",f)
                f.write("!!! new content at 0 !!!")
                f.seek(100)
                f.write("!!! new content at 100 !!!")
                f.seek( 0, 2 )
                f.write("!!! new ending !!!")
                f.flush()
                print("after write",f)
                
                f.seek(0)
                c = f.read()
                print(c)
                
                # uncomment want to test...
                f.rollback()
                #raise Exception("something went wrong")
            
        except Exception as ex:
            
            print("err", ex)

        with open( "monty.txt", "rb" ) as f:
            c = f.read()
            print("---file content---")
            print(c)

        print( dumpbim("monty.txt") )

