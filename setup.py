import cx_Freeze

exe = [cx_Freeze.Executable("Dimensions.py", base = "Win32GUI")] # <-- HERE

cx_Freeze.setup(
    name = "Mizatorian LM0B 20",
    version = "1.0",
    options = {"build_exe": {"packages": ["pygame", "random", "math", "sys"],  
        "include_files": ["music.mid","bounce.wav","crash.wav","wall.wac","at01.ttf"]}},
    executables = exe
) 