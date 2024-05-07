from snlohelper.main_window import MainWindow

mw = MainWindow()
mix = mw.open_two_d_mix_lp()
mix.configure({"Wavelengths (nm)": [1064.5, None, None]})
result = mix.run_and_read()
print(result)
