################################################################################
#author: RD Galang
#desc: takes directories as input and for each directory creates an MPC
#      playlist consisting of all audio-files within
#TODO: -'a' flag to direct program to create playlists for all
#       subdirectories
#      -'o' flag to specify output directory
################################################################################

import os, sys
import glob

def main(argv):
    formats = ['*.mp3', '*.aac', '*.ogg']
    for arg in argv:
        if arg[-1] != os.sep:
            arg += os.sep

        pname = arg.split(os.sep)[-2] #make the playlist the same name as the 
                                      #directory

        with open(arg + pname + '.mpcpl', encoding='utf-8', mode='w') as pl:
            pl.write('MPCPLAYLIST\n')
        for fmt in formats:
            files = glob.glob(arg + fmt)

            with open(arg + pname + '.mpcpl', encoding='utf-8', mode='a') as pl:
                for i, f in enumerate(files):
                    track_no = str(i + 1)
                    pl.write(track_no + ',type,0\n')
                    pl.write(track_no + ',filename,' + f + '\n')
            


if __name__ == '__main__':
    main(sys.argv[1:])
