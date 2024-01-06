import tkinter as tk
from tkinter import messagebox


class JogoDaVelha:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jogo da Velha")
        self.tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
        self.jogador_atual = "X"
        self.criar_interface()

    def criar_interface(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", font=('normal', 20), width=5, height=2,
                                   command=lambda i=i, j=j: self.realizar_jogada(i, j))
                button.grid(row=i, column=j)

    def realizar_jogada(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == " ":
            self.tabuleiro[linha][coluna] = "X"
            self.atualizar_interface(linha, coluna)

            if self.verificar_vitoria("X"):
                messagebox.showinfo("Fim de Jogo", "Parabéns! Você venceu!")
                self.resetar_jogo()
            elif all(self.tabuleiro[i][j] != " " for i in range(3) for j in range(3)):
                messagebox.showinfo("Fim de Jogo", "Empate! O jogo terminou sem vencedores.")
                self.resetar_jogo()
            else:
                # Vez da IA minimax jogar
                self.root.after(1000, self.jogada_ia_minimax_com_atraso)  # Atraso de 1 segundos

    def jogada_ia_minimax_com_atraso(self):
        linha, coluna = self.jogar_ia_minimax()
        self.tabuleiro[linha][coluna] = "O"
        self.atualizar_interface(linha, coluna)

        if self.verificar_vitoria("O"):
            messagebox.showinfo("Fim de Jogo", "A IA minimax venceu!")
            self.resetar_jogo()
        elif all(self.tabuleiro[i][j] != " " for i in range(3) for j in range(3)):
            messagebox.showinfo("Fim de Jogo", "Empate! O jogo terminou sem vencedores.")
            self.resetar_jogo()
        else:
            # Vez do jogador jogar
            pass

    def jogar_ia_minimax(self):
        _, (linha, coluna) = self.minimax(self.tabuleiro, "O")
        return linha, coluna

    def minimax(self, tabuleiro, jogador):
        if self.verificar_vitoria("X"):
            return -1, None
        elif self.verificar_vitoria("O"):
            return 1, None
        elif all(tabuleiro[i][j] != " " for i in range(3) for j in range(3)):
            return 0, None

        movimentos = []
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == " ":
                    tabuleiro[i][j] = jogador
                    pontuacao, _ = self.minimax(tabuleiro, "X" if jogador == "O" else "O")
                    tabuleiro[i][j] = " "
                    movimentos.append((pontuacao, (i, j)))

        if jogador == "O":
            return max(movimentos)
        else:
            return min(movimentos)

    def atualizar_interface(self, linha, coluna):
        button = self.root.grid_slaves(row=linha, column=coluna)[0]
        button.config(text=self.tabuleiro[linha][coluna], state=tk.DISABLED)

    def verificar_vitoria(self, jogador):
        for i in range(3):
            if all(self.tabuleiro[i][j] == jogador for j in range(3)) or \
               all(self.tabuleiro[j][i] == jogador for j in range(3)):
                return True

        if all(self.tabuleiro[i][i] == jogador for i in range(3)) or \
           all(self.tabuleiro[i][2 - i] == jogador for i in range(3)):
            return True

        return False

    def resetar_jogo(self):
        for i in range(3):
            for j in range(3):
                button = self.root.grid_slaves(row=i, column=j)[0]
                button.config(text="", state=tk.NORMAL)
                self.tabuleiro[i][j] = " "

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    jogo = JogoDaVelha()
    jogo.iniciar()
