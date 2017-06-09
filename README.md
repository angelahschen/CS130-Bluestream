# CS130-Bluestream

UCLA CS130 Project Blue-Stream

Dependencies:
    python 2_7
    Django 1.11.1
    python-magic
    
    
Install Python-magic by following instructions at https://github.com/ahupp/python-magic
    Linux:
        install should be ok, cause libmagic should be available ?
    Mac:
        install seems to be straightforward following the instructions?
    Windows:
        32 bit python:
            hasn't been attempted by those writing this documentation
        64 bit python:
            after following the instructions, edit the magic.py install
            and change the constructor for Magic (__init__) so that it's default
            magic_file is the path to your libmagic install

			eg) if using Anaconda:
				in the file: <path_to_your_anaconda_install>/lib/site-packages/magic.py
    			#OLD:
    			#def __init__(self, mime=False, magic_file=None, mime_encoding=False,
    			#             keep_going=False, uncompress=False):
    			# =================================================================
    			#New:
    			def __init__(self, mime=False, magic_file='<path_to_your_libmagic_install>\libmagicwin64\magic.mgc', mime_encoding=False,
    			             keep_going=False, uncompress=False):
