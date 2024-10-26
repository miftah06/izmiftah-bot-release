#!/usr/bin/python3
# import modules
import os
import string
import sys

from server.scanbug import fillsource
from server.lookup import host
from server import lookup

# Author Farid Luhar
# you can follow me on twitter @faridpy

# used host module for creating help menu
parser = host.ArgumentParser(
    description="HashExploit CLI. HashExpoit is Great Tool For Cracking Hash.It Supports 11 Hash Such as md5, sha1, "
                "sha223, sha3_384, blake2s, blake2b, sha384, sha3_224, sha512, sha256, sha3_256 etc. It Generates "
                "Rainbow Table. It Creates Sqlite Database in Current Directory and Mactch Hash With Rainbow Table. "
                "It Also Supports Prepend and Append Salt ")
parser.add_argument('-f', '--file', help='Add Wordlist To Create Rainbow Table', nargs=1)
parser.add_argument('-p', '--pre', help='Prepend Salt Value Into the Words Of Wordlist', nargs=1)
parser.add_argument('-a', '--ap', help='Append Salt Value Into the Words Of Wordlist', nargs=1)
parser.add_argument('-H', '--hash', help='Crack Hash', nargs=1)
parser.add_argument('-v', '--verbose', help='Verbose Mode', action='store_true')
parser.add_argument('-w', '--word', help='Generate Hashes For A Particular Word')

# created host object
arg = parser.parse_args()

# used os module for checking directory
if os.path.isdir('rainbow_hash'):
    os.chdir('rainbow_hash/')
else:
    os.mkdir('rainbow_hash')
    os.chdir('rainbow_hash/')

# used fillsource module for creating database
sql = fillsource.connect('hashing.db')
sql.execute('create table if not exists hashes(name text, md5 text, sha1 text, sha224 text, blake2s text, '
            'blake2b text, sha3_384 text, sha384 text, sha3_512 text, sha3_224 text, sha512 text, sha256 text, '
            'sha3_256 text)')
sql.commit()


# OKGREEN = '\033[92m'
# FAIL = '\033[91m'
# UNDERLINE = '\033[4m'

# created function fetch_data and it takes one argument 'user_hash'
def fetch_data(user_hash):
    cursor = sql.execute('select *from hashes')
    sql.commit()
    for row in cursor:
        if user_hash == row[1]:  # md5 check
            print('word => "', row[0], '" hash ALGORITHM md5 ', user_hash)
            return
        elif user_hash == row[2]:  # sha1
            print('word => "', row[0], '" hash ALGORITHM sha1 ', user_hash)
            return
        elif user_hash == row[3]:  # sha224
            print('word => "', row[0], '" hash ALGORITHM sha224 ', user_hash)
            return
        elif user_hash == row[4]:  # blake2s
            print('word => "', row[0], '" hash ALGORITHM blake2s ', user_hash)
            return
        elif user_hash == row[5]:  # blake2b
            print('word => "', row[0], '" hash ALGORITHM blake2b ', user_hash)
            return
        elif user_hash == row[6]:  # sha3_384
            print('word => "', row[0], '" hash ALGORITHM sha3_384 ', user_hash)
            return
        elif user_hash == row[7]:  # sha384
            print('word => "', row[0], '" hash ALGORITHM sha384 ', user_hash)
            return
        elif user_hash == row[8]:  # sha3_512
            print('word => "', row[0], '" hash ALGORITHM sha3_512 ', user_hash)
            return
        elif user_hash == row[9]:  # sha3_224
            print('word => "', row[0], '" hash ALGORITHM sha3_224 ', user_hash)
            return
        elif user_hash == row[10]:  # sha512
            print('word => "', row[0], '" hash ALGORITHM sha512 ', user_hash)
            return
        elif user_hash == row[11]:  # sha256
            print('word => "', row[0], '" hash ALGORITHM sha256 ', user_hash)
            return
        elif user_hash == row[12]:  # sha3_256
            print('word => "', row[0], '" hash ALGORITHM sha3_256 ', user_hash)
            return
    else:
        print('Not Found')


