-- Documentação do PostgreSQL 14.5: https://halleyoliv.gitlab.io/pgdocptbr/index.html


-- Criando a tabela com suas colunas
CREATE TABLE public.nome_tabela (

    "nome_coluna" CHAR(4),     -- Coluna DIAG_PRINC do tipo CHAR(4)
);

-- Alterando o tipo da coluna
ALTER TABLE public.nome_tabela

	ALTER COLUMN "nome_coluna" TYPE CHARACTER(4),
    ALTER COLUMN "nome_coluna2" TYPE NUMERIC(4,2),
	;

-- Visualizando a tabela
SELECT * FROM public.nome_tabela;

-- Encontra dados que são diferentes de NULL
SELECT * FROM public.nome_tabela WHERE "nome_coluna" IS NOT NULL;