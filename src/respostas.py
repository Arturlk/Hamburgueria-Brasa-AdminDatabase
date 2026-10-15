# =====================================================================
#  SUAS RESPOSTAS
# =====================================================================
#  Escreva cada consulta SQL entre as aspas triplas, assim:
#
#      Q1 = """
#      SELECT ...
#      FROM ...
#      """
#
#  Depois salve o arquivo (Ctrl+S) e veja o resultado no painel.
#  Mexa só no que está ENTRE as aspas triplas.
# =====================================================================

# ---------------------------------------------------------------------
#  NÍVEL 1 - AQUECIMENTO
# ---------------------------------------------------------------------

# Q1. Clientes no Centro
# Colunas do resultado: ClientesNoCentro
Q1 = """
SELECT COUNT(*) AS ClientesNoCentro
FROM Clientes
WHERE Bairro = 'Centro';
"""

# Q2. Hambúrgueres acima de R$ 30
# Colunas do resultado: NomeProduto, Preco
Q2 = """
SELECT NomeProduto, Preco
FROM Produtos
WHERE Categoria = 'Hambúrguer'
AND Preco > 30
ORDER BY Preco DESC;
"""

# Q3. Pedidos por status
# Colunas do resultado: Status, QuantidadePedidos
Q3 = """
SELECT status, count( DataPedido)
FROM [HamburgueriaBrasa].[dbo].[Pedidos]
where DataPedido >= '2026-03-01' and status in ('Entregue', 'Cancelado' )
group by Status;
"""

# Q4. Nota média e pedidos sem avaliação
# Colunas do resultado: PedidosEntregues, PedidosAvaliados, PedidosSemAvaliacao, NotaMedia
Q4 = """
SELECT
COUNT(*)                                   AS PedidosEntregues,
COUNT(Avaliacao)                           AS PedidosAvaliados,
COUNT(*) - COUNT(Avaliacao)                AS PedidosSemAvaliacao,
AVG(Avaliacao)       AS NotaMedia
FROM Pedidos
WHERE Status = 'Entregue';
"""

# Q5. Delivery x Retirada por mês
# Colunas do resultado: Mes, TipoEntrega, QuantidadePedidos
Q5 = """
    SELECT 
        DATENAME(MONTH, DataPedido) AS Mes,
        CONVERT(INT, COUNT(IdPedido)) AS QuantidadePedidos,
        TipoEntrega
    FROM [HamburgueriaBrasa].[dbo].[Pedidos]
    GROUP BY DATENAME(MONTH, DataPedido), TipoEntrega
    order by Mes ASC
"""

# ---------------------------------------------------------------------
#  NÍVEL 2 - CRUZANDO TABELAS
# ---------------------------------------------------------------------

# Q6. Pedidos de janeiro com cliente
# Colunas do resultado: IdPedido, DataPedido, Nome, Bairro, Status
Q6 = """
SELECT  p.IdPedido,p.DataPedido,c.Nome nm_cliente,c.Bairro,p.Status
FROM [HamburgueriaBrasa].[dbo].[Pedidos] p
join [HamburgueriaBrasa].[dbo].[Clientes] c
on p.IdCliente = c.IdCliente
where p.DataPedido >= '2026-01-01' and p.DataPedido <= '2026-01-31'
order by p.DataPedido ASC
"""

# Q7. Entregas por entregador
# Colunas do resultado: Nome, Entregas
Q7 = """
SELECT  count(IdPedido) qtd_pedidos, p.IdEntregador
FROM [HamburgueriaBrasa].[dbo].[Pedidos] p
WHERE P.Status = 'Entregue' AND P.TipoEntrega = 'Delivery'
GROUP by p.IdEntregador
ORDER by p.IdEntregador
"""

# Q8. Unidades e faturamento por produto
# Colunas do resultado: NomeProduto, UnidadesVendidas, Faturamento
Q8 = """
SELECT i.IdProduto, pd.NomeProduto, sum(i.Quantidade) qtd_prod_vend, sum(i.Quantidade)  * i.PrecoUnitario faturamento, pd.Categoria
FROM [HamburgueriaBrasa].[dbo].[Pedidos] p --- join para validar 
join ItensPedido i
on p.IdPedido = i.IdPedido
join Produtos pd
on i.IdProduto = pd.IdProduto
GROUP BY  pd.NomeProduto,i.IdProduto, i.PrecoUnitario, pd.Categoria
ORDER BY qtd_prod_vend desc;
"""

# Q9. Faturamento por categoria
# Colunas do resultado: Categoria, Faturamento
Q9 = """
SELECT p.Categoria, sum(id.Quantidade*id.PrecoUnitario)   as faturamento
from ItensPedido id
join Produtos p
on id.IdProduto = p.IdProduto
Group by p.Categoria --, id.PrecoUnitario 
"""

