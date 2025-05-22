import os
from django.conf import settings
from django.shortcuts import render, redirect
from multiprocessing import Pool, cpu_count

# Bibliotecas da OCC (OpenCascade) para ler arquivos STEP e renderizar imagens
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Display.OCCViewer import OffscreenRenderer

# Função responsável por gerar a imagem (preview) a partir de um arquivo .stp
def gerar_preview_stp_para_png(caminho_stp, caminho_png):
    # Cria o leitor para arquivos STEP
    reader = STEPControl_Reader()
    status = reader.ReadFile(caminho_stp)
    
    # Verifica se o arquivo foi lido com sucesso
    if status != IFSelect_RetDone:
        raise Exception(f"Erro ao ler o arquivo STEP: {caminho_stp}")
    
    # Transfere o conteúdo do arquivo STEP para a variável shape (forma 3D)
    reader.TransferRoot()
    shape = reader.Shape()

    # Inicializa o renderizador offscreen (sem janela gráfica)
    renderer = OffscreenRenderer(screen_size=(640, 480))

    # Exibe o modelo 3D e salva a imagem no caminho indicado
    renderer.DisplayShape(
        shapes=shape,
        transparency=0.7,
        dump_image=True,
        dump_image_path=os.path.dirname(caminho_png),
        dump_image_filename=os.path.basename(caminho_png)
    )

# Função chamada em paralelo para cada arquivo STEP
def processar_preview(arquivo_info):
    # Desempacota os dados
    pasta_modelos, pasta_previews, arquivo = arquivo_info

    # Define os caminhos para o arquivo STEP e a imagem JPEG correspondente
    caminho_stp = os.path.join(pasta_modelos, arquivo)
    nome_imagem = arquivo.replace('.stp', '.jpeg')
    caminho_png = os.path.join(pasta_previews, nome_imagem)

    try:
        # Só gera nova imagem se não existir ou se o arquivo .stp foi modificado mais recentemente
        if not os.path.exists(caminho_png) or os.path.getmtime(caminho_stp) > os.path.getmtime(caminho_png):
            gerar_preview_stp_para_png(caminho_stp, caminho_png)

        # Retorna um dicionário com as informações que serão exibidas no HTML
        return {
            'nome': arquivo,
            'imagem_url': f"/media/modelos/previews/{nome_imagem}"
        }

    except Exception as e:
        # Caso algo dê errado, mostra o erro no terminal e retorna None
        print(f"Erro ao gerar preview para {arquivo}: {e}")
        return None

# View do Django que lista os modelos e seus previews
def listar_modelos_step(request):
    # Define o caminho para a pasta com os modelos (.stp)
    pasta_modelos = os.path.join(settings.MEDIA_ROOT, 'modelos')
    
    # Pasta onde serão salvas as imagens (previews)
    pasta_previews = os.path.join(pasta_modelos, 'previews')
    os.makedirs(pasta_previews, exist_ok=True)  # Cria se não existir

    # Lista todos os arquivos .stp na pasta
    arquivos_stp = [f for f in os.listdir(pasta_modelos) if f.lower().endswith('.stp')]

    # Prepara os dados que serão enviados para cada processo (arquivo + pastas)
    args = [(pasta_modelos, pasta_previews, arquivo) for arquivo in arquivos_stp]

    # Cria um pool de processos para acelerar o processamento usando múltiplos núcleos
    with Pool(processes=cpu_count()) as pool:
        resultados = pool.map(processar_preview, args)

    # Remove da lista os arquivos que falharam (None)
    previews = [r for r in resultados if r]

    # Renderiza a página HTML com as imagens geradas
    return render(request, 'visualizador/preview.html', {'previews': previews})

# Metodo de Login
def login(request):
    
    # pega o login e senha
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # é pra pegar o nome e senha, ver se é identica e dai dá acesso
        if username == 'admin' and password == '1234':
            request.session['usuario'] = 'admin'
        else:
            request.session['usuario'] = 'visualizador'
            
        return redirect('pagina_principal')

    return render(request, 'login/login.html')

# funcao para aparecer a tela incial
def pagina_principal(request):
    
    #ve se o usuario pode editar(usuario) ou nao(visualizador)
    usuario = request.session.get('usuario', 'visualizador')
    pode_editar = (usuario == 'admin')
    
    return render(request, 'tela_principal/principal.html', {'pode_editar': pode_editar})

# puxar a checklist
def checklist(request):
    
    return render(request, 'checklist/checklist.html')