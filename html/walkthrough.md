# Walkthrough — cap1.html Dynamic Loader

## O que foi feito

Reescrito [cap1.html](file:///d:/GOOGLE%20DRIVE/1%20-%20RPG/Legends%20in%20the%20Mist/Tradução/THE%20HERO/Markdown/html/cap1.html) para carregar dinamicamente o conteúdo dos 7 arquivos HTML da pasta.

### Funcionalidades implementadas

| Recurso | Descrição |
|---------|-----------|
| **Carregamento dinâmico** | `fetch()` busca cada arquivo e injeta a div `.book-container` na ordem correta |
| **Menu flutuante hierárquico** | Botão ☰ abre painel lateral com h1 → h2 → h3 indentados, com separadores entre seções |
| **Scroll suave** | Clicar num item do menu rola suavemente até o heading correspondente |
| **Scroll Spy** | Destaca no menu o heading atualmente visível conforme o usuário rola |
| **Barra de progresso** | Fina barra no topo mostra % de leitura da página |
| **Overlay + Escape** | Menu fecha ao clicar fora ou pressionar Esc |

### Arquivos modificados

- ✅ [cap1.html](file:///d:/GOOGLE%20DRIVE/1%20-%20RPG/Legends%20in%20the%20Mist/Tradu%C3%A7%C3%A3o/THE%20HERO/Markdown/html/cap1.html) — reescrito (todo JS/CSS inline, sem arquivos novos)
- ❌ Nenhum dos 7 arquivos HTML de conteúdo foi alterado
- ❌ [style.css](file:///d:/GOOGLE%20DRIVE/1%20-%20RPG/Legends%20in%20the%20Mist/Tradu%C3%A7%C3%A3o/THE%20HERO/Markdown/html/style.css) não foi alterado

### Headings filtrados

O menu ignora h1/h2/h3 dentro de cards (`.card-origin`, `.card-adventure`, etc.) e `.themebook-block` / `.trope-block` para manter a navegação limpa e focada nos títulos de seção.

## Verificação

Testado no browser via `http-server` local:
- ✅ Todos os 7 arquivos carregam na ordem correta
- ✅ Menu exibe headings hierarquicamente
- ✅ Scroll suave funciona ao clicar nos itens
- ✅ Menu fecha após seleção e ao clicar fora

> [!NOTE]
> A página requer um servidor HTTP para funcionar (o `fetch()` não opera com `file://`). Use Live Server no VS Code ou `npx http-server . -p 8091` na pasta html.

## Gravação do teste

![Teste no browser](C:/Users/mauri/.gemini/antigravity/brain/77f01157-97be-448c-9365-10b8bd1f3254/cap1_verification_1772337138755.webp)