# Q10. Bairros com 7+ pedidos entregues
# Colunas do resultado: Bairro, PedidosEntregues
Q10 = """
SELECT  count(p.IdPedido) qtd_pedidos ,c.Bairro
FROM [HamburgueriaBrasa].[dbo].[Pedidos] p
join [HamburgueriaBrasa].[dbo].[Clientes] c
on p.IdCliente = c.IdCliente
where Status = 'Entregue' 
group by c.Bairro
having count(p.IdPedido) >=7
"""

# Q11. Preços praticados do X-Bacon
# Colunas do resultado: PrecoUnitario, Unidades, Faturamento
Q11 = """
select sum(i.Quantidade) qtd_venda, i.PrecoUnitario,
sum(i.Quantidade * i.PrecoUnitario) faturamento
from ItensPedido i
join Produtos p on i.IdProduto = p.IdProduto
join Pedidos pd on i.IdPedido = pd.IdPedido
where p.NomeProduto like 'x%' and pd.Status = 'Entregue'
group by i.PrecoUnitario
"""

# ---------------------------------------------------------------------
#  NÍVEL 3 - DESAFIO
# ---------------------------------------------------------------------

# Q12. Top 3 clientes (fidelidade)
# Colunas do resultado: Nome, Pedidos, TotalGasto
Q12 = """
SELECT TOP 3
    c.Nome AS Nome,
    COUNT(DISTINCT p.IdPedido) AS Pedidos,
    SUM(i.Quantidade * i.PrecoUnitario) AS TotalGasto
FROM Clientes c
JOIN Pedidos p
    ON c.IdCliente = p.IdCliente
JOIN ItensPedido i
    ON p.IdPedido = i.IdPedido
WHERE p.Status = 'Entregue'
GROUP BY c.Nome
ORDER BY TotalGasto DESC;
"""

# Q13. Faturamento mês a mês
# Colunas do resultado: Mes, PedidosEntregues, Faturamento
Q13 = """
    SELECT
    DATENAME(MONTH, p.DataPedido) AS mes,
    COUNT(DISTINCT p.IdPedido) AS PedidosEntregues,
    SUM(i.Quantidade * i.PrecoUnitario) AS Faturamento
FROM Pedidos p
JOIN ItensPedido i
    ON p.IdPedido = i.IdPedido
WHERE p.Status = 'Entregue'
GROUP BY DATENAME(MONTH, p.DataPedido)
ORDER BY Mes;
"""

# Q14. Entregador do trimestre
# Colunas do resultado: Nome, Entregas, NotaMedia
Q14 = """
SELECT e.Nome nome_entregador, count(IdPedido) qtd_pedidos, p.IdEntregador, avg(Avaliacao) media_nota 
FROM [HamburgueriaBrasa].[dbo].[Pedidos] p
join Entregadores e on p.IdEntregador = e.IdEntregador
WHERE P.Status = 'Entregue' AND P.TipoEntrega = 'Delivery'
GROUP by p.IdEntregador, e.Nome
having count(IdPedido)  >= 4
ORDER by p.IdEntregador
"""

# Q15. Valor total dos pedidos de março
# Colunas do resultado: IdPedido, Nome, ValorProdutos, TaxaEntrega, ValorTotal
Q15 = """
  SELECT
    c.Nome,
    DATENAME(MONTH, p.DataPedido) AS mes,
    p.IdPedido,
    SUM(i.Quantidade * i.PrecoUnitario) +  sum(TaxaEntrega) AS Faturamento
FROM Pedidos p
JOIN ItensPedido i
    ON p.IdPedido = i.IdPedido
join  Clientes c
    ON c.IdCliente = p.IdCliente
WHERE p.Status = 'Entregue' and p.DataPedido >= '2026-03-01' and p.DataPedido <= '2026-03-31'
GROUP BY DATENAME(MONTH, p.DataPedido), p.IdPedido, c.Nome
ORDER BY  Faturamento desc;
"""
#####atualizar
# Q16. Clientes sem nenhum pedido
# Colunas do resultado: Nome, Bairro, DataCadastro
Q16 = """
select C.*,p.IdPedido
from Clientes C
left  JOIN Pedidos p on C.IdCliente = p.IdCliente
where p.IdPedido is null
"""

# Q17. Produto que nunca foi vendido
# Colunas do resultado: NomeProduto, Categoria, Preco
Q17 = """
select C.*
from Produtos C
left  JOIN ItensPedido p on C.IdProduto = p.IdProduto
where p.IdPedido is null
"""