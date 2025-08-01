CREATE DATABASE AchadosEPerdidos;

USE AchadosEPerdidos;

CREATE TABLE Pessoa (
    PessoaMatricula VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE,
    Pnome VARCHAR(100) NOT NULL,
    Contato VARCHAR(100) NOT NULL
);

CREATE TABLE Objeto (
    ObjetoID INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    Titulo VARCHAR(100) NOT NULL,
    Cor VARCHAR(50) NULL,
    Descricao TEXT NOT NULL,
    Data_encontrado DATE NOT NULL,
    Local_encontrado VARCHAR(100) NOT NULL,
    Pessoa_entregou VARCHAR(50), 
    Reinvidicado BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (Pessoa_entregou) REFERENCES Pessoa(PessoaMatricula)
);

CREATE TABLE Ocorrencia_Perda (
    OcorrenciaID INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    Tipo_objeto VARCHAR(100) NOT NULL,
    Data_perdido DATE NOT NULL,
    Local_perdido VARCHAR(100),
    Pessoa_perdeu VARCHAR(50),
    FOREIGN KEY (Pessoa_perdeu) REFERENCES Pessoa(PessoaMatricula)
);

CREATE TABLE Reivindicacao (
    ReivindicacaoID INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    Objeto_reivindicado_ID INT NOT NULL UNIQUE, 
    Pessoa_retirou VARCHAR(50),
    Ocorrencia_ID INT NULL, 
    Data_retirada DATE NOT NULL,
    FOREIGN KEY (Objeto_reivindicado_ID) REFERENCES Objeto(ObjetoID),
    FOREIGN KEY (Pessoa_retirou) REFERENCES Pessoa(PessoaMatricula),
    FOREIGN KEY (Ocorrencia_ID) REFERENCES Ocorrencia_Perda(OcorrenciaID)
);
