import multiprocessing as mp

dfr,dfw = mp.Pipe()

dfw.send("test")

print(dfr.recv())
print(dfr.recv())