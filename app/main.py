import pytesseract as tesseract
import cv2
import numpy as py
from app.utilidades import validacao_codigo_boleto, padroes_comuns_fraude, detectar_image_manipulacao,destaque_areas_suspeitas

def analise_boleto(imagem):
    try:
        ##Converter em uma escala de cinza
        cinza = cv2.cvtColor(imagem,cv2.COLOR_BAYER_BGGR2GRAY)

        #Aplicando o Google TOCR
        extracao_de_texto = tesseract.image_to_string(cinza)

        #Validação do código de barras do boleto//indentificar se é fraude.
        e_valido, mensagem = validacao_codigo_boleto(extracao_de_texto)
        padroes_fraude = padroes_comuns_fraude(extracao_de_texto)
        manipulacao_detectada = detectar_image_manipulacao(extracao_de_texto)

        ##Destaque de areas suspeitas e coletamento de informações.
        imagem_marcada, areas_suspeitas = destaque_areas_suspeitas(imagem, extracao_de_texto)

        #Checagem de indicadores de fraudes
        e_fraude = not e_valido or padroes_fraude or manipulacao_detectada 
        razoes = []
        if not e_valido:
            razoes.append(f"Código de barra inválido: {mensagem}")
        if padroes_fraude:
            razoes.append("Palavras chaves suspeitas no texto.")
        if manipulacao_detectada:
            razoes.append("Possivel Manipulação encontrada nop texto.")

        ## Resultados finais esperados para mais informações.
        return {
            "fraude_detectada": e_fraude,
            "message": " | ".join(razoes) if e_fraude else "O boleto parece ser verdadeiro.",
            "imagem_marcada": imagem_marcada,
            "areas_suspeitas": areas_suspeitas,
            "extracao_de_texto": extracao_de_texto,
            "detalhes_fraude": {
                "codigo_de_barras_invalido": not e_valido,
                "chaves_suspeitas": padroes_fraude,
                "manipulacao_de_imagens": manipulacao_detectada
            }
        }
    except Exception as e:
        return{
            "Fraude_detectada": True,
            "messagem": f"erro no processamento do boleto: {str(e)}",
            "imagem_marcada": imagem,
            "areas_suspeitas": [],
            "extracao_de_texto": "",
            "detalhes_fraude": {
                "codigo_de_barras_invalido": False,
                "chaves_suspeitas": False,
                "manipulacao_de_imagens": False,
                "erro": str(e)
            }
        }
    



