import os
from claimsExtractor import extractClaims
from aiClaimsValidator import validateClaim

if __name__ == "__main__":

    # Chemins
    source_dir = './AzureFoundryPhi4/AiSinistreValidator'
    output_dir = './AzureFoundryPhi4/AiSinistreValidator/extraction'
    os.makedirs(output_dir, exist_ok=True)

    # Extract claims info from PDF : FNOL/Picture/Contract
    extractClaims(source_dir,output_dir)

    # Validate claims
    sinistres = [f for f in os.listdir(output_dir) if f.endswith("_fnol.txt")]
    for sinistre_name in sinistres:
        validateClaim(output_dir, sinistre_name)