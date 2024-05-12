DERIVED_MEASUREMENT_UNITS_SIMBOLS = {
    "kg*(m/(s²))":"N",
    "(m/(s²))*kg":"N",
    "N*m":"J",
    "m*N":"J",
    "(m/s)/s":"m/(s²)"
}

def rewrite_measurement_unit(mu1: str, mu2: str, op:str):
    print(mu1, mu2)
    if mu1==None:
        return mu2
    elif mu2==None:
        return mu1
    
    if "*" in mu1 or "/" in mu1:
        mu1=f"({mu1})"
    if "*" in mu2 or "/" in mu2:
        mu2=f"({mu2})"
        
    if f"{mu1}{op}{mu2}" in DERIVED_MEASUREMENT_UNITS_SIMBOLS.keys():
        return DERIVED_MEASUREMENT_UNITS_SIMBOLS[f"{mu1}{op}{mu2}"]
    else:
        return f"{mu1}{op}{mu2}"
