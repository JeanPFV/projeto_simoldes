import os
from django.conf import settings
from django.shortcuts import render, redirect
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Display.OCCViewer import OffscreenRenderer

#Gerar jpegs (bom mudar o nome, to com preguiça agora)
def gerar_preview_stp_para_png(caminho_stp, caminho_png):
    
    # Leitura do arquivo STEP
    reader = STEPControl_Reader()
    status = reader.ReadFile(caminho_stp)
    if status != IFSelect_RetDone:
        raise Exception(f"Erro ao ler o arquivo STEP: {caminho_stp}")
    reader.TransferRoot()
    shape = reader.Shape()

    # Inicializa o renderizador
    renderer = OffscreenRenderer(screen_size=(640, 480))
    
    # Exibe a forma e salva diretamente no caminho da imagem, alem de settar as configurações de como o visual do modelo é feito
    renderer.DisplayShape(
        shapes=shape,
        transparency=0.7,
        dump_image=True,
        dump_image_path=os.path.dirname(caminho_png),
        dump_image_filename=os.path.basename(caminho_png)
    )

#Listar Modelos
def listar_modelos_step(request):
    
    # pega as pastas com os modelos stp e as previews(jpeg's)
    pasta_modelos = os.path.join(settings.MEDIA_ROOT, 'modelos')
    pasta_previews = os.path.join(pasta_modelos, 'previews')
    arquivos_stp = [f for f in os.listdir(pasta_modelos) if f.lower().endswith('.stp')]

    #Inicia uma lista para armazenar os stp's e jpeg's
    previews = []
    for arquivo in arquivos_stp:
        caminho_stp = os.path.join(pasta_modelos, arquivo)
        nome_imagem = arquivo.replace('.stp', '.jpeg')
        caminho_png = os.path.join(pasta_previews, nome_imagem)

        # gera apenas jpeg se ainda não existir
        if not os.path.exists(caminho_png):  
            try:
                gerar_preview_stp_para_png(caminho_stp, caminho_png)
            except Exception as e:
                print(f"Erro ao gerar preview para {arquivo}: {e}")
                continue
        
        #Cria as urls num apendice
        previews.append({
            'nome': arquivo,
            'imagem_url': f"/media/modelos/previews/{nome_imagem}"  # URL correta
        })

    # retorna o html das previews junto de um dicionarios com as previews
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