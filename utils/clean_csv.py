import os
import shutil


# remove '|' at the buttom of each line
def main():
    srcpath = '../csv'
    filelist = os.listdir(srcpath)
    outpath = '../clean_csv'

    shutil.rmtree(outpath)
    os.makedirs(outpath)
    for file in filelist:
        print('Processing File "{}" ...'.format(srcpath + '/' + file))
        f = open(srcpath + '/' + file)

        src_name = file.split('.')[0]
        dst_name = src_name + '.csv'

        outfile = open(outpath + '/' + dst_name, 'w')

        for line in f.readlines():
            line = line[:-2]
            outfile.write(line + '\n')

    f.close()
    outfile.close()


if __name__ == '__main__':
    main()
