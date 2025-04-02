#include <SDL2/SDL.h>
#include <stdio.h>

int main() {
    // Inicializa a SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL não pode ser inicializada! Erro: %s\n", SDL_GetError());
        return 1;
    }

    // Cria a janela
    SDL_Window *window = SDL_CreateWindow("Quadrado com SDL2",
                                          SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                          640, 480, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("A janela não pôde ser criada! Erro: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Cria o renderer para desenhar
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Não foi possível criar o renderer! Erro: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Define a cor do quadrado (vermelho)
    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);  // Red

    // Desenha um quadrado (x, y, largura, altura)
    SDL_Rect square = {200, 150, 100, 100}; // Posição e tamanho do quadrado
    SDL_RenderFillRect(renderer, &square);

    // Exibe o que foi desenhado
    SDL_RenderPresent(renderer);

    // Aguarda 5 segundos antes de fechar
    SDL_Delay(5000);

    // Limpeza e encerramento
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}