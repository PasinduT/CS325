from distutils.core import setup, Extension

def main():
    extra_link_args=["-stdlib=libc++", '-mmacosx-version-min=10.9']
    setup(  name="dp_distance",
            version="1.0.0",
            description="something much ado about Nothing",
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
