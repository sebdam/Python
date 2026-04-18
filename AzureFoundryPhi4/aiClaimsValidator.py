from openai import OpenAI
from pydantic import BaseModel
import json
import os

from azureFoundryApiClient import getClient

# 1. On définit le schéma de sortie
class CoverageVerdict(BaseModel):
    vehicule_identifie: str
    vehicule_est_couvert: bool
    cause_identifiee: str
    cause_est_couverte: bool
    explication: str
    verdict_final: str # "✅ ACCEPTE" ou "❌ REFUSE"

# 2. Exemples pour guider le LLM (Few-shot)
few_shot_coverage = """
Exemple 1 :
CONTRAT : "Covered aircrafts: Airplanes, Gliders, Helicopters, Gyrocopters. Covered: Pilot Mistakes or failures, Collision with animals or trees or environment, Mechanical due to engine issues, oil starvation, fuel exhaust, Student or instructor mistakes or failures, Unregistered plane or uncertified pilot."
SINISTRE : "Aicraft : PIPER. Cause: The pilot's failure to maintain directional control during landing in flat light conditions, resulting in the airplane to nose over."
JSON : {"vehicule_identifie": "Avion", "vehicule_est_couvert": true, "cause_identifiee": "Pilot Mistakes or failures", "cause_est_couverte": true, "explication": "Le véhicule et la cause sont dans le contrat.", "verdict_final": "✅ ACCEPTE"}
"""

response_format = """
{
    "vehicule_identifie": string        # le vehicule identifié
    "vehicule_est_couvert": boolean     # true si le véhicule est couvert, false si non
    "cause_identifiee": string          # la cause identifiée
    "cause_est_couverte": boolean.      # true si la cause est couverte, false si non
    "explication": string               # Une breve explication du verdicte final
    "verdict_final": string             # "✅ ACCEPTE" ou "❌ REFUSE"
}
"""

def validateClaim(output_dir:str, fnolFilePath: str):

    base_name = fnolFilePath.replace("_fnol.txt", "")
    path_contrat = os.path.join(output_dir, f"{base_name}_contract.txt")
    path_sinistre = os.path.join(output_dir, f"{base_name}_fnol.txt")

    with open(path_contrat, 'r', encoding='utf-8') as f:
        contrat_text = f.read()

    with open(path_sinistre, 'r', encoding='utf-8') as f:
        sinistre_text = f.read()

    # Construction du prompt avec le texte du contrat et les exemples
    instruction_prompt = f"""
    Compare et valide le SINISTRE ci-dessous
    #SINISTRE
    {sinistre_text}
    
    avec le CONTRAT ci-dessous
    #CONTRAT 
    {contrat_text}

    en produisant une réponse dans le format JSON ci-dessous
     - sans commentaires,
     - avec des caracteres d'échapement corrects
    #FORMAT
    {response_format}
    
    Un peu comme dans l'exemple ci-dessous :
    {few_shot_coverage}

    Ne produit pas de sortie dans un autre format que JSON car je ne saurait pas le lire.

    """

    deployment_name = "Phi-4"
    client = getClient()
    completion = client.chat.completions.parse(
        model = deployment_name,
        messages = [{
                'role': 'system', 
                'content': 'Tu es un expert en validation de sinistres.'
            },
            {
                'role': 'user', 
                'content': instruction_prompt
            }],
    )

    if len(completion.choices) <= 0 or completion.choices[0].message.content == None:
        print(f"No ideas for {base_name} ! Sorry...")
    else:
        try:
            jsonstr, verdict_data = getResponseData(completion)
            if verdict_data == None:
                print(f"Response parsing error:{jsonstr}")
            else:
                print(f"--- Dossier {base_name} ---")
                print(f"    Verdict : {verdict_data.verdict_final}")
                print(f"    Raison : {verdict_data.explication}")
        except Exception as e:
            print(f"--- Dossier {base_name} ---")
            print(e)
    
    if(completion.usage != None):
        print("Usage :")
        print(f"    Prompt: {completion.usage.prompt_tokens}")
        print(f"    Completion: {completion.usage.completion_tokens}")
        print(f"    -> Total: {completion.usage.total_tokens}")

def getResponseData(completion) -> tuple[str, CoverageVerdict]:
    jsonstr = completion.choices[0].message.content[8:]
    jsonstr = jsonstr[:jsonstr.index('```')]
    jsonstr = jsonstr.replace('\n','')
    jsonstr = jsonstr.replace("\'","'")
    verdict_data = CoverageVerdict.model_validate_json(jsonstr)
    return jsonstr,verdict_data