
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
            
            # uncomment want to test...
            f.rollback()
            raise Exception("something went wrong")
        
    except Exception as ex:
        
        print("err", ex)

    with open( "monty.txt", "rb" ) as f:
        c = f.read()
        print("---file content---")
        print(c)

    print( dumpbim("monty.txt") )


if __name__=='__main__':
    #sample()
    sample2()
    
    