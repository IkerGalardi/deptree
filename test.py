import deptree

def test_parse_ldd_output(case, expected):
    string = ''
    with open(case, 'r') as file:
        string = file.read()

    deps = deptree.parse_ldd_output(string)
    if deps != expected:
        print('')
        print(f'[X] parse_lld_output test failed on case \'{case}\':')
        print(f'    Expected:\n      {expected}')
        print(f'    Got:\n      {deps}')
        print('')
    else:
        print(f'[✓] parse_lld_output test succeded on case \'{case}\'')

test_parse_ldd_output('testcases/ls-deps', ['/lib64/libselinux.so.1', '/lib64/libcap.so.2', '/lib64/libc.so.6', '/lib64/libpcre2-8.so.0'])
test_parse_ldd_output('testcases/bash-deps', ['/lib64/libtinfo.so.6', '/lib64/libc.so.6'])