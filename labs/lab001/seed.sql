-- Limpeza prévia para garantir um fresh start (Cuidado: apaga dados existentes nestas tabelas)
DROP TABLE IF EXISTS public.fato_vendas;
DROP TABLE IF EXISTS public.dim_produtos;
DROP TABLE IF EXISTS public.dim_clientes;
DROP TABLE IF EXISTS public.dim_tempo;

-- 1. Criação da Dimensão Clientes
CREATE TABLE public.dim_clientes (
    cliente_id INT PRIMARY KEY,
    nome VARCHAR(100),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    segmento VARCHAR(20)
);

-- 2. Criação da Dimensão Produtos
CREATE TABLE public.dim_produtos (
    produto_id INT PRIMARY KEY,
    nome_produto VARCHAR(100),
    categoria VARCHAR(50),
    preco_unitario DECIMAL(10, 2)
);

-- 3. Criação da Dimensão Tempo (Calendário)
CREATE TABLE public.dim_tempo (
    data_id DATE PRIMARY KEY,
    ano INT,
    mes INT,
    dia_semana VARCHAR(20),
    trimestre INT
);

-- 4. Criação da Tabela Fato Vendas
CREATE TABLE public.fato_vendas (
    venda_id SERIAL PRIMARY KEY,
    data_id DATE REFERENCES public.dim_tempo(data_id),
    cliente_id INT REFERENCES public.dim_clientes(cliente_id),
    produto_id INT REFERENCES public.dim_produtos(produto_id),
    quantidade INT,
    valor_total DECIMAL(12, 2)
);

-- POPULANDO AS DIMENSÕES
INSERT INTO public.dim_clientes VALUES 
(1, 'Ana Silva', 'Florianópolis', 'SC', 'Varejo'),
(2, 'Bruno Souza', 'São Paulo', 'SP', 'Corporativo'),
(3, 'Carla Dias', 'Rio de Janeiro', 'RJ', 'Varejo'),
(4, 'Diego Lemos', 'Porto Alegre', 'RS', 'E-commerce');

INSERT INTO public.dim_produtos VALUES 
(101, 'Notebook Pro', 'Eletrónicos', 4500.00),
(102, 'Rato Sem Fios', 'Acessórios', 150.00),
(103, 'Monitor 4K', 'Eletrónicos', 2200.00),
(104, 'Teclado Mecânico', 'Acessórios', 350.00);

INSERT INTO public.dim_tempo VALUES 
('2026-02-18', 2026, 2, 'Quarta-feira', 1),
('2026-02-19', 2026, 2, 'Quinta-feira', 1),
('2026-02-20', 2026, 2, 'Sexta-feira', 1);

-- POPULANDO A FATO (Onde a "mágica" acontece)
INSERT INTO public.fato_vendas (data_id, cliente_id, produto_id, quantidade, valor_total) VALUES 
('2026-02-18', 1, 101, 1, 4500.00),
('2026-02-18', 2, 102, 2, 300.00),
('2026-02-19', 3, 104, 1, 350.00),
('2026-02-20', 1, 103, 1, 2200.00),
('2026-02-20', 4, 102, 3, 450.00),
('2026-02-20', 2, 101, 1, 4500.00);