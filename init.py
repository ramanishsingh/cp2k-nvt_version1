import signac
  
####Project declaration ####
iodine = signac.init_project('iodine')

with open("iodine.inp","r") as f:
        Temp= [];
        N=[];
        L=[];
        for i,line in enumerate(f):
                if i>0:
                        clean_line = line.strip().split()
                        
                        temp = float(clean_line[2])
                        Temp.append(temp)
                        N.append(int(clean_line[0]))
                        L.append(float(clean_line[1]))

for i in range(len(Temp)):
    point={'Temp':Temp[i],'N':N[i],'L':L[i]}
    iodine.open_job(point).init()
