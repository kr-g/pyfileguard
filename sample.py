
import os
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


def sample2():
    
    # copy test file
    shutil.copy2("monty.bak.txt","monty.txt")
    try:
        os.remove("monty.txt.bim")
    except Exception as ex:
        print(ex)

    try:
        with LargeFileGuard("monty.txt","r+",
                                always_restore=False,
                                keep_bim=True,
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
            
            # rollback but no bim removal!
            f.rollback()
        
    except Exception as ex:
        
        print("err", ex)

    with open( "monty.txt", "rb" ) as f:
        c = f.read()
        print("---file content---")
        print(c)

    print( dumpbim("monty.txt") )


def sample3():
    
    # copy test file
    shutil.copy2("monty.bak.txt","monty.txt")
    try:
        os.remove("monty.txt.bim")
    except Exception as ex:
        print(ex)

    try:
        with LargeFileGuard("monty.txt","r+",
                                always_restore=False,
                                keep_bim=True,
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
            
            raise Exception("something went wrong")
        
    except Exception as ex:
        
        print("err", ex)

    with open( "monty.txt", "rb" ) as f:
        c = f.read()
        print("---file content---")
        print(c)

    print( dumpbim("monty.txt") )

    # open existing bim and rollback changes

    with LargeFileGuard("monty.txt","r+",
                            bimfile = "monty.txt.bim", # external bim file name
                            always_restore=False,
                            #keep_bim=True,
                            blksize=512,
                            debug=True,
                        ) as f:
        f.rollback()


def compare():
    with open("monty.bak.txt","rb") as f:
        old_content = f.read()
    with open("monty.txt","rb") as f:
        new_content = f.read()
    return old_content == new_content


if __name__=='__main__':
    #sample()
    #sample2()
    sample3()
    print("eq:", compare() )
    