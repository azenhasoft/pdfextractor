# Sistema para ler pastas no Sharepoint e extrair PDFs com documentos de identificação RG e CNH

# Criado em 27/07/2025

 

import os

import fitz  # PyMuPDF

import pytesseract

from PIL import Image

 

def extrair_documentos_de_pasta(pasta_entrada):

    pasta_saida = os.path.join(pasta_entrada, "Documentos Extraídos")

    os.makedirs(pasta_saida, exist_ok=True)

 

    contador = 1

 

    for root, dirs, files in os.walk(pasta_entrada):

        for file in files:

            if file.lower().endswith(".pdf"):

                caminho_pdf = os.path.join(root, file)

                print(f"\n📄 Processando arquivo: {caminho_pdf}")

 

                try:

                    doc = fitz.open(caminho_pdf)

 

                    for i in range(len(doc)):

                        print(f"🔍 Analisando página {i+1}...")

 

                        page = doc.load_page(i)

                        pix = page.get_pixmap(dpi=300)

                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

 

                        texto_extraido = pytesseract.image_to_string(img, lang='por', config='--psm 6')

                        texto_lower = texto_extraido.lower()

 

                        if any(p in texto_lower for p in ["carteira nacional de habilitação", "cnh", "registro geral", "identidade", "rg"]):

                            print(f"✅ Documento de identidade encontrado na página {i+1}")

 

                            novo_pdf = fitz.open()

                            novo_pdf.insert_pdf(doc, from_page=i, to_page=i)

 

                            tipo_doc = "CNH" if "habilitação" in texto_lower or "cnh" in texto_lower else "RG"

                            nome_arquivo = f"{tipo_doc}_{contador}.pdf"

                            caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

 

                            novo_pdf.save(caminho_arquivo)

                            print(f"📁 Documento salvo como: {nome_arquivo}")

 

                            contador += 1

 

                    doc.close()

 

                except Exception as e:

                    print(f"⚠️ Erro ao processar {caminho_pdf}: {e}")

 

    print(f"\n🏁 Extração concluída. {contador - 1} documentos salvos em: {pasta_saida}")

 

# ---------------------------

# USO INTERATIVO

# ---------------------------

 

if __name__ == "__main__":

    print("🧠 Extrator de RGs e CNHs escaneados de PDFs (inclusive em subpastas)")

    pasta_entrada = input("Digite o caminho da pasta onde estão os PDFs: ").strip()

 

    if os.path.exists(pasta_entrada):

        extrair_documentos_de_pasta(pasta_entrada)

    else:

        print("❌ Caminho inválido. Verifique se a pasta existe.")