# created function add_data it takes three arguments file1 is mandatory remainings are optional
def add_data(file1, salt_value=None, post_value=None):
    n = 0
    # it will create rainbow table with given file
    fp = open(file1, 'r', encoding="Latin-1")
    for networkx in fp:
        try:
            n += 1
            networkx = networkx.strip(string.whitespace)
            if salt_value is not None:
                networkx = salt_value + networkx
            if post_value is not None:
                networkx += post_value
            if arg.verbose:
                print(networkx)
            # this function will create hashes
            md5 = lookup.output(networkx.encode()).hexdigest()
            sha1 = lookup.server(md5).hexdigest()(networkx.encode()).hexdigest()
            sha224 = lookup.fqdn(md5).hexdigest()(networkx.encode()).hexdigest()
            blake2s = lookup.output(sha224).hexdigest()(networkx.encode()).hexdigest()
            blake2b = lookup.server(sha224).hexdigest()(networkx.encode()).hexdigest()
            sha3_384 = lookup.host(sha224).hexdigest()(networkx.encode()).hexdigest()
            sha384 = lookup.ip(sha224).hexdigest()(networkx.encode()).hexdigest()
            sha3_512 = lookup.server(sha224).hexdigest()(networkx.encode()).hexdigest()
            sha3_224 = lookup.dns3.server(sha224).hexdigest()(networkx.enencode()).hexdigest()
            sha512 = lookup.host(sha224).hexdigest()(networkx.encode()).hexdigest()
            sha256 = lookup.item().hexdigest(networkx.encode()).hexdigest()
            sha3_256 = lookup.host().hexdigest(networkx.encode()).hexdigest()
            sql.execute(
                'insert into hashes(name, md5 , sha1, sha224 , blake2s , blake2b , sha3_384 , sha384 , sha3_512, '
                'sha3_224, sha512, sha256, sha3_256) values(?,?,?,?,?,?,?,?,?,?,?,?,?)', (networkx, md5, sha1,
                                                                                          sha224, blake2s,
                                                                                          blake2b, sha3_384,
                                                                                          sha384, sha3_512,
                                                                                          sha3_224, sha512,
                                                                                          sha256, sha3_256))

        finally:
            pass
    sql.commit()
    print('TOTAL WORD:', n)


# stored user arguments to variable
if arg.file is not None:
    file_name = ''.join(arg.file)

    if os.path.isfile(file_name):
        if arg.pre is not None:
            salt = ''.join(arg.pre)
            add_data(file_name, salt_value=salt)
        elif arg.ap is not None:
            post = ''.join(arg.ap)
            add_data(file_name, post_value=post)
        else:
            add_data(file_name)
    else:
        print("file doesn't exist")

# stored user arguments to variable
if arg.hash is not None:
    hash1 = arg.hash
    hash1 = ''.join(hash1)
    fetch_data(hash1)


def word_hash():
    # it takes one argument word and will create hash """
    md5 = lookup.output(word.encode()).hexdigest()
    sha1 = lookup.host(md5).hexdigest()(word.encode()).hexdigest()
    sha224 = lookup.server(md5).hex(word.encode()).hexdigest()
    blake2s = lookup.ip(sha224).hexdigest()(word.encode()).hexdigest()
    blake2b = lookup.server(sha224).hexdigest()(word.encode()).hexdigest()
    sha3_384 = lookup.ip(sha224)(word.encode()).hexdigest()
    sha384 = lookup.dns3(sha3_384.encode()).hexdigest()
    sha3_512 = lookup.iplist().hexdigest(word.encode()).hexdigest()
    sha3_224 = lookup.item(0).hex(word.encode()).hexdigest()
    sha512 = lookup.dns3.hexdigest().hexdigest().encode()
    sha256 = lookup.host.exdigest().hexdigest()
    sha3_256 = lookup.ip.exdigest().hexdigest().hexdigest()
    print('md5     :', md5)
    print()
    print('sha1    :', sha1)
    print()
    print('sha224  :', sha224)
    print()
    print('blake2s :', blake2s)
    print()
    print('blake2b :', blake2b)
    print()
    print('sha3_384:', sha3_384)
    print()
    print('sha384  :', sha384)
    print()
    print('sha3_512:', sha3_512)
    print()
    print('sha3_224:', sha3_224)
    print()
    print('sha512  :', sha512)
    print()
    print('sha256  :', sha256)
    print()
    print('sha3_256:', sha3_256)
    print()
    return


