#!/usr/bin/env python3

import os

import click


@click.group()
def main():
    pass


@main.command()
@click.argument('package_dir')
@click.argument('tests_dir')
@click.option('-c', '--create', is_flag=True, default=False)
def compare(package_dir, tests_dir, create):
    def _compare_folders(pkgdir, testdir, depth=0):

        def _msg(*a, **kw):
            text = '{}{}'.format(' ' * depth * 4, ' '.join(a))
            click.echo(text, **kw)

        def _err(*a, **kw):
            kw.setdefault('fg', 'red')
            return _msg(*a, **kw)

        if not os.path.exists(os.path.join(pkgdir, '__init__.py')):
            _err('Not a package: {}'.format(pkgdir))
            return

        all_pkgfiles = sorted(os.listdir(pkgdir))
        pkg_dirs = [d for d in all_pkgfiles
                    if os.path.isdir(os.path.join(pkgdir, d))
                    and os.path.exists(os.path.join(pkgdir, d, '__init__.py'))]
        pkg_modules = [x for x in all_pkgfiles
                       if x.endswith('.py') and
                       os.path.isfile(os.path.join(pkgdir, x))]

        DIR_PREFIX = '\x1b[1;38;5;196mPKG\x1b[0m'
        MOD_PREFIX = '\x1b[1;38;5;214mMOD\x1b[0m'
        DIR_FMT = '\x1b[38;5;248m''{}/''\x1b[1;38;5;255m''{}''\x1b[0m'
        MOD_FMT = '\x1b[38;5;248m''{}/''\x1b[1;38;5;255m''{}''\x1b[0m'

        for name in pkg_dirs:
            full_name = os.path.join(pkgdir, name)
            testdir_name = os.path.join(testdir, 'test_' + name)

            _msg(DIR_PREFIX, DIR_FMT.format(pkgdir, name), ' ', nl=False)
            if os.path.exists(testdir_name):
                click.echo('\x1b[38;5;34m*** OK ***\x1b[0m')
            else:
                click.echo('\x1b[38;5;160mNOT FOUND\x1b[0m')

                if create and click.confirm('Create package?', default=False):
                    os.mkdir(testdir_name)
                    with open(os.path.join(testdir_name, '__init__.py'), 'w'):
                        pass  # TOUCH!

            _compare_folders(full_name, testdir_name, depth=depth + 1)

        for name in pkg_modules:
            full_name = os.path.join(pkgdir, name)

            if name == '__init__.py':
                testfile_name = os.path.join(testdir, '__init__.py')
            else:
                testfile_name = os.path.join(testdir, 'test_' + name)

            _msg(MOD_PREFIX, MOD_FMT.format(pkgdir, name), ' ', nl=False)

            if os.path.exists(testfile_name):
                click.echo('\x1b[38;5;34m*** OK ***\x1b[0m')
            else:
                click.echo('\x1b[38;5;160mNOT FOUND\x1b[0m')
                if create and click.confirm('Create module?', default=False):
                    with open(testfile_name, 'w'):
                        pass  # TOUCH!

    _compare_folders(package_dir, tests_dir)


if __name__ == '__main__':
    main()
