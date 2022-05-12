# extract pathway pdbs. 
inpsf="../../5.representative_conf/ener_path/ges_imi.d1.path_f22.psf"
incor="../../5.representative_conf/ener_path/ges_imi.d1.path_f22.cor"
outdir="d1_f22"
outpsf="d1_f22.psf"
outdcd="d1_f22.dcd"

mkdir -p $outdir
charmm inpsf:$inpsf incor:$incor outdcd:$outdcd outdir:$outdir outpsf:$outpsf < mkpdb.inp

inpsf="../../5.representative_conf/ener_path/ges_imi.d2.path_f22.psf"
incor="../../5.representative_conf/ener_path/ges_imi.d2.path_f22.cor"
outdir="d2_f22"
outpsf="d2_f22.psf"
outdcd="d2_f22.dcd"

mkdir -p $outdir
charmm inpsf:$inpsf incor:$incor outdcd:$outdcd outdir:$outdir outpsf:$outpsf < mkpdb.inp
