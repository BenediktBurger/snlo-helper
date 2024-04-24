from snlohelper import snlo

snlo.utils.set_screenfactors()

sim = snlo.TwoDMixLP()
sim.open()
sim.configure({"Wavelengths (nm)": [1064.5, None, None]})
result = sim.run_and_read()
print(result)
