from distutils.core import setup, Extension

def main():
    setup(  name="dp_distance",
            version="1.0.0",
            description="Implements edit distance between two sequences",
            author="Pasindu Tennakoon",
            author_email="ppt8251@truman.edu",
            ext_modules=[
                Extension("dp_distance", ['distance.cpp'],
                extra_compile_args=['-O3'])]
        )

if __name__ == '__main__':
    main()