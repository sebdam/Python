import fitz
import os

def extractClaims(source_dir:str, output_dir:str):
    for file_name in os.listdir(source_dir):
        if file_name.endswith(".pdf"):
            # Ouverture du document avec fitz
            doc = fitz.open(os.path.join(source_dir, file_name))
            base_name = file_name.replace(".pdf", "")

            # --- ÉTAPE 2.1 : Extraction des Textes ---
            # Page 1 : FNOL
            fnol_text = doc[0].get_text()
            with open(f"{output_dir}/{base_name}_fnol.txt", "w") as f:
                f.write(str(fnol_text))

            # --- ÉTAPE 2.2 : Extraction de l'Image ---
            # Page 2 : Photo du sinistre
            if len(doc) > 1:
                page_photo = doc[1]
                images = page_photo.get_images(full=True)

                if images:
                    xref = images[0][0]
                    pix = fitz.Pixmap(doc, xref)
                    # Conversion en RGB si nécessaire (pour éviter les couleurs bizarres)
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    pix.save(f"{output_dir}/{base_name}_photo.png")
                pix = None

            # --- ÉTAPE 2.3 : Extraction du texte du contrat ---
            # Page 3 : Contrat
            if len(doc) > 2:
                contract_text = doc[2].get_text()
                with open(f"{output_dir}/{base_name}_contract.txt", "w") as f:
                    f.write(str(contract_text))

            doc.close()