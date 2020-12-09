from distutils.core import setup, Extension

# This setup file is needed to compile the C++ extension for the version of 
# python that you are running. This is the MacOS version of the setup file, 
# which is needed because some extra linker and compiler arguments are required 
# by the clang compiler used in MacOS
def main():
    extra_link_args=["-stdlib=libc++", '-mmacosx-version-min=10.9']
    setup(  name="dp_distance",
            version="1.0.0",
            description="Implements edit distance between two sequences",
            author="Pasindu Tennakoon",
            author_email="ppt8251@truman.edu",
            ext_modules=[
                Extension("dp_distance", ['distance.cpp'],
                extra_compile_args=["-stdlib=libc++", '-mmacosx-version-min=10.9', 
                    '-O3'],
                extra_link_args=extra_link_args)],
        )

if __name__ == '__main__':
    main()
