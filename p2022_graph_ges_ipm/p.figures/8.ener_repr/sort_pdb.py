# Sort pdb lines by residue ids so that residue connectivities in ChimeraX visualization is correct. 
# Zilin Song, 03 May 2022
# 
def sort_pdb(indir:str, resid:int):
  pdb_in=f'{indir}/r{resid}.pdb'
  pdb_out=f'{indir}_sorted/r{resid}.pdb'
  lines=open(pdb_in, 'r').readlines()
  file_out=open(pdb_out,'w')

  for i in range(0,300):
    for line in lines:
      if line.split()[0]=='ATOM' and line.split()[4]==str(i):
        file_out.write(line)

for fname in ['d1_f22', 'd2_f22']:
  for i in range(1,37):
    print(fname, i)
    sort_pdb(fname, i)
