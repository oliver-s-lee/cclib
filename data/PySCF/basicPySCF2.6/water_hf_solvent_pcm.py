from pyscf import gto, scf, solvent

def calculate():
    mol = gto.M(atom = """
    O         -0.00000       -0.11916        0.00000
    H         -0.79065        0.47664        0.00000
    H          0.79065        0.47664       -0.00000
    """, basis = "STO-3G", symmetry = True)
    
    scf_steps = []
    def store_intermediate(_locals):
        scf_steps.append({
            "e_tot": _locals["e_tot"],
            "norm_gorb": _locals["norm_gorb"],
            "conv_tol": _locals["conv_tol"],
            "conv_tol_grad": _locals["conv_tol_grad"],
        })

    method = scf.HF(mol)
    method.callback = store_intermediate
    
    method = solvent.PCM(method)
    method.with_solvent.method = "IEF-PCM"
    # Toluene
    method.with_solvent.eps = 2.3741
    
    method.kernel()
    
    return {
        'methods': [method],
        'scf_steps': [scf_steps],
    }

if __name__ == "__main__":
    calculate()