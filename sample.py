
import os
import shutil
from fileguard import FileGuard, LargeFileGuard, GuardJournal, dumpbim


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


def sample4():
    
    "guard journal basic usage"
    
    # copy test file
    shutil.copy2("monty.bak.txt","monty.txt")

    try:

        with GuardJournal(debug=True) as gj:
            
            with LargeFileGuard("monty.txt","r+",
                                    always_restore=False,
                                    keep_bim=True, # with fileguard always open with True!
                                    blksize=512,
                                    debug=True,
                                ) as f:
                
                # add largefileguard to journal
                gj.add(f)
                
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
                
                print( dumpbim("monty.txt") )
     
           # not in with scope above
            # comment out to commit
            raise Exception("something went wrong")
            
    except Exception as ex:
        print(ex)


def sample5():
    
    "guard journal multiple file usage"
    
    # copy test file
    shutil.copy2("monty.bak.txt","monty.txt")
    shutil.copy2("monty.bak.txt","monty2.txt")

    try:

        with GuardJournal(debug=True) as gj:
 
            print("-"*37,"monty")            

            with LargeFileGuard("monty.txt","r+",
                                    always_restore=False,
                                    keep_bim=True, # with fileguard always open with True!
                                    blksize=512,
                                    debug=True,
                                ) as f:
                
                # add largefileguard to journal
                gj.add(f)
                
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
                
                print( dumpbim("monty.txt") )
                
                # auto commit with suite

            print("-"*37,"monty2")            

            with LargeFileGuard("monty2.txt","r+",
                                    always_restore=False,
                                    keep_bim=True, # with fileguard always open with True!
                                    blksize=512,
                                    debug=True,
                                ) as f:
                
                # add largefileguard to journal
                gj.add(f)
                
                print("before write",f)
                f.write("!!! monty2 new content at 0 !!!")
                f.seek(100)
                f.write("!!! monty2 new content at 100 !!!")
                f.seek( 0, 2 )
                f.write("!!! monty2 new ending !!!")
                f.flush()
                print("after write",f)
                
                f.seek(0)
                c = f.read()
                print(c)
                
                print( dumpbim("monty2.txt") )

                # auto commit with suite

            # guard journal with scope 
            # comment out to commit, otherwise rollback monty and monty2 
            raise Exception("something went wrong")
            
    except Exception as ex:
        print(ex)

    print("eq monty2:", compare("monty2.txt") )


def compare(fnam="monty.txt"):
    print("compare", fnam )
    with open("monty.bak.txt","rb") as f:
        old_content = f.read()
    with open(fnam,"rb") as f:
        new_content = f.read()
    return old_content == new_content


if __name__=='__main__':
    #sample()
    #sample2()
    #sample3()
    #sample4()
    sample5()
    print("eq:", compare() )
    