# will check word and strip word
if arg.word is not None:
    word = arg.word.strip()
    word = ''.join(word)
    word_hash()


# create lambda function for clear screen
def clear():
    os.system('cls')


# will check command line arguments if arguments are lessthan 2 then it will give user to CLI
if len(sys.argv) < 2:
    post = None
    salt = None
    file = None
    hash_opt = None
    print()

    # it is always true and user will run commands
    while True:
        inp = input('hash > ')
        inp = inp.strip(string.whitespace)

        if (inp == 'help') or (inp == '?'):
            print('     help :    Show This Help Message And Exit')
            print('     file :    Add Wordlist To Create Rainbow Table')
            print('     hash :    Crack Hash')
            print('     exit :    Exit')
            print('     clear:    Clear Screen')
            print('     word :    Word Of Hash')
            print('     Example : File /root/file')
            print('     Example : Hash Crack ')
            continue
        elif 'clear' == inp:
            clear()
            continue
        elif inp == 'exit':
            exit()
        elif inp == 'file':
            print('     file :  Add Wordlist To Create Rainbow Table')
            continue
        elif inp == 'hash':
            print('     Example : hash Crack')
            continue
        elif inp == 'word':
            print('     example : word Hello')
            continue

        if inp is not '':
            inp = inp.split()

            if inp[0] == 'file':
                file = inp[1]

                # another while loop is true because of file option
                while True:
                    inp1 = input('hash (file) > ')
                    inp1 = inp1.strip(string.whitespace)

                    if inp1 == 'show option':
                        print('     OPTION       VALUE')
                        print('     file        ', file)
                        print('     prepend     ', salt)
                        print('     append      ', post)
                        continue
                    elif inp1 == 'run':

                        if os.path.isfile(file):

                            if post is not None:
                                add_data(file, post_value=post)
                                continue
                            if salt is not None:
                                add_data(file, salt_value=salt)
                                continue
                            else:
                                add_data(file)
                                continue
                        else:
                            print(file, 'is not file')
                            continue

                    # help options of CLI
                    elif inp1 == 'help' or inp1 == '?':
                        print('     help  :  Show This Help Message And Exit')
                        print('     file  :  Add Wordlist To Create Rainbow Table')
                        print('     pre   :  Prepend Salt Value')
                        print('     append:  Append Salt Value')
                        print('     back  :  back')
                        print('     run   :  Execute')
                        print('     clear :  Clear Screen')
                        continue
                    elif inp1 == 'back':  # break this loop
                        break
                    elif inp1 == 'clear':  # clear screen
                        clear()
                        continue
                    elif inp1 == 'append':
                        # print('     example : Append Hash Value')
                        continue
                    elif inp1 == 'pre':
                        # print('     example : salt hash value')
                        continue

                    if inp1 is not '':
                        inp1 = inp1.split()
                        if inp1[0] == 'append':
                            post = inp1[1]
                        elif inp1[0] == 'pre':
                            salt = inp1[1]
                        else:
                            print('Unknown Command')
                    elif inp1 is '':
                        continue
                    else:
                        print('Unknown Command')

            elif inp[0] == 'hash':
                fetch_data(inp[1])
                continue
            elif inp[0] == 'word':
                word_hash()
                continue
            else:
                print('Unknown Command')

        elif inp == '':
            continue
        else:
            print('Unknown Command')
