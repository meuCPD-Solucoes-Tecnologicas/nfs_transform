-- Active: 1681754446966@@127.0.0.1@3306
DELETE FROM nNFs_PRODUCAO_Serie1;
DELETE FROM nNFs_HOMOLOGACAO_Serie1;
DELETE FROM nNFs_PRODUCAO_Serie2;
DELETE FROM nNFs_HOMOLOGACAO_Serie2;

-- select sqlite_version();

DROP TABLE IF EXISTS nNFs_PRODUCAO_Anulados;
DROP TABLE IF EXISTS nNFs_PRODUCAO_Serie1;
DROP TABLE IF EXISTS nNFs_HOMOLOGACAO_Serie1;
DROP TABLE IF EXISTS nNFs_PRODUCAO_Serie2;
DROP TABLE IF EXISTS nNFs_HOMOLOGACAO_Serie2;

CREATE TABLE
    nNFs_PRODUCAO_Anulados(
        id INTEGER PRIMARY KEY NOT NULL,
        nnf_complementar INTEGER,
        nnf_original INTEGER NOT NULL,
        chave_acesso_nota_original TEXT NOT NULL CHECK(
            length(chave_acesso_nota_original) == 44
        ),
        chave_acesso_nota_complementar TEXT CHECK(
            length(
                chave_acesso_nota_complementar
            ) == 44
        ),
        criado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        anulado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        atualizado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        enviado_em TIMESTAMP,
        xml_nota_original TEXT NOT NULL,
        xml_nota_complementar TEXT NULL,
        xml__recibo_nota_complementar TEXT NULL
    );

CREATE TABLE
    nNFs_PRODUCAO_Serie1(
        nnf_complementar INTEGER PRIMARY KEY NOT NULL,
        nnf_original INTEGER UNIQUE NOT NULL,
        chave_acesso_nota_original TEXT NOT NULL UNIQUE CHECK(
            length(chave_acesso_nota_original) == 44
        ),
        chave_acesso_nota_complementar TEXT UNIQUE NULL CHECK(
            length(
                chave_acesso_nota_complementar
            ) == 44
        ),
        criado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        atualizado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        enviado_em TIMESTAMP,
        xml_nota_original TEXT NOT NULL,
        xml_nota_complementar TEXT NULL,
        xml__recibo_nota_complementar TEXT NULL
        
    );

CREATE TABLE
     nNFs_HOMOLOGACAO_Serie1(
        nnf_complementar INTEGER PRIMARY KEY NOT NULL,
        nnf_original INTEGER UNIQUE NOT NULL,
        chave_acesso_nota_original TEXT NOT NULL UNIQUE CHECK(
            length(chave_acesso_nota_original) == 44
        ),
        chave_acesso_nota_complementar TEXT UNIQUE NULL CHECK(
            length(
                chave_acesso_nota_complementar
            ) == 44
        ),
        criado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        atualizado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        enviado_em TIMESTAMP,
        xml_nota_original TEXT NOT NULL,
        xml_nota_complementar TEXT NULL,
        xml__recibo_nota_complementar TEXT NULL
    );
CREATE TABLE
    nNFs_PRODUCAO_Serie2(
        nnf_complementar INTEGER PRIMARY KEY NOT NULL,
        nnf_original INTEGER UNIQUE NOT NULL,
        chave_acesso_nota_original TEXT NOT NULL UNIQUE CHECK(
            length(chave_acesso_nota_original) == 44
        ),
        chave_acesso_nota_complementar TEXT UNIQUE NULL CHECK(
            length(
                chave_acesso_nota_complementar
            ) == 44
        ),
        criado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        atualizado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        enviado_em TIMESTAMP,
        xml_nota_original TEXT NOT NULL,
        xml_nota_complementar TEXT NULL,
        xml__recibo_nota_complementar TEXT NULL
    );

CREATE TABLE
     nNFs_HOMOLOGACAO_Serie2(
        nnf_complementar INTEGER PRIMARY KEY NOT NULL,
        nnf_original INTEGER UNIQUE NOT NULL,
        chave_acesso_nota_original TEXT NOT NULL UNIQUE CHECK(
            length(chave_acesso_nota_original) == 44
        ),
        chave_acesso_nota_complementar TEXT UNIQUE NULL CHECK(
            length(
                chave_acesso_nota_complementar
            ) == 44
        ),
        criado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        atualizado_em TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
        enviado_em TIMESTAMP,
        xml_nota_original TEXT NOT NULL,
        xml_nota_complementar TEXT NULL,
        xml__recibo_nota_complementar TEXT NULL
    );